from time import sleep
import requests
import sys, datetime

ep = 'https://api.binance.com'
ping = '/api/v1/ping'
ticker24h = '/api/v1/ticker/24hr'


def get_ohlc_binance(t):
    params = {'symbol': t + 'USDT'}
    r1 = requests.get(ep+ping)
    r2 = requests.get(ep+ticker24h, params=params)
    # print(r2.json())

    return float(r2.json()['openPrice']), float(r2.json()['lastPrice']), float(r2.json()['priceChangePercent'])


def main(argv):
    # tickers = ['BTC', 'ETH', 'LTC', 'XLM', 'ADA', 'XRP']
    tickers = ['BTC', 'ETH', 'XRP']

    while 1:
        cur = datetime.datetime.now().strftime('%H:%M:%S')

        for t in tickers:
            open_price, last_price, chang_per = get_ohlc_binance(t)
            print(cur, t, open_price, last_price, f'{chang_per:.2f}%')

        sleep(10)
        print()


if __name__ == "__main__":
    main(sys.argv)
