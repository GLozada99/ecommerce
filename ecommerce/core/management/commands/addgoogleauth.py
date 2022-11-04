from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from django.db import transaction

from ecommerce.settings import env_settings


class Command(BaseCommand):
    help = ('A command to populate the slide_image table.\n'
            'This command does not need parameters')

    @transaction.atomic  # type: ignore
    def handle(self, *args: tuple, **kwargs: dict) -> None:
        if Site.objects.filter(domain=env_settings.SITE_DOMAIN).exists():
            self.stdout.write(self.style.SUCCESS('Google auth already '
                                                 'implemented.'))
            return
        site = Site.objects.first()
        site.name = env_settings.SITE_NAME
        site.domain = env_settings.SITE_DOMAIN
        site.save()
        app = SocialApp(provider='google', name='Google',
                        client_id=env_settings.SITE_GOOGLE_ID,
                        secret=env_settings.SITE_GOOGLE_SECRET)

        app.save()
        app.sites.add(site)
