import uuid

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

    def test_add_product_to_cart(self) -> None:
        baker.make(ProductConfiguration, _quantity=10)

        product = ProductConfiguration.objects.all().order_by('?').first()
        cart_user = Cart.objects.all().exclude(user__isnull=True).first().user

        service = CartService(cart_user, str(uuid.uuid4()))
        cart = service.cart

        service.add_product(product.id)
        self.assertTrue(cart.contains_product(product.id))

        service.add_product(product.id)
        service.add_product(product.id)
        self.assertEqual(CartProducts.objects.get(
            cart=cart, product_id=product.id).quantity, 3)

    def test_remove_product_from_cart(self) -> None:
        baker.make(ProductConfiguration, _quantity=10)

        product = ProductConfiguration.objects.all().order_by('?').first()

        cart_user = Cart.objects.all().exclude(user__isnull=True).first().user

        service = CartService(cart_user, str(uuid.uuid4()))
        cart = service.cart

        service.add_product(product.id)
        service.add_product(product.id)
        service.add_product(product.id)
        self.assertEqual(CartProducts.objects.get(
            cart=cart, product_id=product.id).quantity, 3)

        service.remove_product(product.id)
        service.remove_product(product.id)
        service.remove_product(product.id)
        self.assertFalse(cart.contains_product(product.id))

    def test_delete_all_products_from_cart(self) -> None:
        baker.make(ProductConfiguration, _quantity=10)

        products = ProductConfiguration.objects.all().order_by('?')
        product_1 = products[0]
        product_2 = products[1]

        cart_user = Cart.objects.all().exclude(user__isnull=True).first().user

        service = CartService(cart_user, str(uuid.uuid4()))
        cart = service.cart

        service.add_product(product_1.id)
        service.add_product(product_2.id)
        service.add_product(product_1.id)
        service.delete_all()
        self.assertFalse(cart.has_products)
