from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
    'start': '1',
    'limit': '1',
    'convert': 'USD'
}
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '8fd0b0e4-a44e-4311-8468-ecaf68a810db',
}

# 'X-CMC_PRO_API_KEY': '408f9e2f-96b8-45fb-ae03-0cd552fda446'
# https://github.com/ky039/BTC-USDT-Dominance-Analysis/blob/main/USDT%20Market%20Dominance.ipynb

def get_dominance():
    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        jsonObject = json.loads(response.text)
        jsonArray = jsonObject.get("data")
        symbol = jsonArray[0]['symbol']
        price = jsonArray[0]['quote']['USD']['price']
        chg24 = jsonArray[0]['quote']['USD']['percent_change_24h']
        domi = jsonArray[0]['quote']['USD']['market_cap_dominance']

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    return symbol, price, chg24, domi

if __name__ == "__main__":
    get_dominance()
