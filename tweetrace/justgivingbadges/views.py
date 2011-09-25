import hashlib
from oauth import oauth
from tweepy.auth import OAuthHandler
import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.functional import wraps

from justgivingbadges.forms import FundRaiserRegistration
from justgivingbadges.models import FundRaiserProfile

from linkwatcher.models import Mention, TwitterUser, FundRaisingPageStats

from django.conf import settings

class Sticker(object):
    def __init__(self, image_url, name):
        self.name = name
        self.image_url = image_url
    def __unicode__(self):
        return self.name
GOLD = Sticker('img/gold_sticker_small.png', 'gold')
SILVER = Sticker('img/silver_sticker_small.png', 'silver')
BRONZE = Sticker('img/bronze_sticker_small.png', 'bronze')

def return_json(view):
    def wrapper(request, *args, **kwargs):
        try:
            data = view(request, *args, **kwargs)
            status = 200
        except Exception, e:
            data = {'error': str(e)}
            status = 400
        json_str = json.dumps(data, cls=JustGivingBadgesJSONEncoder)
        return HttpResponse(json_str, mimetype='application/json', status=status)
    return wraps(view)(wrapper)

def _user_from_reg_form(form):
    email = form.cleaned_data['email']
    return User.objects.create_user(
            hashlib.md5(email).hexdigest()[:16],
            password=form.cleaned_data['jg_password'],
            email=email)

def _profile_from_reg_form(form, user):
    profile, created = FundRaiserProfile.objects.get_or_create(
            jg_page_id=form.cleaned_data['jg_page'],
            defaults={'user': user}
        )
    if not created:
        if profile.user is None:
            profile.user = user
            profile.save()
        else:
            raise ValueError
    return profile

def _top_fundraisers():
    fundraisers = list(FundRaiserProfile.objects.order_by('-page_score')[:3])
    for fundraiser in fundraisers:
        _extend_profile(fundraiser)
    return fundraisers

def _extend_profile(fundraiser):
    try:
        stats = FundRaisingPageStats.objects.get(fundraiser=fundraiser)
        fundraiser.event_name = stats.result_from_jg['eventName']
        fundraiser.owner_name = stats.result_from_jg['owner']
        fundraiser.total_raised = stats.result_from_jg['totalRaisedOnline']
    except FundRaisingPageStats.DoesNotExist:
        fundraiser.event_name, fundraiser.owner_name, fundraiser.total_raised = ('', '', '')

def home(request):
    fundraiser = None
    if request.user.is_authenticated():
        fundraiser = _extend_profile(request.user.get_profile())
    top_fundraisers = _top_fundraisers()

    return render_to_response('home.html',
        {'fundraiser': fundraiser,
         'top_fundraisers': top_fundraisers},
        context_instance=RequestContext(request))

def register(request):
    if request.method == 'POST':
        form = FundRaiserRegistration(request.POST)
        if form.is_valid():
            # partially create user, and store unauthed token
            user = _user_from_reg_form(form)
            try:
                profile = _profile_from_reg_form(form, user)
            except ValueError:
                return HttpResponse('that page is already registered')

            request.session['user_id'] = user.pk
            handler = OAuthHandler(settings.TWITTER_CONSUMER_KEY,
                    settings.TWITTER_CONSUMER_SECRET,
                    callback='http://www.justgivingthanks.com/callback/',
                    secure=True)
            auth_url = handler.get_authorization_url()
            request.session['unauthed_token'] = handler.request_token.to_string()
            print 'created user, got token, redirecting to %s' % (auth_url)
            return HttpResponseRedirect(auth_url)
    else:
        form = FundRaiserRegistration() # An unbound form

    return render_to_response('registration.html',
            {'form': form},
            context_instance=RequestContext(request))

def callback(request):
    unauthed_token = request.session.get('unauthed_token', None)
    if not unauthed_token:
        return HttpResponse("No un-authed token cookie")
    token = oauth.OAuthToken.from_string(unauthed_token)
    if token.key != request.GET.get('oauth_token', 'no-token'):
        return HttpResponse("Something went wrong! Tokens do not match")
    verifier = request.GET.get('oauth_verifier')
    handler = OAuthHandler(settings.TWITTER_CONSUMER_KEY,
               settings.TWITTER_CONSUMER_SECRET,
               secure=True)
    handler.request_token = token
    access_token = handler.get_access_token(verifier)

    # save token against user
    user = User.objects.get(pk=request.session['user_id'])
    profile = user.get_profile()
    profile.access_token = access_token.key
    profile.access_token_secret = access_token.secret
    profile.save()

    redirect = reverse('fundraiser-page', kwargs={'fundraiser_id': profile.jg_page_id})
    return HttpResponseRedirect(redirect)

def fundraiser_page(request, fundraiser_id=None):
    profile = get_object_or_404(FundRaiserProfile, pk=fundraiser_id)
    _extend_profile(profile)
    my_page = request.user.is_authenticated() and profile.user == request.user

    mentions = Mention.objects.select_related('tweeter').filter(
        link=profile).order_by('-when')
    uids = [m.tweeter.uid for m in mentions]
    top_supporters = TwitterUser.objects.filter(uid__in=uids).order_by('-followers')[:5]

    return render_to_response('fundraiser.html',
            {'fundraiser': profile,
             'recent_mentions': mentions[:5],
             'top_supporters': top_supporters,
             'my_page': my_page},
            context_instance=RequestContext(request))

def supporter_page(request, fundraiser_id=None, supporter_name=None):
    profile = get_object_or_404(FundRaiserProfile, pk=fundraiser_id)
    _extend_profile(profile)
    my_page = request.user.is_authenticated() and profile.user == request.user

    supporter = TwitterUser.objects.get(screen_name=supporter_name)
    mentions = Mention.objects.filter(tweeter=supporter, link=profile).order_by('-when')

    sticker = BRONZE
    if len(mentions) > 1:
        sticker = SILVER
    if supporter.has_donated:
        sticker = GOLD

    return render_to_response('supporter.html',
            {'fundraiser': profile,
             'supporter': supporter,
             'supporter_mentions': mentions,
             'my_page': my_page,
             'sticker': sticker},
            context_instance=RequestContext(request))

@return_json
def top_fundraisers(request):
    return _top_fundraisers()

class JustGivingBadgesJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, FundRaiserProfile):
            return {
                'page_id': o.jg_page_id,
                'page_score': o.page_score,
                'event_name': o.event_name,
                'total_raised': o.total_raised,
                'owner_name': o.owner_name,
            }
        elif isinstance(o, date):
            return o.isoformat()
        else:
            return json.JSONEncoder.default(self, o)
