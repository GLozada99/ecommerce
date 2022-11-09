import uuid
from functools import partial
from typing import Callable

from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from model_bakery import baker
from parameterized import parameterized

from ecommerce.core.models import User
from ecommerce.order.helpers.tests import (
    get_random_cookie_id,
    helper_test_add_product,
    helper_test_delete_all_products,
    helper_test_remove_product,
)
from ecommerce.order.models.cart import Cart, CartProducts
from ecommerce.order.services.cart import CartService
from ecommerce.products.models.composite_models import ProductConfiguration


class CartServiceTestCase(TestCase):

    def setUp(self) -> None:
        baker.make(Cart, cookie_id=uuid.uuid4, _quantity=5)
        user = baker.make(User)
        baker.make(Cart, user=user)

    @parameterized.expand([  # type: ignore
        ("old cookie id", lambda: str(get_random_cookie_id())),
        ("new cookie id", lambda: str(uuid.uuid4())),
    ])
    def test_get_cart_anonymous_user(
            self, _: str, get_cookie_id: Callable) -> None:
        cookie_id = get_cookie_id()
        service = CartService(AnonymousUser(), cookie_id)
        cart = service.cart
        self.assertEqual(str(cart.cookie_id), cookie_id)
        self.assertIsNone(cart.user)

    @parameterized.expand([  # type: ignore
        ("old cookie id", lambda: str(get_random_cookie_id())),
        ("new cookie id", lambda: str(uuid.uuid4())),
    ])
    def test_get_cart_user(
            self, _: str, get_cookie_id: Callable) -> None:
        user = User.objects.all().first()
        service = CartService(user, get_cookie_id())
        cart = service.cart
        self.assertEqual(cart.user, user)
        self.assertIsNone(cart.cookie_id)

    @parameterized.expand([  # type: ignore
        ("add product",
         partial(helper_test_add_product, qty=5), 5,
         lambda cart, product_id, qty: CartProducts.objects.get(
             cart=cart, product_id=product_id).quantity == qty),

        ("remove product",
         partial(helper_test_remove_product, qty=5, qty_rem=3), 2,
         lambda cart, product_id, qty: CartProducts.objects.get(
             cart=cart, product_id=product_id).quantity == qty),

        ("delete all products",
         partial(helper_test_delete_all_products, qty=5), 0,
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
