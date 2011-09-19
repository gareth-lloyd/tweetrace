import re
from collections import defaultdict

from linkwatcher.models import TwitterUser, Mention

def sanitize_link(link):
    if link.startswith('just'):
        link = 'http://www.' + link
    elif link.startswith('ww'):
        link = 'http://' + link

    if '?' in link:
        link = link.split('?')[0]
    return link

def analyse():
    mentions = Mention.objects.select_related('tweeter').all()
    exposures = defaultdict(int)
    for mention in mentions:
        link_key = sanitize_link(mention.link)
        if mention.is_targeted:
            reach = 1
        else:
            reach = mention.tweeter.followers
        exposures[link_key] += reach
    for k, v in exposures.iteritems():
        if v < 100:
            print k, ':', v
        if v > 10000:
            print k, ':', v
