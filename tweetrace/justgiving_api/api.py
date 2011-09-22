import requests
from xml.dom import minidom
from lxml import etree
import StringIO

from django.conf import settings

HOST = 'https://api.%sjustgiving.com/%s/v1/%s'
_STAGING_SEGMENT = 'staging.'
REQ_HEADERS = {
    'Accept': 'application/xml'
}

class JustGivingAPIException(Exception):
    def __init__(self, code=None, **kwargs):
        super(JustGivingAPIException, self).__init__(**kwargs)
        self.code = code

    def __str__(self):
        if self.code is not None:
            return 'API returned %s' % self.code
        return 'Unknown error'

class FundraisingPage(object):
    pass

def parse2(content):
        dom = minidom.parseString(content)
        total = dom.getElementsByTagName(
            'grandTotalRaisedExcludingGiftAid')[0].childNodes[0].wholeText
        percent = dom.getElementsByTagName(
            'totalRaisedPercentageOfFundraisingTarget')[0].childNodes[0].wholeText

def element_to_kv(element):
    if len(element) == 0:
        return (element.tag, element.text)
    else:
        return (element.tag, dict([element_to_kv(el) for el in element]))

def parse(content):
    f = StringIO.StringIO(content)
    doc = etree.parse(f).getroot()
    return dict((element_to_kv(element) for element in doc))

def _jg_url(method):
    if settings.JUSTGIVING_LIVE:
        return HOST % ('', settings.JUSTGIVING_APP_ID, method)
    else:
        return HOST % (_STAGING_SEGMENT, settings.JUSTGIVING_APP_ID, method)

def retrieve_funds_raised(id):
    url = _jg_url('fundraising/pages/' + id)
    r  = requests.get(url, headers=REQ_HEADERS)
    if r.status_code == 200:
        return parse(r.content)
    else:
        raise JustGivingAPIException(code=r.status_code)
