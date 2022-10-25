import uuid
from decimal import Decimal

from django.test import TestCase
from model_bakery import baker
from parameterized import parameterized

from ecommerce.clients.models import Address
from ecommerce.core.models import User
from ecommerce.order.helpers.tests import get_random_post_data
from ecommerce.order.models.cart import Cart, CartProducts
from ecommerce.order.models.order import Order, OrderProducts
from ecommerce.order.services.cart import CartService
from ecommerce.order.services.checkout import CheckoutService


class CheckoutServiceTestCase(TestCase):

    def setUp(self) -> None:
        baker.make(Cart, cookie_id=uuid.uuid4, _quantity=5)
        user = baker.make(User)
        baker.make(User, is_staff=True)
        baker.make(Cart, user=user)

    def test_get_checkout_context(self) -> None:
        user = User.objects.filter(is_staff=False).order_by('?').first()
        service = CheckoutService(user, {})
        context = service.get_checkout_info_context()

        self.assertIs(context['addresses'].model, Address)
        self.assertIsInstance(context['phone'], str)
        self.assertIsInstance(context['email'], str)
        self.assertIsInstance(context['payment_types'], list)
        self.assertIsInstance(context['delivery'], int)

    @parameterized.expand([  # type: ignore
        ("pickup", {}, Order.PaymentChoices.PICKUP),
        ("card on delivery", {'delivery': True,
                              'payment': Order.PaymentChoices.CARD_DELIVERY},
         Order.PaymentChoices.CARD_DELIVERY),
        ("cash on delivery", {'delivery': True,
                              'payment': Order.PaymentChoices.CASH_DELIVERY},
         Order.PaymentChoices.CASH_DELIVERY),
    ])
    def test_create_order_correct_payment_type(
            self, _: str, extra_post_data: dict,
            payment_type: Order.PaymentChoices) -> None:
        user = User.objects.filter(is_staff=False).order_by('?').first()
        cart = Cart.objects.filter(user=user).order_by('?').first()
        baker.make(CartProducts, cart=cart, _quantity=10)

        post_data = get_random_post_data() | extra_post_data
        service = CheckoutService(user, post_data)
        order = service.create_order(CartService(user, ''))
        self.assertEqual(order.payment_type, payment_type)

    @parameterized.expand([  # type: ignore
        ("1", [5], [Decimal("25")], Decimal("125")),
        ("2", [10, 2, 3],
         [Decimal("5.6"), Decimal("3.9"), Decimal("10")], Decimal("93.8")),
        ("3", [15, 7, 6],
         [Decimal("15.4"), Decimal("23.9"), Decimal("5")], Decimal("428.3")),
    ])
    def test_create_order(
            self, _: str, product_quantities: list[int],
            product_prices: list[Decimal], order_total: Decimal, ) -> None:
        user = User.objects.filter(is_staff=False).order_by('?').first()
        cart = Cart.objects.filter(user=user).order_by('?').first()
        ids = []
        for quantity, price in zip(product_quantities, product_prices):
            cp = baker.make(CartProducts, cart=cart, quantity=quantity,
                            product__current_price=price)
            ids.append(cp.product.id)

        post_data = get_random_post_data()
        service = CheckoutService(user, post_data)
        order = service.create_order(CartService(user, ''))
        products_order = {data.product.id: data for data in
                          OrderProducts.objects.filter(order=order).all()}
        for id_, quantity, price in zip(
                ids, product_quantities, product_prices):
            product_data: OrderProducts = products_order[id_]
            self.assertEqual(product_data.quantity, quantity)
            self.assertEqual(product_data.product.current_price, price)
        self.assertEqual(order.total, order_total)
