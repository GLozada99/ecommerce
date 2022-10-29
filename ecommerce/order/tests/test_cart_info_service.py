import uuid
from decimal import Decimal

from django.db.models import QuerySet
from django.test import TestCase
from model_bakery import baker
from parameterized import parameterized

from ecommerce.core.models import User
from ecommerce.order.models.cart import Cart, CartProducts
from ecommerce.order.services.cart import CartInfoService


class CartInfoServiceTestCase(TestCase):

    def setUp(self) -> None:
        baker.make(Cart, cookie_id=uuid.uuid4, _quantity=5)
        user = baker.make(User)
        baker.make(Cart, user=user)

    def test_get_cart_context(self) -> None:
        cart = Cart.objects.filter().order_by('?').first()
        context = CartInfoService.get_cart_context(cart, None)

        self.assertIs(context['products_data'].model, CartProducts)
        self.assertIsInstance(context['total_price'], Decimal)

    @parameterized.expand([  # type: ignore
        ("no limit", 10, None, 10),
        ("limit equals quantity", 10, 10, 10),
        ("limit less than quantity", 8, 10, 8),
        ("limit greater than quantity", 15, 10, 10),
    ])
    def test_get_cart_context_correct_number_products(
            self, _: str, quantity: int, limit: int | None,
            final_quantity: int) -> None:
        cart = Cart.objects.filter().order_by('?').first()
        baker.make(CartProducts, _quantity=quantity, cart=cart)

        context = CartInfoService.get_cart_context(cart, limit)
        products_data: QuerySet = context['products_data']
        self.assertEqual(products_data.count(), final_quantity)

    @parameterized.expand([  # type: ignore
        ("no elements", [], [], Decimal("0.0")),
        ("one element", [5], [Decimal("25")], Decimal("125")),
        ("multiple elements", [10, 2, 3],
         [Decimal("5.6"), Decimal("3.9"), Decimal("10")], Decimal("93.8")),
    ])
    def test_get_cart_context_correct_price(
            self, _: str, product_quantities: list[int],
            product_prices: list[Decimal], cart_total: Decimal) -> None:
        cart = Cart.objects.filter().order_by('?').first()

        for quantity, price in zip(product_quantities, product_prices):
            baker.make(CartProducts, cart=cart, quantity=quantity,
                       product__current_price=price)

        context = CartInfoService.get_cart_context(cart, None)
        total: Decimal = context['total_price']
        self.assertEqual(cart_total, total)
