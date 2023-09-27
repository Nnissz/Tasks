import requests
import json
from config import keys

class ConvertionException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        try:
            sum = round(float(amount) * float(CryptoConverter.convert(quote, base, amount)), 2)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount} ')

        return sum

    @staticmethod
    def convert(quote: str, base: str, amount: str):

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote} ')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base} ')

        if quote == base:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}.')

        # try:
        #     amount = float(amount)
        # except ValueError:
        #     raise ConvertionException(f'Не удалось обработать количество {amount} ')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base