import json
from functools import lru_cache

from ecommerce.clients.models import Address, Client


class AddressService:

    @staticmethod
    @lru_cache
    def get_states() -> list:
        with open('./states/states.json') as fil:
            data = json.load(fil)
            return data['data']

    @staticmethod
    @lru_cache
    def get_cities(state_id: str) -> list:
        with open(f'./states/cities/cities_{state_id}.json') as fil:
            data = json.load(fil)
            return data['data']

    @staticmethod
    def get_map(data: list[dict]) -> dict:
        return {str(entry['id']): entry for entry in data}

    @classmethod
    def add_address(cls, client: Client, post_data: dict) -> Address:
        state = cls.get_map(cls.get_states())[post_data['state']]
        city = cls.get_map(cls.get_cities(post_data['state']))[post_data[
            'city']]

        return Address.objects.create(
            client=client,
            state=state['name'],
            city=city['name'],
            first_line=post_data['first_line'],
            second_line=post_data['second_line'],
        )
