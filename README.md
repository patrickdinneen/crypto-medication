# crypto-medication
Crypto-Medication is a simple web app for viewing the volatility that would be experienced if consumers paid for their medication using cryptocurrencies.

### Requirements
Crypto-Medication requires Python 3.x

### Docker Installation
You can build a container by running:

```
docker build . -t crypto-med
```

This can then be run:

```
docker run -p 5000:5000 crypto-med
```

If you're feeling wild (not recommended) you can do both at the same time:

```
docker build . -t crypto-med && docker run -p 5000:5000 crypto-med
```

The server will be running on http://localhost:5000

### Virtualenv Installation
Create and activate a new virtual environment:

```
python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
```

Start the server:
```
./go.sh
```

The server will be running on http://localhost:5000

### Running tests
```
./run_tests.sh
```

