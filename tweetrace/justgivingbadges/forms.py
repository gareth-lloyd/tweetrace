import re

from django import forms
from justgivingbadges.models import FundRaiserProfile

JG_URL = re.compile(
    r"""\b                          # start at word boundary
        (?:https?://)?              # protocol optional
        (?:www\d{0,3}\.)?           # server optionl
        (?:justgiving\.com/)?       # domain optional
        ([a-zA-Z0-9-]+)             # capture path
        (.*)                        # capture the rest
    """, re.IGNORECASE|re.UNICODE|re.VERBOSE);

def cleaned_page_id(candidate_id, strict=False):
    m = JG_URL.match(candidate_id)
    if m:
        page_id = m.group(1)
        print m.group(1)
        if strict and m.group(2):
            print m.group(2)
            return None
        else:
            return page_id
    else:
        return None

class FundRaiserRegistration(forms.Form):

    def clean_jg_page(self):
        jg_page = self.cleaned_data['jg_page']
        jg_page = cleaned_page_id(jg_page, strict=True)
        if not jg_page:
            raise forms.ValidationError('That\'s not a valid JustGiving Page')
        return jg_page

    email = forms.EmailField(
        label="Your email address")
    jg_page = forms.CharField(
        label="Your JustGiving Page")
    jg_password = forms.CharField(
        widget=forms.PasswordInput, label="Your JustGiving Password")

