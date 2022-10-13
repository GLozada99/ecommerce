from typing import Any, Mapping

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from ecommerce.order.mixins import CartViewActionMixin
from ecommerce.order.services.checkout import CheckoutService


class CheckoutView(LoginRequiredMixin, TemplateView, CartViewActionMixin):
    template_name = 'checkout.html'

    def get_context_data(self, **kwargs: Any) -> Mapping:
        context = self.get_cart_context(
            super().get_context_data(**kwargs),
            None
        )
        service = CheckoutService(self.request)
        context |= service.get_checkout_info_context()
        return context


def order_form_view(request: HttpRequest, delivery: int) -> HttpResponse:
    service = CheckoutService(request)
    context = service.get_checkout_info_context()
    context['delivery'] = int(not delivery)

    return render(request, 'checkout/order_info.html', context)


def add_address_view(request: HttpRequest) -> HttpResponse:
    context = {
        'states': CheckoutService.get_states(),
        'cities': CheckoutService.get_cities(
            int(request.GET.get('state_id', 1))),
    }

    # TODO: Fix template
    return render(request, 'list/categories_hx.html', context)
