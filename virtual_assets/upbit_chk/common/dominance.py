from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from bs4 import BeautifulSoup
import requests


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


# 워뇨띠 포지션
def aoa_position():
    # sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
    # sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

    r = requests.get('https://www.bitsignal.me/indexw.php');

    soup = BeautifulSoup(r.content.decode('utf-8', 'replace'), 'html.parser')
    str0 = soup.prettify()
    idx = str0.find('<td class="one">')
    str1 = str0[idx:idx + 300]
    strs = str1.splitlines()

    str_out = ''
    for s in strs:
        if s.strip().startswith('<'):
            continue
        else:
            str_out = str_out + ' ' + s.strip()

    return str_out.strip()


if __name__ == "__main__":
    print(get_dominance())
    print(aoa_position())

