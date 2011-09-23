from datetime import datetime, timedelta
import re
from collections import defaultdict
from django.conf import settings
import tweepy
from twistedstream import Stream
from oauth import oauth
from twisted.internet import reactor
from twisted.python import log

from linkwatcher.models import Mention, TwitterUser, FundRaisingPageStats

LINK_PATTERN = re.compile(r"\b(w*\.?justgiving\.com/[^ ]+)", flags=re.IGNORECASE|re.MULTILINE)
JUST_GIVING_TRACK = ['justgiving']
CONSUMER = oauth.OAuthConsumer(settings.TWITTER_CONSUMER_KEY,
                           settings.TWITTER_CONSUMER_SECRET)
TOKEN = oauth.OAuthToken(settings.TWITTER_APP_ACCESS_TOKEN,
                     settings.TWITTER_APP_ACCESS_TOKEN_SECRET)
STREAM = Stream(CONSUMER, TOKEN)

def do_watch():
    d = STREAM.track(LinkReceiver(), JUST_GIVING_TRACK)
    def started(arg):
        print 'started watching'
    d.addCallback(started)
    d.addErrback(log.err)

def link_from_entities(status):
    if 'entities' not in status:
        print 'no entities for ', status['text']
        return None
    entities = status['entities']
    if 'urls' in entities and entities['urls']:
        for url in status['entities']['urls']:
            original = url['url'].lower()
            expanded = url['expanded_url']
            if expanded:
                expanded = expanded.lower()
            if 'justgiving' in original:
                return original
            if 'justgiving' in expanded:
                return expanded
    print 'NO JG URLS IN ENTITIES: ', entities
    return None

def link_search(status):
    match = LINK_PATTERN.search(status['text'])
    if match:
        return match.group(0)
    return None

def link_from_obj(status):
    link = link_from_entities(status)
    if not link:
        # twitter hasn't detected any urls, so search manually
        link = link_search(status)

    if not link and 'retweeted_status' in status:
        # this may be a retweet, in which case we may have matched the justgiving
        # link in the original rather the retweet
        original_status = status['retweeted_status']
        link = link_from_entities(original_status)
        if not link:
            link = link_search(original_status)

    return link

class LinkReceiver(object):
    def __init__(self):
        self.reconnects = 0

    def status(self, json_obj):
        try:
            just_giving_link = link_from_obj(json_obj)
            if not just_giving_link:
                print 'no just giving link in', json_obj['text']
                return

            status = tweepy.Status.parse(tweepy.api, json_obj)
            user, _ = TwitterUser.objects.get_or_create(
                uid=status.author.id,
                defaults={
                    'screen_name': status.author.screen_name,
                    'followers': status.author.followers_count,
                    'profile_picture': status.author.profile_image_url}
            )

            Mention.objects.create(
                link=just_giving_link,
                when=status.created_at,
                text=status.text,
                tweeter=user,
                is_targeted=status.text.startswith('@'),
                is_retweet=status.retweeted,
                result_from_twitter=json_obj)
        except Exception, e:
            print 'Exception', e

    def rate_limitation(self, json_obj):
        print 'Encountered rate limitation notice from twitter: %s' % json_obj

    def status_deletion(self, json_obj):
        print 'Encountered deletion notice from twitter: %s' % json_obj

    def location_deletion(self, json_obj):
        print 'Encountered deletion notice from twitter: %s' % json_obj

    def json(self, json_obj):
        print 'Encountered unrecognized JSON from twitter: %s' % json_obj

    def invalid(self, line):
        print 'Encountered invalid JSON from twitter: %s' % line

    def disconnected(self, reason):
        print 'disconnected from twitter streaming API at %s' % datetime.now()
        print 'REASON:', reason
        if self.reconnects < 40:
            reactor.callLater(self.reconnects * 10, do_watch)
