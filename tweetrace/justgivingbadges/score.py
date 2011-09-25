from linkwatcher.models import TwitterUser, Mention, FundRaisingPageStats
from justgivingbadges.models import FundRaiserProfile
from math import log

def fundraiser_score(fundraiser):
    mentions = list(Mention.objects.select_related('tweeter').filter(link=fundraiser))
    score = 0
    for mention in mentions:
        if mention.is_targeted:
            score += 1
        else:
            # a single tweet to a massive follower base can skew results, so 
            # we base it on the log of followers
            if mention.tweeter.followers > 0:
                score += int(3 * (log(mention.tweeter.followers, 2)))
    return score

def percentage_success(fundraiser):
    stats = fundraising_page_stats(fundraiser)
    if stats:
        return int(stats.result_from_jg['totalRaisedPercentageOfFundraisingTarget'])
    else:
        return None

def fundraising_page_stats(fundraiser):
    try:
        stats = FundRaisingPageStats.objects.get(fundraiser=fundraiser)
    except FundRaisingPageStats.DoesNotExist:
        return None
    return stats

def _update_score(fundraiser):
    fundraiser.page_score = fundraiser_score(fundraiser)
    fundraiser.save()

def _update_all_scores():
    for fundraiser in FundRaiserProfile.objects.all():
        _update_score(fundraiser)

