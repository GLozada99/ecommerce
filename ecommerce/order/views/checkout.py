from typing import Any, Mapping

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.views.generic import TemplateView

from ecommerce.order.mixins import CartViewActionMixin
from ecommerce.order.services.cart import CartInfoService, CartService
from ecommerce.order.services.checkout import CheckoutService


class CheckoutView(LoginRequiredMixin, TemplateView, CartViewActionMixin):
    template_name = 'checkout.html'

    def get_queryset(self) -> QuerySet:
        service = CartService(self.request.user,
                              self.request.COOKIES.get('cookie_id', ''))
        return CartInfoService.get_product_data(service.cart)

    def get_context_data(self, **kwargs: Any) -> Mapping:
        context = self.get_cart_context(
            super().get_context_data(**kwargs),
            None
        )
        context |= {
            'states': CheckoutService.get_states(),
            'cities': CheckoutService.get_cities(
                int(self.request.GET.get('state_id', 1))),
        }
        return context
