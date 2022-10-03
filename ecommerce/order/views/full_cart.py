from typing import Any, Callable

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView

from ecommerce.order.mixins import CartViewActionMixin
from ecommerce.order.models import CartProducts
from ecommerce.order.services.cart import CartService


class FullCartView(ListView, CartViewActionMixin):
    template_name = 'cart.html'
    context_object_name = 'products_data'
    paginate_by = 6
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

    def get_queryset(self) -> QuerySet:
        service = CartService(self.request.user,
                              self.request.COOKIES.get('cookie_id', ''))
        return CartProducts.objects.filter(
            cart=service.cart).select_related('product')
