# command to clean spam

from helpers.spam_utils import clean_spam
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    def handle(self, *args, **options):
        clean_spam()
