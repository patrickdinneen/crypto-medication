from flask import Flask, render_template, request
from medicine import MedicineRegistry
from exchange_rates import CoinDeskExchangeRateProvider, VolatilityCalculator
from datetime import timedelta, date

app = Flask('crypto-medication')
medicine_registry = MedicineRegistry()
exchange_rate_provider = CoinDeskExchangeRateProvider()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/medicine/search', methods=['GET'])
def search_medicines():
    search_query = request.args.get('query')
    medicines = medicine_registry.search(search_query)
    return render_template('search_results.html', medicines=medicines)


@app.route('/medicine/<id>/volatility', methods=['GET'])
def medicine_price_volatility(id, target_currency='BTC'):
    medicine = medicine_registry.get(id)
    valuation_dates = get_valuation_dates()
    valuation_rates = [exchange_rate_provider.get_exchange_rate(medicine.currency_code, target_currency, d)
                       for d in valuation_dates]
    target_prices = [rate.convert_base_to_target(medicine.total_cost()) for rate in valuation_rates]
    volatility = [VolatilityCalculator.calculateRelativeChange(price, target_prices[0]) for price in target_prices]
    target_price_volatility = zip(valuation_dates, volatility)

    return render_template('medicine_volatility.html',
                           medicine=medicine,
                           valuation_rates=dict(zip(valuation_dates, valuation_rates)),
                           target_price_volatility=target_price_volatility,
                           target_currency=target_currency)


def get_valuation_dates():
    today = date.today()
    timedeltas = [timedelta(days=0),
                  timedelta(days=1),
                  timedelta(weeks=1),
                  timedelta(days=30),
                  timedelta(days=365),
                  timedelta(days=365 * 5)]
    return [today - delta for delta in timedeltas]


if __name__ == '__main__':
    app.run(host='0.0.0.0')
