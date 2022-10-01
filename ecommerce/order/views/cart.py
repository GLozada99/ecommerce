from typing import Any, Mapping

from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView

from ecommerce.order.services.cart import CartService
from ecommerce.products.services.product import ProductListService


class ManageCartView(TemplateView):
    template_name = 'base/modals/add-to-cart.html'

    def post(self, request: HttpRequest,
             *args: Any, **kwargs: Any) -> HttpResponse:
        service = CartService(self.request.user,
                              self.request.COOKIES.get('cookie_id', ''))
        service.add_product(kwargs['product_id'])

        response = super().get(request, *args, **kwargs)
        response.set_cookie('cookie_id', service.cart.cookie_id_str)
        return response

    def delete(self, request: HttpRequest,
               *args: Any, **kwargs: Any) -> HttpResponse:
        service = CartService(self.request.user,
                              self.request.COOKIES.get('cookie_id', ''))
        service.remove_product(kwargs['product_id'])

        response = super().get(request, *args, **kwargs)
        return response

    def get_context_data(self, **kwargs: Any) -> Mapping:
        context = super().get_context_data(**kwargs)
        context |= {
            'configuration': (ProductListService.
                              get_configuration(kwargs['product_id'])),
            'show': True,
        }

        return context
