# command to set manual spams

from helpers.page_utils import delete
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    def handle(self, *args, **options):
        ids = options['id']
        delete(ids, False)
        print("Spam, " + str(ids))

    def add_arguments(self, parser):
        parser.add_argument('id')
