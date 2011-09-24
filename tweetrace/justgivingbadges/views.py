import httplib, time, datetime
from oauth import oauth
import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse

from justgivingbadges.twitter_utils import (get_unauthorised_request_token, 
        exchange_request_token_for_access_token, get_authorisation_url)
from justgivingbadges.forms import FundRaiserRegistration
from justgivingbadges.models import FundRaiserProfile

from django.conf import settings

CONSUMER = oauth.OAuthConsumer(settings.TWITTER_CONSUMER_KEY,
            settings.TWITTER_CONSUMER_SECRET)
CONNECTION = httplib.HTTPSConnection(getattr(settings, 'OAUTH_SERVER', 'twitter.com'))

def _user_from_reg_form(form):
    return User.objects.create_user(
            form.cleaned_data['username'],
            password=form.cleaned_data['jg_password'],
            email=form.cleaned_data['email'])

def _profile_from_reg_form(form, user):
    return FundRaiserProfile.objects.create(
            user=user,
            jg_page_id=form.cleaned_data['jg_page'],
        )

def register(request):
    if request.method == 'POST':
        form = FundRaiserRegistration(request.POST)
        if form.is_valid():
            # partially create user, and store unauthed token
            user = _user_from_reg_form(form)
            profile = _profile_from_reg_form(form, user)
            request.session['user_id'] = user.pk

            token = get_unauthorised_request_token(CONSUMER, CONNECTION)
            request.session['unauthed_token'] = token.to_string()

            auth_url = get_authorisation_url(CONSUMER, token)
            print 'created user, got token %s, redirecting to %s' % (token, auth_url)
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
    access_token = exchange_request_token_for_access_token(CONSUMER, token, params={'oauth_verifier':verifier})

    # save token against user
    user = User.objects.get(id=request.session['user_id'])
    profile = user.get_profile()
    profile.access_token = access_token.key
    profile.access_token_secret = access_token.secret

    return render_to_response('success.html',
            {'form': form},
            context_instance=RequestContext(request))
