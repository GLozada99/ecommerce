import os

from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction
from django.template.defaultfilters import slugify
from faker import Faker

from ecommerce.products.models.composite_models import (ProductConfiguration,
                                                        ProductImage, )
from ecommerce.products.models.models import Category, Product


class Command(BaseCommand):

    help = ('A command to populate the product table.\n'
            'This command does not need parameters')

    @transaction.atomic  # type: ignore
    def handle(self, *args: tuple, **kwargs: dict) -> None:
        self.stdout.write('Creating Products.')
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
                with open(f, 'rb') as fil:
                    product = Product(
                        name=name,
                        general_description='\n\r\n\r'.join(
                            faker.paragraphs(20)
                        ),
                        slug=slugify(name),
                        category_id=categories.get(name.split('_')[0])
                    )
                    product.general_image.save(f, File(fil))
                    product.save()
                type_product = ProductConfiguration.objects.create(
                    product=product,
                    name=faker.word(),
                    description='\n\r\n\r'.join(faker.paragraphs(5)),
                    current_price=faker.pydecimal(left_digits=5,
                                                  right_digits=2,
                                                  min_value=100),
                )
                with open(f, 'rb') as fil:
                    ip = ProductImage(product=type_product)
                    ip.image.save(f, File(fil))
                    ip.save()

            self.stdout.write(self.style.SUCCESS('OK'))
