import json
import alpaca_trade_api as trade_api

API_KEY_ID, SECRET_KEY, ENDPOINT = '', '', ''
ALPACA_PAPER = True

with open('api_key.json') as f:
    d = json.load(f)
    API_KEY_ID = d['API_KEY_ID']
    SECRET_KEY = d['SECRET_KEY']
    ENDPOINT = d['ENDPOINT']

print(API_KEY_ID, " ", SECRET_KEY, " ", ENDPOINT)

API = trade_api.REST(API_KEY_ID, SECRET_KEY, base_url=ENDPOINT)
account = API.get_account()
API.list_positions()
