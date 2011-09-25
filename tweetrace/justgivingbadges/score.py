from linkwatcher.models import TwitterUser, Mention, FundRaisingPageStats

def fundraising_profile_score(fundraising_profile):
    mentions = list(Mention.objects.select_related('tweeter').filter(link=fundraising_profile))
    score = 0
    for mention in mentions:
        if mention.is_targeted:
            score += 1
        else:
            score += mention.tweeter.followers
    return score

def percentage_success(fundraising_profile):
    stats = fundraising_page_stats(fundraising_profile)
    if stats:
        return int(stats.result_from_jg['totalRaisedPercentageOfFundraisingTarget'])
    else:
        return None

def fundraising_page_stats(fundraising_profile):
    try:
        stats = FundRaisingPageStats.objects.get(fundraiser=fundraising_profile)
    except FundRaisingPageStats.DoesNotExist:
        return None
    return stats
