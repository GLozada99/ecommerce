from django.http import HttpRequest

from django.http import HttpRequest

from ecommerce.clients.models import Client
from ecommerce.core.models import User
from ecommerce.order.models.order import Order


class CheckoutService:

    def __init__(self, request: HttpRequest):
        self.request = request

    def get_client_profile(self) -> Client:
        try:
            return self.request.user.client_profile
        except AttributeError:
            return Client.objects.create(user=self.request.user)

    def get_checkout_info_context(self) -> dict:
        user: User = self.request.user
        return {
            'addresses': self.get_client_profile().addresses.all(),
            'phone': user.phone or '',
            'email': user.email or '',
            'payment_types': Order.payment_choices,
            'delivery': 1,
        }
