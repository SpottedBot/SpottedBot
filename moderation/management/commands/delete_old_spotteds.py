from django.core.management.base import BaseCommand
from spotteds.models import Spotted
from datetime import timedelta
from django.utils import timezone
now = timezone.now()


class Command(BaseCommand):
    help = 'Deletes old spotteds'

    def add_arguments(self, parser):

        # Days
        parser.add_argument('days', type=int, help='Deletes spotteds older than this number of days')

        # Commit deletion
        parser.add_argument(
            '--commit',
            action='store_true',
            dest='commit',
            default=False,
            help='Whether or not to commit the Spotted deletion',
        )

    def handle(self, *args, **options):

        # get the lookup days from args
        days = int(options['days'])

        # Get whether or not the changes are to be commited
        commit = options['commit']

        # Get all spotteds
        spotteds = Spotted.objects.all().order_by('created')

        del_date = now - timedelta(days=days)

        counter = 0
        for s in spotteds:
            if s.created < del_date:
                counter += 1

                if commit:
                    s.delete()
            else:
                break

        if commit:
            return str(counter) + ' spotteds flushed successfully.'
        else:
            return str(counter) + ' spotteds flushed successfully. (not commited)'
