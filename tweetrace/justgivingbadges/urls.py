from django.conf.urls.defaults import patterns, include, url

from justgivingbadges.views import (register, callback)

urlpatterns = patterns('',
    url(r'^register/$', register, name='register'),

    url(r'^callback/$',callback, name='twitter_oauth_callback'),

)
