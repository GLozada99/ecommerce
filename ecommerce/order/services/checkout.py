import json

from django.http import HttpRequest
from django.utils.translation import gettext as _

from ecommerce.clients.models import Client


class CheckoutService:

    def __init__(self, request: HttpRequest):
        self.request = request

    @staticmethod
    def get_states() -> list:
        with open('./states/states.json') as fil:
            data = json.load(fil)
            return data['data']

    @staticmethod
    def get_cities(state_id: int) -> list:
        with open(f'./states/cities/cities_{state_id}.json') as fil:
            data = json.load(fil)
            return data['data']

    def get_client_profile(self) -> Client:
        try:
            return self.request.user.client_profile
        except AttributeError:
            return Client.objects.create(user=self.request.user)

    def get_checkout_info_context(self) -> dict:
        return {
            'addresses': self.get_client_profile().addresses.all(),
            'phone': self.request.user.phone,
            'email': self.request.user.email,
            'payment_types': [
                _('Cash on delivery'),
                _('Card on delivery'),
                _('Bank Transfer on delivery'),
            ],
            'delivery': 0,
        }
