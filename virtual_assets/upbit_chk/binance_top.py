from time import sleep
import requests

ep = 'https://api.binance.com'
ping = '/api/v1/ping'
ticker24h = '/api/v1/ticker/24hr'


def get_ohlc_binance(t):
    params = {'symbol': t + 'USDT'}
    r1 = requests.get(ep+ping)
    r2 = requests.get(ep+ticker24h, params=params)
    # print(r2.json())

    return float(r2.json()['openPrice']), float(r2.json()['lastPrice']), float(r2.json()['priceChangePercent'])


while 1:
    tickers = ['BTC', 'ETH', 'LTC', 'XLM', 'ADA', 'XRP']
    for t in tickers:
        open_price, last_price, chang_per = get_ohlc_binance(t)
        print(t, open_price, last_price,  f'{chang_per:.2f}%')

    sleep(10)
    print()
