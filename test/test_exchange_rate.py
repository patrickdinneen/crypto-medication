from unittest import TestCase
from exchange_rates import CoinDeskExchangeRateProvider, ExchangeRate, VolatilityCalculator
from datetime import date


class CoinDeskExchangeRateProviderTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.provider = CoinDeskExchangeRateProvider()

    def test_fetch_latest(self):
        value_date = date.today()
        exchange_rate = self.provider._fetch_latest_rate('ZAR', 'BTC', value_date)
        self.assertTrue(exchange_rate.rate > 1)
        self.assertEqual(exchange_rate.base_currency, 'ZAR')
        self.assertEqual(exchange_rate.target_currency, 'BTC')
        self.assertEqual(exchange_rate.date, value_date)

    def test_fetch_historic(self):
        value_date = date(2019, 9, 1)
        exchange_rate = self.provider._fetch_historic_rate('ZAR', 'BTC', value_date)
        self.assertTrue(exchange_rate.rate > 1)
        self.assertEqual(exchange_rate.base_currency, 'ZAR')
        self.assertEqual(exchange_rate.target_currency, 'BTC')
        self.assertEqual(exchange_rate.date, value_date)

    def test_only_btc_supported(self):
        self.assertRaises(ValueError, self.provider.get_exchange_rate, 'ZAR', 'ETH', date.today())


class ExchangeRateTestCase(TestCase):
    def test_convert(self):
        exchange_rate = ExchangeRate('ABC', 'DEF', date.today(), 0.5)
        self.assertEqual(exchange_rate.convert_base_to_target(20), 40)


class VolatilityCalculatorTestCase(TestCase):
    def test_volatility(self):
        self.assertEqual(VolatilityCalculator.calculateRelativeChange(price=1, reference_price=2).volatility, -50,
                         'price is 50% less than the reference price')
        self.assertEqual(VolatilityCalculator.calculateRelativeChange(price=200, reference_price=100).volatility, 100,
                         'price is 100% more than the reference price')
