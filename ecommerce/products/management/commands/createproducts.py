import os

from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction
from django.template.defaultfilters import slugify
from faker import Faker

from ecommerce.products.models import Category, ImageProduct, Product


class Command(BaseCommand):

    help = ('A command to populate the product table.\n'
            'This command does not need parameters')

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write('Creating Roles.')
        if Product.objects.exists():
            self.stdout.write(self.style.SUCCESS('Categories already exist.'))
        else:
            faker = Faker()
            categories = {
                category['name']: category['id']
                for category in Category.objects.values()
            }
            path = './pics/products'
            for filename in os.listdir(path):
                f = os.path.join(path, filename)
                name = filename.split('.')[0]
                product = Product(
                    name=name,
                    description=faker.text(10),
                    current_price=faker.pydecimal(left_digits=5,
                                                  right_digits=2,
                                                  min_value=100),
                    slug=slugify(name),
                )
                product.save()
                if category := categories.get(name.split('_')[0]):
                    product.categories.add(category)
                with open(f, 'rb') as fil:
                    ip = ImageProduct(product=product)
                    ip.image.save(f, File(fil))
                    ip.save()

            self.stdout.write(self.style.SUCCESS('OK'))
