from typing import Any, Mapping

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from ecommerce.order.mixins import CartViewActionMixin
from ecommerce.order.services.cart import CartService
from ecommerce.products.services.product import ProductListService


class MiniCartView(TemplateView, CartViewActionMixin):
    template_name = 'base/modals/minicart.html'
    cart_functions = {
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
        return (self.get_cart_context(
            super().get_context_data(**kwargs), product_limit=5) |
                {'get_cart_show': True, }
                )


def add_cart_product_view(
        request: HttpRequest, product_id: int) -> HttpResponse:
    service = CartService(request.user,
                          request.COOKIES.get('cookie_id', ''))
    service.add_product(product_id)

    context = {
        'configuration': (ProductListService.
                          get_configuration(product_id)),
        'post_cart_show': True,
    }
    response = render(request, 'base/modals/add-to-cart.html', context)
    response.set_cookie('cookie_id', service.cart.cookie_id_str)

    return response
