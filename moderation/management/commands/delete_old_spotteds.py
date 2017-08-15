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

        return delete_executer(days, commit)


def delete_executer(days, commit):

    del_date = now - timedelta(days=days)

    # Filter spotteds
    spotteds = Spotted.objects.all().filter(created__lt=del_date)

    if commit:
        [s.delete() for s in spotteds]
        return str(len(spotteds)) + ' spotteds flushed successfully.'
    else:
        return str(len(spotteds)) + ' spotteds flushed successfully. (not commited)'
