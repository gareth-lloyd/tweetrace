from django import forms
from justgivingbadges.models import FundRaiserProfile


class FundRaiserRegistration(forms.Form):
    email = forms.EmailField(
        label="Your email address")
    jg_page = forms.CharField(
        label="Your JustGiving Page")
    jg_password = forms.CharField(
        widget=forms.PasswordInput, label="Your JustGiving Password")
    
