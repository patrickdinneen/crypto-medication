import requests
from os import path

class Medicine(object):
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price

class MedicineRegistry(object):
    def __init__(self):
        self.url = 'https://mpr.code4sa.org/api/v2/'

    def search(self, search_query):
        response = requests.get(path.join(self.url, 'search-lite'),
                                params={'q': search_query})
        if response:
            return [Medicine(result['id'], result['name'], result['sep']) for result in response.json()]
        else:
            response.raise_for_status()

# TODO - limit responses/pagination
# TODO - handle the 'no results because search term too short' challenge (maybe with a flash?)
# TODO - Medicine construction method from results -> parse SEP into ZAR + amount
# TODO - Forex pieces