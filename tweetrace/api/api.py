import requests
import json
import base64

from django.conf import settings

HOST = 'https://api.%sjustgiving.com/%s/v1/%s'
_STAGING_SEGMENT = 'staging.'

def fundraising_page(id):
    url = _jg_url('fundraising/pages/' + id)
    return _get_json(url)

def validate_credentials(email, password):
    url = _jg_url('account/validate')
    json_obj = _post(url, email, password)
    if json_obj['isValid']:
        return json_obj['consumerId']
    return None

def _headers(username=None, password=None, content_type=False):
    headers = {'Accept': 'application/json'}
    if content_type:
        headers.update({'Content-Type': content_type})
    if username:
        headers.update(_basic_auth_header(username, password)

def _post(url, data, username=None, password=None):
    headers = _headers(username, password)
    r  = requests.post(url, data=data, headers=headers)
    return _handle_response(r)

def _get_json(url, username=None, password=None):
    headers = _headers(username, password)
    r  = requests.get(url, headers=headers)
    return _handle_response(r)

def _handle_response(r, expected_code=200):
    if r.status_code == expected_code:
        return json.loads(r.content)
    else:
        raise JustGivingAPIException(code=r.status_code)

class JustGivingAPIException(Exception):
    def __init__(self, code=None, **kwargs):
        super(JustGivingAPIException, self).__init__(**kwargs)
        self.code = code

    def __str__(self):
        if self.code is not None:
            return 'API returned %s' % self.code
        return 'Unknown error'

def _basic_auth_header(user, password):
    return {'Authorization': base64.b64encode('Basic %s:%s' % (user, password))}

def _jg_url(method):
    if settings.JUSTGIVING_LIVE:
        return HOST % ('', settings.JUSTGIVING_APP_ID, method)
    else:
        return HOST % (_STAGING_SEGMENT, settings.JUSTGIVING_APP_ID, method)
