import requests
from os import path

class Medicine(object):
    def __init__(self, id, name, currency_code,price, dispensing_fee):
        self.id = id
        self.name = name
        self.currency_code = currency_code
        self.price = price
        self.dispensing_free = dispensing_fee

class MedicineRegistry(object):
    def __init__(self):
        self.url = 'https://mpr.code4sa.org/api/v2/'
        self.currency_code = 'ZAR'

    def _parse_price(self, price):
        if price:
            return float(price.replace('R ', ''))
        else:
            return None

    def _create_medicine(self, api_result):
        return Medicine(api_result.get('nappi_code'),
                        api_result.get('name'),
                        self.currency_code,
                        self._parse_price(api_result.get('sep')),
                        api_result.get('dispensing_fee'))

    def search(self, search_query):
        response = requests.get(path.join(self.url, 'search-lite'),
                                params={'q': search_query})
        if response:
            return [self._create_medicine(result) for result in response.json()]
        else:
            response.raise_for_status()

    def get(self, id):
        response = requests.get(path.join(self.url, 'detail'), params={'nappi': id})

        if response:
            return self._create_medicine(response.json())
        else:
            response.raise_for_status()

# TODO - limit responses/pagination
# TODO - handle the 'no results because search term too short' challenge (maybe with a flash?)
# TODO - Forex pieces