from typing import Any, Callable, Mapping

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from ecommerce.order.services.cart import CartService
from ecommerce.products.services.product import ProductListService


class MiniCartView(TemplateView):
    template_name = 'base/modals/cart.html'
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
        response = super().get(request, *args, **kwargs)
        service = CartService(self.request.user,
                              self.request.COOKIES.get('cookie_id', ''))
        action = self.request.GET.get('action', '_')
        product_id = int(self.request.GET.get('product_id', 0))
        self.cart_functions[action](service, product_id)

        return response

    def get_context_data(self, **kwargs: Any) -> Mapping:
        service = CartService(self.request.user,
                              self.request.COOKIES.get('cookie_id', ''))

        context = super().get_context_data(**kwargs)

        context |= service.get_cart_context(product_limit=5)

        return context


def add_cart_product_view(
        request: HttpRequest, product_id: int) -> HttpResponse:
    service = CartService(request.user,
                          request.COOKIES.get('cookie_id', ''))
    service.add_product(product_id)

    response = HttpResponse()
    response.set_cookie('cookie_id', service.cart.cookie_id_str)

    context = {
        'configuration': (ProductListService.
                          get_configuration(product_id)),
        'post_cart_show': True,
    }
    return render(request, 'base/modals/add-to-cart.html', context)
