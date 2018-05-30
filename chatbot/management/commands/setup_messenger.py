from django.core.management.base import BaseCommand
from chatbot.setup import setup_messenger


class Command(BaseCommand):
    help = 'Sets up the messenger'

    def add_arguments(self, parser):

        # Greeting
        parser.add_argument(
            'greeting',
            type=str,
            nargs='?',
            default='Simplificando e automatizando a distribuição de mensagens amorosas pela Interweb.',
            help='Greeting to be used when new users open the chat'
        )

    def handle(self, *args, **options):

        # get the lookup days from args
        try:
            setup_messenger(options['greeting'])
        except Exception:
            return 'Oops! Something went wrong!'

        return 'Success'
