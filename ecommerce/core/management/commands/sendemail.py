from typing import Any

from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandParser


class Command(BaseCommand):
    help = ('A command to test if email configuration is correct.\n'
            'This command does not need parameters')

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('emails', nargs='+', type=str)

    def handle(self, *args: Any, **kwargs: Any) -> None:

        emails = kwargs['emails']
        try:
            send_mail(
                'This is a test subject',
                'This is a test',
                None,
                emails,
                fail_silently=False,
            )
        except ValueError:
            self.stdout.write(self.style.ERROR('ONE OR MORE OF THE EMAILS '
                                               'ARE NOT VALID'))
            return

        self.stdout.write(self.style.SUCCESS('OK'))
