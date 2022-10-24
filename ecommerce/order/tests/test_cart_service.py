import uuid
from functools import partial
from typing import Callable

from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from model_bakery import baker
from parameterized import parameterized

from ecommerce.core.models import User
from ecommerce.order.models.cart import Cart, CartProducts
from ecommerce.order.services.cart import CartService
from ecommerce.products.models.composite_models import ProductConfiguration


def _get_random_cookie_id() -> uuid.UUID:
    return Cart.objects.filter(
        cookie_id__isnull=False).order_by('?').first().cookie_id


def _helper_test_add_product(
        service: CartService, product_id: int, qty: int) -> None:
    for _ in range(qty):
        service.add_product(product_id)


def _helper_test_remove_product(
        service: CartService, product_id: int, qty: int,
        qty_rem: int) -> None:
    for _ in range(qty):
        service.add_product(product_id)

    for _ in range(qty_rem):
        service.remove_product(product_id)


def _helper_test_delete_all_products(
        service: CartService, product_id: int, qty: int) -> None:
    for _ in range(qty):
        service.add_product(product_id)

    service.delete_all()


class CartServiceTestCase(TestCase):

    def setUp(self) -> None:
        baker.make(Cart, cookie_id=uuid.uuid4, _quantity=5)
        baker.make(User, _quantity=1)
        user = User.objects.all().first()
        baker.make(Cart, user=user)

    @parameterized.expand([  # type: ignore
        ("old cookie id", str(_get_random_cookie_id())),
        ("new cookie id", str(uuid.uuid4())),
    ])
    def test_get_cart_anonymous_user(
            self, _: str, cookie_id: str) -> None:
        service = CartService(AnonymousUser(), cookie_id)
        cart = service.cart
        self.assertEqual(str(cart.cookie_id), cookie_id)
        self.assertIsNone(cart.user)

    @parameterized.expand([  # type: ignore
        ("old cookie id", str(_get_random_cookie_id())),
        ("new cookie id", str(uuid.uuid4())),
    ])
    def test_get_cart_user(
            self, _: str, cookie_id: str) -> None:
        user = User.objects.all().first()
        service = CartService(user, cookie_id)
        cart = service.cart
        self.assertEqual(cart.user, user)
        self.assertIsNone(cart.cookie_id)

    @parameterized.expand([  # type: ignore
        ("add product",
         partial(_helper_test_add_product, qty=5), 5,
         lambda cart, product_id, qty: CartProducts.objects.get(
             cart=cart, product_id=product_id).quantity == qty),

        ("remove product",
         partial(_helper_test_remove_product, qty=5, qty_rem=3), 2,
         lambda cart, product_id, qty: CartProducts.objects.get(
             cart=cart, product_id=product_id).quantity == qty),

        ("delete all products",
         partial(_helper_test_delete_all_products, qty=5), 0,
         lambda cart, _, __: not cart.has_products)
    ])
    def test_manage_cart(self, _: str, helper: Callable, final_qty: int,
                         true_callable: Callable) -> None:
        baker.make(ProductConfiguration, _quantity=10)

        product = ProductConfiguration.objects.all().order_by('?').first()
        cart_user = Cart.objects.all().exclude(user__isnull=True).first().user

        service = CartService(cart_user, str(uuid.uuid4()))
        cart = service.cart

        helper(service, product.id)
        self.assertTrue(true_callable(cart, product.id, final_qty))
