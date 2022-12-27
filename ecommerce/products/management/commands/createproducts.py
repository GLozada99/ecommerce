import os
import uuid

from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify
from faker import Faker

from ecommerce.products.models.composite_models import ProductConfiguration
from ecommerce.products.models.models import Category, Product


class Command(BaseCommand):
    help = ('A command to populate the product table.\n'
            'This command does not need parameters')

    @transaction.atomic  # type: ignore
    def handle(self, *args: tuple, **kwargs: dict) -> None:
        self.stdout.write('Creating Products.')
        if Product.objects.exists():
            self.stdout.write(self.style.SUCCESS('Products already exist.'))
        else:
            faker = Faker()
            categories = {
                category['name']: category['id']
                for category in Category.objects.values()
            }
            path = './pics/products'
            for directory in os.listdir(path):
                full_directory = os.path.join(path, directory)
                for sub_dir in os.listdir(full_directory):
                    full_subdirectory = os.path.join(full_directory, sub_dir)
                    product = Product.objects.populate(True).create(
                        name=sub_dir,
                        general_description='\n\r\n\r'.join(
                            faker.paragraphs(5)
                        ),
                        slug=slugify(sub_dir[:50]),
                        category_id=categories.get(directory)
                    )

                    for i, filename in enumerate(
                            os.listdir(full_subdirectory)):
                        name, ext = filename.split('.')
                        full_filepath = os.path.join(
                            full_subdirectory, filename
                        )
                        configuration = ProductConfiguration(
                            store_id=faker.isbn13(),
                            product=product,
                            name=name,
                            slug=slugify(name[:50]),
                            description='\n\r\n\r'.join(faker.paragraphs(5))
                            if i % 2 == 0 else '',
                            current_price=faker.pydecimal(left_digits=5,
                                                          right_digits=2,
                                                          min_value=100),
                        )
                        print(filename)
                        with open(full_filepath,
                                  'rb') as fil:
                            configuration.picture.save(
                                "%s.%s" % (uuid.uuid4(), ext), File(fil))
                            configuration.save()

            self.stdout.write(self.style.SUCCESS('OK'))
