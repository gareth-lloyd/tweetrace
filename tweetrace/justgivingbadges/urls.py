from django.conf.urls.defaults import patterns, include, url

from justgivingbadges.views import (register, callback,
            home, fundraiser_page, supporter_page, top_fundraisers)

urlpatterns = patterns('',
    url(r'^register/$', register, name='register'),
    url(r'^callback/$', callback, name='twitter-oauth-callback'),

    url(r'^$', home, name='home-page'),
    url(r'^top_fundraisers/$', top_fundraisers, name='top-fundraisers'),
    url(r'^fundraiser/(?P<fundraiser_id>\w+)/$',
        fundraiser_page, name='fundraiser-page'),
    url(r'^fundraiser/(?P<fundraiser_id>\w+)/supporter/(?P<supporter_name>\w+)/$',
        supporter_page, name='supporter-page'),
)
