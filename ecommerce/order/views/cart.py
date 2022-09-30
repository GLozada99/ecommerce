from typing import Any

from django.http import HttpRequest, HttpResponse
from django.views import View

from ecommerce.order.services.cart import CartService


class ManageCartView(View):

    def post(self, request: HttpRequest,
             *args: Any, **kwargs: Any) -> HttpResponse:
        service = CartService(self.request.user,
                              self.request.COOKIES.get('cookie_id', ''))
        service.add_product(kwargs['product_id'])

        response = HttpResponse()
        response.set_cookie('cookie_id', service.cart.cookie_id_str)
        return response

    def delete(self, request: HttpRequest,
               *args: Any, **kwargs: Any) -> HttpResponse:
        service = CartService(self.request.user,
                              self.request.COOKIES.get('cookie_id', ''))
        service.remove_product(kwargs['product_id'])

        return HttpResponse()
