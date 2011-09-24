from django import forms
from justgivingbadges.models import FundRaiserProfile


class FundRaiserRegistration(forms.Form):
    username = forms.CharField(
        min_length=2, max_length=200, label="Your Twitter Username")
    jg_password = forms.CharField(
        widget=forms.PasswordInput, label="Your JustGiving Password")
    jg_page = forms.CharField(
        label="Your JustGiving Page")
    email = forms.EmailField(
        label="Your email address")
    
