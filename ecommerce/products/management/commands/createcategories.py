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
            names = ['Ropa', 'Zapatos', 'Libros', 'Electrodomesticos',
                     'Juguetes', 'Cuidado Personal', 'Artículos de Bebé',
                     'Artículos del Hogar']
            categories = []

            for name in names:
                category = Category(
                    name=name,
                    slug=slugify(name),
                )
                with open(f'./pics/{name}.svg') as f:
                    category.icon.save(f'{name.replace(" ", "_")}.svg', f)

            Category.objects.bulk_create(categories)
            self.stdout.write(self.style.SUCCESS('OK'))
