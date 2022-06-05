import json
import requests
from config import *


class ExchangeException(Exception):
    pass


class Exchange:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise ExchangeException(f'одинаковые валюты {base}.')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ExchangeException(f'нет такой валюты {quote}.')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise ExchangeException(f'нет такой валюты {base}.')
        try:
            amount = int(amount)
        except ValueError:
            raise ExchangeException(f'нет такого количества {amount}.')
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        total_base = float(json.loads(r.content)[keys[quote]])
        return total_base
