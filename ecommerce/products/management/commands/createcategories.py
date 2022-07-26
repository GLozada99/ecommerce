import os

from django.core.management.base import BaseCommand
from django.db import transaction
from django.template.defaultfilters import slugify

from ecommerce.products.models import Category


class Command(BaseCommand):

    help = ('A command to populate the category table.\n'
            'This command does not need parameters')

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write('Creating Roles.')
        if Category.objects.exists():
            self.stdout.write(self.style.SUCCESS('Categories already exist.'))
        else:
            path = './pics/categories'
            for filename in os.listdir(path):
                f = os.path.join(path, filename)
                name = filename.split('.')[0]
                category = Category(
                    name=name,
                    slug=slugify(name),
                )
                with open(f) as fil:
                    category.icon.save(f, fil)

            self.stdout.write(self.style.SUCCESS('OK'))