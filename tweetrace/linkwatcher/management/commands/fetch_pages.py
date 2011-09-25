from django.core.management.base import NoArgsCommand
from time import sleep
from linkwatcher.models import FundRaisingPageStats, Mention
from api.api import fundraising_page, JustGivingAPIException

class Command(NoArgsCommand):
    help = "Listen for JustGiving page mentions"

    def handle_noargs(self, **options):
        for mention in list(Mention.objects.select_related('link').all()):
            try:
                if FundRaisingPageStats.objects.filter(fundraiser=mention.link).count():
                    continue

                page = fundraising_page(mention.link_id)
                FundRaisingPageStats.objects.create(fundraiser=mention.link, result_from_jg=page)
                print 'Got page', mention.link_id 
                sleep(4)
            except Exception, e:
                if isinstance(e, JustGivingAPIException) and e.code == 404:
                    print '404', mention.link_id
                else:
                    print 'OH NOES:', e

