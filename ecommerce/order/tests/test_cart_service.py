import uuid

from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from model_bakery import baker

from ecommerce.core.models import User
from ecommerce.order.models.cart import Cart, CartProducts
from ecommerce.order.services.cart import CartService
from ecommerce.products.models.composite_models import ProductConfiguration


class CartServiceTestCase(TestCase):

    def setUp(self) -> None:
        baker.make(Cart, cookie_id=uuid.uuid4, _quantity=5)
        baker.make(User, _quantity=1)
        user = User.objects.all().first()
        baker.make(Cart, user=user)

    def test_get_cart_cookie(self) -> None:
        old_cookie_id = (Cart.objects.filter(cookie_id__isnull=False).
                         order_by('?').first().cookie_id)
        service = CartService(AnonymousUser(), str(old_cookie_id))
        old_cookie_cart = service.cart
        self.assertEqual(old_cookie_cart.cookie_id, old_cookie_id)
        self.assertIsNone(old_cookie_cart.user)

        new_cookie_id = uuid.uuid4()
        service = CartService(AnonymousUser(), str(new_cookie_id))
        new_cookie_cart = service.cart
        self.assertEqual(new_cookie_cart.cookie_id, new_cookie_id)
        self.assertIsNone(new_cookie_cart.user)

    def test_get_cart_user(self) -> None:
        old_user = User.objects.all().first()
        self.client.force_login(old_user)
        service = CartService(old_user, str(uuid.uuid4()))
        cart = service.cart
        self.assertEqual(cart.user, old_user)
        self.assertIsNone(cart.cookie_id)

        baker.make(User, _quantity=1)
        new_user = User.objects.exclude(id=old_user.id).first()
        self.client.force_login(new_user)
        service = CartService(new_user, str(uuid.uuid4()))
        cart = service.cart
        self.assertEqual(cart.user, new_user)
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
