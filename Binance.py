import pandas as pd
import requests
import json
import decimal
import hmac
import time
import hashlib

keys = {
    'api': YOUR_KEY_HERE
}

class Binance:
    def __init__(self):
        self.base = 'https://api.binance.us'

        self.endpoints = {
            "order": '/api/v3/order',
            "testOrder": '/api/v3/order/test',
            "allOrders": '/api/v3/allOrders',
            "klines": '/api/v3/klines',
            "exchangeInfo": '/api/v3/exchangeInfo'
        }

        self.headers = {
            "X-MBX-APIKEY": keys['api']
        }

    # get symbols with selected quote asset from Binance
    def get_trading_symbols(self, quote_assets:list = None):
        url = self.base + self.endpoints["exchangeInfo"]

        print('Getting symbols from Binance...', flush = True)
        try:
            response = requests.get(url)
            data = json.loads(response.text)
        except Exception as e:
            print("Failed to access " + url)
            return []

        symbols = []

        for pair in data['symbols']:
            if pair['status'] == 'TRADING':
                if quote_assets is not None and pair['quoteAsset'] in quote_assets:
                    symbols.append(pair['symbol'])

        print('Symbols trading: ' + str(len(symbols)))

        return symbols

    # get price data for symbol from Binance
    def get_symbol_data(self, symbol:str, interval:str):
        params = '?&symbol=' + symbol + '&interval=' + interval

        url = self.base + self.endpoints['klines'] + params
        data = requests.get(url)

        dictionary = json.loads(data.text)
        df = pd.DataFrame.from_dict(dictionary)
        df = df.drop(range(6, 12), axis = 1)

        col_names = ['time', 'open', 'high', 'low', 'close', 'volume']
        df.columns = col_names

        for col in col_names:
            df[col] = df[col].astype(float)

        df['date'] = pd.to_datetime(df['time'] * 1000000, infer_datetime_format = True)

        return df