from django.db import models
from django.contrib.auth.models import User

class FundRaiserProfile(models.Model):
    jg_page_id = models.CharField(max_length=200, primary_key=True)
    user = models.OneToOneField(User, blank=True, null=True, default=None)

    twitter_id = models.BigIntegerField(null=True, blank=True)
    access_token = models.CharField(max_length=200,null=True, blank=True)
    access_token_secret = models.CharField(max_length=200,null=True, blank=True)
    twitter_username = models.CharField(max_length=200,null=True, blank=True)
