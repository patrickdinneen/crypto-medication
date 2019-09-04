import requests
from collections import defaultdict, namedtuple
from os import path
from abc import ABC, abstractmethod

class ExchangeRate(object):
    def __init__(self, base_currency, target_currency, date, rate):
        self.base_currency = base_currency
        self.target_currency = target_currency
        self.date = date
        self.rate = rate

    def convert_base_to_target(self, amount):
        return amount/self.rate


class ExchangeRateProvider(ABC):
    @abstractmethod
    def get_exchange_rate(self, base_currency, target_currency, date):
        pass


class CoinDeskExchangeRateProvider(ExchangeRateProvider):
    def __init__(self):
        self.historic_url = 'https://api.coindesk.com/v1/bpi/historical/close.json'
        self.latest_url = 'https://api.coindesk.com/v1/bpi/currentprice/'
        self.cached_results = defaultdict(dict)
        self.supported_target_currencies = ['BTC']

    def get_exchange_rate(self, base_currency, target_currency, date):
        cached_result = self._get_cached_result(base_currency, target_currency, date)
        if cached_result:
            return cached_result
        else:
            return self._fetch_rate(base_currency, target_currency, date)

    def _get_cached_result(self, base_currency, target_currency, date):
        currency_pair_rates = self.cached_results[self._create_cache_key(base_currency, target_currency)]
        return currency_pair_rates.get(date)

    def _create_cache_key(self, base_currency, target_currency):
        return '{base}_{target}'.format(base=base_currency, target=target_currency)

    def _fetch_rate(self, base_currency, target_currency, date):
        if target_currency not in self.supported_target_currencies:
            raise ValueError('Currency code: {} not supported by provider'.format(target_currency))

        if date == date.today():
            exchange_rate = self._fetch_latest_rate(base_currency, target_currency, date)
        else:
            exchange_rate = self._fetch_historic_rate(base_currency, target_currency, date)

        self._cache_rate(exchange_rate)
        return exchange_rate

    def _fetch_historic_rate(self, base_currency, target_currency, date):
        date_string = date.strftime('%Y-%m-%d')
        response = requests.get(self.historic_url, params={'start': date_string, 'end': date_string, 'currency': base_currency})

        if response:
            rate = response.json()['bpi'][date_string]
            return ExchangeRate(base_currency, target_currency, date, rate)
        else:
            response.raise_for_status()

    def _cache_rate(self, exchange_rate):
        currency_pair_rates = self.cached_results[self._create_cache_key(exchange_rate.base_currency, exchange_rate.target_currency)]
        currency_pair_rates[exchange_rate.date] = exchange_rate

    def _fetch_latest_rate(self, base_currency, target_currency, date):
        response = requests.get(path.join(self.latest_url, base_currency, 'JSON'))

        if response:
            rate = response.json()['bpi'][base_currency]['rate_float']
            return ExchangeRate(base_currency, target_currency, date, rate)
        else:
            response.raise_for_status()


PriceVolatility = namedtuple('PriceVolatility', 'price volatility')

class VolatilityCalculator(object):
    @staticmethod
    def calculateRelativeChange(price, reference_price):
        return PriceVolatility(price, (price - reference_price)/reference_price*100)