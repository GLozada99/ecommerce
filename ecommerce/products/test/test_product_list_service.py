from django.test import TestCase
from model_bakery import baker

from ecommerce.products.models.composite_models import ProductConfiguration
from ecommerce.products.models.models import Product
from ecommerce.products.services.product import ProductListService


class ProductListServiceTestCase(TestCase):

    def setUp(self) -> None:
        product_quantity = 10
        baker.make(ProductConfiguration, _quantity=product_quantity)

    def test_products_contain_current_price(self) -> None:
        products = Product.objects.all()
        result_products = ProductListService.get_products(products, '')

        for initial, final in zip(products, result_products):
            self.assertFalse(hasattr(initial, 'current_price'))
            self.assertTrue(hasattr(final, 'current_price'))

    def test_products_order_by_name(self) -> None:
        products = Product.objects.all()
        result_products = ProductListService.get_products(products, 'name')
        sorted_products = sorted(products, key=lambda p: p.name.upper())

        for r_product, s_product in zip(result_products, sorted_products):
            self.assertEqual(r_product.id, s_product.id)

    def test_products_order_by_current_price(self) -> None:
        products = Product.objects.all()
        result_products = ProductListService.get_products(products,
                                                          'current_price')
        sorted_products = sorted(
            products, key=lambda p: p.configurations.first().current_price
        )

        for r_product, s_product in zip(result_products, sorted_products):
            self.assertEqual(r_product.id, s_product.id)

    def test_current_price_comes_from_first_config(self) -> None:
        products = Product.objects.all().order_by('name')
        result_products = ProductListService.get_products(products, 'name')

        for product, s_product in zip(products, result_products):
            first_config = product.configurations.first()
            self.assertEqual(first_config.current_price,
                             s_product.current_price)
