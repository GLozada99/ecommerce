from typing import Any, Callable, Mapping

from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView

from ecommerce.order.mixins import CartViewActionMixin
from ecommerce.order.services.cart import CartService


class FullCartView(TemplateView, CartViewActionMixin):
    template_name = 'cart/items_hx.html'
    cart_functions: dict[str, Callable[[CartService, int], None]] = {
        'increase': lambda service, product_id: service.add_product(
            product_id),
        'decrease': lambda service, product_id: service.remove_product(
            product_id),
        'delete': lambda service, product_id: service.delete_product(
            product_id),
        '_': lambda _, __: None,
    }

    def patch(self, request: HttpRequest,
              *args: Any, **kwargs: Any) -> HttpResponse:
        self.execute_cart_action()
        response = super().get(request, *args, **kwargs)
        return response

    def get_context_data(self, **kwargs: Any) -> Mapping:
        return self.get_full_cart_context(super().get_context_data(**kwargs))
