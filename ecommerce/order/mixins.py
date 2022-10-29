from typing import Callable, Mapping

from django.http import HttpRequest

from ecommerce.order.services.cart import CartInfoService, CartService


class CartViewActionMixin:
    request: HttpRequest
    cart_functions: dict[str, Callable[[CartService, int], None]]

    def execute_cart_action(self) -> None:
        service = CartService(self.request.user,
                              self.request.COOKIES.get('cookie_id', ''))
        action = self.request.GET.get('action', '_')
        product_id = int(self.request.GET.get('product_id', 0))
        self.cart_functions[action](service, product_id)

    def get_cart_context(self, context: Mapping,
                         product_limit: int | None) -> Mapping:
        service = CartService(self.request.user,
                              self.request.COOKIES.get('cookie_id', ''))
        cart = service.cart
        context |= CartInfoService.get_cart_context(
            cart,
            product_limit=product_limit,
        )

        return context
