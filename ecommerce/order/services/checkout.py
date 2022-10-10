import json


class CheckoutService:

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
