import re
from django.core.management.base import NoArgsCommand
from time import sleep
from linkwatcher.models import FundRaisingPageStats, Mention
from api.api import fundraising_page
import urllib
import urlparse

PAGE_NAME_PATT = re.compile(r'giving\.com/([^/?]+)', re.IGNORECASE)
def page_name(link_text):
    match = PAGE_NAME_PATT.search(link_text)
    if not match:
        return None
    else:
        return match.group(1)

class Command(NoArgsCommand):
    help = "Listen for JustGiving page mentions"

    def handle_noargs(self, **options):
        for mention in list(Mention.objects.all()):
            try:
                name = page_name(mention.link)
                if not name or FundRaisingPageStats.objects.filter(page_name=name).count():
                    continue

                page = fundraising_page(name)
                FundRaisingPageStats.objects.create(page_name=name, result_from_jg=page)
                print 'Got page', name
                sleep(4)
            except Exception, e:
                print 'OH NOES:', e

