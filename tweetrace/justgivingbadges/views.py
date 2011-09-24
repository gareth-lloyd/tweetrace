import hashlib
from oauth import oauth
from tweepy.auth import OAuthHandler
import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from justgivingbadges.forms import FundRaiserRegistration
from justgivingbadges.models import FundRaiserProfile

from linkwatcher.models import Mention, TwitterUser

from django.conf import settings

def _user_from_reg_form(form):
    email = form.cleaned_data['email']
    return User.objects.create_user(
            hashlib.md5(email).hexdigest()[:16],
            password=form.cleaned_data['jg_password'],
            email=email)

def _profile_from_reg_form(form, user):
    profile, created = FundRaiserProfile.objects.get_or_create(
            jg_page_id=form.cleaned_data['jg_page'],
            defaults={user: user}
        )
    if not created:
        if profile.user is None:
            profile.user = user
            profile.save()
        else:
            raise ValueError
    return profile

def home(request):
    top_pages = []
    return render_to_response('home.html',
        {'top_pages': top_pages},
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
    user = User.objects.get(id=request.session['user_id'])
    profile = user.get_profile()
    profile.access_token = access_token.key
    profile.access_token_secret = access_token.secret

    return render_to_response('success.html',
            {},
            context_instance=RequestContext(request))

def fundraiser_page(request, fundraiser_id=None):
    profile = get_object_or_404(FundRaiserProfile, pk=fundraiser_id)
    my_page = request.user.is_authenticated() and profile.user == request.user

    mentions = Mention.objects.select_related('tweeter').filter(link=profile)

    return render_to_response('supporters.html',
            {'fundraiser': profile,
             'mentions': mentions,
             'my_page': my_page},
            context_instance=RequestContext(request))

def supporter_page(request, fundraiser_id=None, supporter_name=None):
    profile = get_object_or_404(FundRaiserProfile, pk=fundraiser_id)
    my_page = request.user.is_authenticated() and profile.user == request.user

    supporter = TwitterUser.objects.get(screen_name=supporter_name)
    mentions = Mention.objects.filter(tweeter=supporter, link=profile)

    return render_to_response('supporter.html',
            {'fundraiser': profile,
             'mentions': mentions,
             'my_page': my_page},
            context_instance=RequestContext(request))
