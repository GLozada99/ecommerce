from typing import Any, Mapping

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from ecommerce.clients.services import AddressService
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


@login_required  # type: ignore
def order_form_view(request: HttpRequest) -> HttpResponse:
    service = CheckoutService(request)
    context = service.get_checkout_info_context()
    context['delivery'] = int(bool(request.GET.get('delivery')))
    return render(request, 'checkout/order_info.html', context)


@login_required  # type: ignore
def add_address_form_view(request: HttpRequest) -> HttpResponse:
    context = {
        'states': AddressService.get_states(),
        'add_address': True,
    }
    return render(request, 'checkout/new_address.html', context)


@require_POST  # type: ignore
@login_required  # type: ignore
def add_address_view(request: HttpRequest) -> HttpResponse:
    checkout_service = CheckoutService(request)
    client = checkout_service.get_client_profile()
    AddressService.add_address(client, request.POST.dict())
    return redirect('site:checkout:checkout')


@login_required  # type: ignore
def get_cities_view(request: HttpRequest) -> HttpResponse:
    context = {
        'cities': AddressService.get_cities(
            request.GET.dict().get('state', '1')),
    }
    return render(request, 'checkout/cities_hx.html', context)


@require_POST  # type: ignore
@login_required  # type: ignore
def order_submit_view(request: HttpRequest) -> HttpResponse:
    checkout_service = CheckoutService(request)
    checkout_service.create_order()
    # TODO: Add order succesfull template and redirect there
    return redirect('site:checkout:checkout')
