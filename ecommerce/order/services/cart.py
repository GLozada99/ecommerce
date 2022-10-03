import uuid
from typing import Optional

from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ValidationError
from django.db.models import F, QuerySet

from ecommerce.core.models import User
from ecommerce.order.models import Cart, CartProducts


class CartService:

    def __init__(self, user: User | AnonymousUser, cookie_id: str):
        self.user = user
        self.cookie_uuid = uuid.UUID(cookie_id) if cookie_id else uuid.uuid4()
        self.cart = self._get_cart()

    def _get_cart(self) -> Cart:
        cookie_cart = Cart.objects.filter(cookie_id=self.cookie_uuid).first()
        if not self.user.is_authenticated:
            return self._get_anonymous_cart(cookie_cart)

        return self._get_auth_cart(cookie_cart)

    def _get_anonymous_cart(self, cookie_cart: Cart) -> Cart:
        return (cookie_cart if cookie_cart
                else Cart.objects.create(cookie_id=self.cookie_uuid))

    def _get_auth_cart(self, cookie_cart: Cart) -> Cart:
        if user_cart := Cart.objects.filter(user=self.user).first():
            return user_cart
        else:
            return self._migrate_cart(cookie_cart)

    def _migrate_cart(self, cookie_cart: Cart | None) -> Cart:
        if not cookie_cart:
            return Cart.objects.create(user=self.user)

        cookie_cart.cookie_id = None
        cookie_cart.user = self.user
        cookie_cart.save()
        return cookie_cart

    def get_product_data(self, product_limit: int | None = None) -> QuerySet:
        products = CartProducts.objects.filter(cart=self.cart)
        count = products.count()
        limit = (min(products.count(), product_limit)
                 if product_limit else count)
        return products[:limit]

    def add_product(self, product_id: int) -> None:
        if not CartProducts.objects.filter(cart=self.cart,
                                           product_id=product_id).exists():
            CartProducts.objects.create(cart=self.cart,
                                        product_id=product_id)
        else:
            (CartProducts.objects.filter(cart=self.cart,
                                         product_id=product_id).
             update(quantity=F('quantity') + 1))

    def remove_product(self, product_id: int) -> None:
        try:
            cart_product = (CartProducts.objects.get(
                cart=self.cart, product_id=product_id))
            cart_product.quantity -= 1
            cart_product.full_clean()
            cart_product.save()
        except ValidationError:
            CartProducts.objects.get(
                cart=self.cart, product_id=product_id).delete()
        except CartProducts.DoesNotExist:
            pass

    def delete_product(self, product_id: int) -> None:
        try:
            CartProducts.objects.get(
                cart=self.cart, product_id=product_id).delete()
        except CartProducts.DoesNotExist:
            pass

    def get_cart_context(self, product_limit: Optional[int]) -> dict:
        return {
            'products_data': self.get_product_data(product_limit),
            'get_cart_show': True,
            'total_price': self.cart.calculate_total_price()
        }
