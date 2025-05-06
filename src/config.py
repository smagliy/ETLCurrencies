import os


class APIConfig:
    BASE_API_URL = 'https://openexchangerates.org/api/'
    HISTORICAL_ENDPOINT = 'historical/'
    DAILY_ENDPOINT = 'latest.json'
    PARAMS = {'app_id': os.environ['APP_ID'], 'base': 'USD', 'symbols': 'EUR,GBP,USD,UAH'}


