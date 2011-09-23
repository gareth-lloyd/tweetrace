import requests
import json

from django.conf import settings

HOST = 'https://api.%sjustgiving.com/%s/v1/%s'
_STAGING_SEGMENT = 'staging.'
REQ_HEADERS = {
    'Accept': 'application/json'
}

class JustGivingAPIException(Exception):
    def __init__(self, code=None, **kwargs):
        super(JustGivingAPIException, self).__init__(**kwargs)
        self.code = code

    def __str__(self):
        if self.code is not None:
            return 'API returned %s' % self.code
        return 'Unknown error'

def _jg_url(method):
    if settings.JUSTGIVING_LIVE:
        return HOST % ('', settings.JUSTGIVING_APP_ID, method)
    else:
        return HOST % (_STAGING_SEGMENT, settings.JUSTGIVING_APP_ID, method)

def retrieve_page(id):
    url = _jg_url('fundraising/pages/' + id)
    r  = requests.get(url, headers=REQ_HEADERS)
    if r.status_code == 200:
        return json.loads(r.content)
    else:
        raise JustGivingAPIException(code=r.status_code)
