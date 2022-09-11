import random
from unittest.mock import MagicMock, patch

import faker
from django.test import TestCase
from model_bakery import baker

from ecommerce.products.models.composite_models import (ProductConfiguration,
                                                        ProductPicture, )
from ecommerce.products.models.models import Product
from ecommerce.products.services.product import ProductDetailService


class ProductDetailServiceTestCase(TestCase):

    def setUp(self) -> None:
        product_quantity = 10
        baker.make(ProductConfiguration, _quantity=product_quantity)

    def test_get_product_configuration(self) -> None:
        product = Product.objects.first()

        first_configuration = product.configurations.first()
        not_existing_id = ProductConfiguration.objects.exclude(
            product=product).first().id

        last_configuration = product.configurations.last()

        service = ProductDetailService(product)
        self.assertEqual(service.get_product_configuration(
            last_configuration.id), last_configuration)
        self.assertEqual(service.get_product_configuration(
            not_existing_id), first_configuration)

    @patch('thumbnails.images.Thumbnail.url')
    def test_get_product_thumbnails(
            self, thumbnail_url_mock: MagicMock) -> None:
        thumbnail_url_mock.return_value = lambda: faker.Faker().file_name(
            category='image')

        max_individual_pic_number = 10
        product = Product.objects.order_by('?').first()

        baker.make(
            ProductPicture, _quantity=10,
            product=product,
        )
        baker.make(
            ProductConfiguration, _quantity=4,
            product=product,
        )

        total_pic_number = (product.configurations.count() +
                            min(product.pictures.count(),
                                max_individual_pic_number)
                            )

        service = ProductDetailService(product)
        thumbnail_data = service.get_product_thumbnails(
            max_individual_pic_number)

        for data in thumbnail_data:
            self.assertTrue('url' in data)
            self.assertTrue('id' in data)
            self.assertTrue('type' in data)
        self.assertEqual(len(thumbnail_data), total_pic_number)

    @patch('thumbnails.images.Thumbnail.url')
    def test_get_configurations_data(
            self, thumbnail_url_mock: MagicMock) -> None:
        thumbnail_url_mock.return_value = lambda: faker.Faker().file_name(
            category='image')

        product = Product.objects.order_by('?').first()

        baker.make(
            ProductConfiguration, _quantity=4,
            product=product,
        )

        service = ProductDetailService(product)
        configuration_data = service.get_configurations_data()

        for data in configuration_data:
            self.assertTrue('id' in data)
            self.assertTrue('name' in data)
            self.assertTrue('current_price' in data)
            self.assertTrue('url' in data)
        self.assertEqual(len(configuration_data),
                         product.configurations.count())

    @patch('thumbnails.images.Thumbnail.url')
    def test_get_product_picture_url(
            self, thumbnail_url_mock: MagicMock) -> None:
        thumbnail_url_mock.return_value = lambda: faker.Faker().file_name(
            category='image')

        max_individual_pic_number = 10
        product = Product.objects.order_by('?').first()

        baker.make(
            ProductPicture, _quantity=10,
            product=product,
        )
        baker.make(
            ProductConfiguration, _quantity=4,
            product=product,
        )

        service = ProductDetailService(product)
        thumbnail_data = service.get_product_thumbnails(
            max_individual_pic_number)
        rand_thumbnail = random.choice(thumbnail_data)
        large_pic_url = getattr(product, rand_thumbnail['type']).get(
            id=rand_thumbnail['id']).picture.thumbnails.large.url

        self.assertEqual(large_pic_url, service.get_product_picture_url(
                                            rand_thumbnail['type'],
                                            int(rand_thumbnail['id'])
                                        )
                         )
