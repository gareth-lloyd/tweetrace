from django.core.management.base import NoArgsCommand
from linkwatcher.receiver import LinkReceiver, do_watch
from twisted.internet import reactor

class Command(NoArgsCommand):
    help = "Listen for JustGiving page mentions"

    def handle_noargs(self, **options):
        do_watch()

        reactor.run()
