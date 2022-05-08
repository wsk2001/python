from time import sleep
import requests

ep = 'https://api.binance.com'
ping = '/api/v1/ping'
ticker24h = '/api/v1/ticker/24hr'
exchange_rate = 1186

def get_ohlc(t):
    params = {'symbol': t + 'USDT'}
    r1 = requests.get(ep+ping)
    r2 = requests.get(ep+ticker24h, params=params)

    return float(r2.json()['openPrice']), float(r2.json()['lastPrice'])


while 1:
    tickers = ['BTC', 'ETH', 'CHZ', 'FIL', 'ADA', 'IOST']
    # tickers = ['BTC', 'ETH', 'IOST']
    for t in tickers:
        open_price, last_price = get_ohlc(t)
        cur_rate = ((last_price / open_price) - 1.0) * 100.0
        print(t, last_price,  f'{cur_rate:.3f}', last_price * exchange_rate)

    sleep(10)
    print()



