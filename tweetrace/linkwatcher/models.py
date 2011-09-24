from django.db import models
from picklefield import PickledObjectField
from justgivingbadges.models import FundRaiserProfile


class TwitterUser(models.Model):
    uid             = models.BigIntegerField(primary_key=True)
    screen_name     = models.CharField(max_length=20, db_index=True)
    profile_picture = models.URLField(max_length=1000)
    followers       = models.IntegerField()

    def json_object(self):
        return {'id': self.uid,
            'screen_name': self.screen_name,
            'profile_picture': self.profile_picture,
            'followers': self.followers
        }


class Mention(models.Model):
    link = models.ForeignKey(FundRaiserProfile)
    when = models.DateTimeField()
    text = models.CharField(max_length=200)
    tweeter = models.ForeignKey(TwitterUser)
    is_targeted = models.BooleanField()
    is_retweet = models.BooleanField()
    result_from_twitter = PickledObjectField(null=True, blank=True)

class FundRaisingPageStats(models.Model):
    fundraiser = models.ForeignKey(FundRaiserProfile, null=True, blank=True, default=None)
    result_from_jg = PickledObjectField(null=True, blank=True)


