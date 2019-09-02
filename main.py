from flask import Flask, render_template, request
from medicine import MedicineRegistry

app = Flask('crypto-medication')
medicine_registry = MedicineRegistry()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()

@app.route('/medicine/search', methods=['POST'])
def search_medicines():
    search_query = request.form['query']
    medicines = medicine_registry.search(search_query)
    return render_template('search_results.html', medicines=medicines)

@app.route('/medicine/<id>/volatility', methods=['GET'])
def medicine_price_volatility(id):
    medicine = medicine_registry.get(id)
