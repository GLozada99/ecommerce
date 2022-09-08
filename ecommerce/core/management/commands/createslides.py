import os

from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction

from ecommerce.core.models import SlideImage


class Command(BaseCommand):

    help = ('A command to populate the slide_image table.\n'
            'This command does not need parameters')

    @transaction.atomic  # type: ignore
    def handle(self, *args: tuple, **kwargs: dict) -> None:
        self.stdout.write('Creating SlideImages.')
        if SlideImage.objects.exists():
            self.stdout.write(self.style.SUCCESS('SlideImages already exist.'))
        else:
            path = './pics/slide_images'
            for filename in os.listdir(path):
                f = os.path.join(path, filename)
                name = filename.split('.')[0]
                slide = SlideImage.objects.create(
                    text=name,
                )
                print(name)
                with open(f, 'rb') as fil:
                    slide.image.save(name, File(fil))

            self.stdout.write(self.style.SUCCESS('OK'))
