import uuid
from typing import Any

from django.core.exceptions import ValidationError
from django.db.models import F
from django.db.transaction import atomic

from ecommerce.core.models import User
from ecommerce.order.models import Cart, CartProducts


class CartService:

    @classmethod
    @atomic  # type: ignore
    def add_to_cart(cls, user: User, cookie_id: uuid.UUID,
                    product_id: int) -> Any:
        cart = cls.get_cart(user, cookie_id)
        cls.add_product(cart, product_id)

    @classmethod
    def remove_from_cart(cls, user: User, cookie_id: uuid.UUID,
                         product_id: int) -> Any:
        cart = cls.get_cart(user, cookie_id)
        cls.remove_product(cart, product_id)

    @classmethod
    def get_cart(cls, user: User, cookie_id: uuid.UUID) -> Cart:
        if user_cart := cls.get_user_cart(user):
            return user_cart
        elif cookie_cart := cls.get_cookie_cart(cookie_id):
            return cookie_cart
        else:
            return (Cart.objects.create(user=user) if user.is_authenticated
                    else Cart.objects.create(cookie_id=cookie_id))

    @staticmethod
    def get_user_cart(user: User) -> Cart | None:
        if not user.is_authenticated:
            return None

        try:
            return Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return None

    @staticmethod
    def get_cookie_cart(cookie_id: uuid.UUID) -> Cart | None:
        try:
            return Cart.objects.get(cookie_id=cookie_id)
        except Cart.DoesNotExist:
            return None

    @classmethod
    def add_product(cls, cart: Cart, product_id: int) -> None:
        if not CartProducts.objects.filter(cart=cart,
                                           product_id=product_id).exists():
            CartProducts.objects.create(cart=cart, product_id=product_id)
        else:
            (CartProducts.objects.filter(cart=cart, product_id=product_id).
             update(quantity=F('quantity') + 1))

    @classmethod
    def remove_product(cls, cart: Cart, product_id: int) -> None:
        try:
            cart_product = (CartProducts.objects.get(
                cart=cart, product_id=product_id))
            cart_product.quantity -= 1
            cart_product.full_clean()
            cart_product.save()
        except ValidationError:
            CartProducts.objects.get(cart=cart, product_id=product_id).delete()
        except CartProducts.DoesNotExist:
            pass
