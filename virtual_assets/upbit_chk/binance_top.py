from time import sleep
import requests
import sys, datetime
from win10toast import ToastNotifier


ep = 'https://api.binance.com'
ping = '/api/v1/ping'
ticker24h = '/api/v1/ticker/24hr'


def get_ohlc_binance(t):
    params = {'symbol': t + 'USDT'}
    _ = requests.get(ep+ping)
    r2 = requests.get(ep+ticker24h, params=params)

    return float(r2.json()['openPrice']), float(r2.json()['lastPrice']), float(r2.json()['priceChangePercent'])


def main(argv):
    tickers = ['BTC', 'ETH', 'XRP']
    mons = [20000.0, 1000.0, 0.3]

    while 1:
        cur = datetime.datetime.now().strftime('%H:%M:%S')
        i = 0
        for t in tickers:
            open_price, last_price, chang_per = get_ohlc_binance(t)
            print(cur, t, open_price, last_price, f'{chang_per:.2f}%')

            lp = float(last_price)
            if lp < mons[i]:
                toaster = ToastNotifier()
                toaster.show_toast("Toast Notifier", f' {t:<6}' + ' Stop Loss. ' + f'{lp:4.2f}')

            i += 1

        sleep(10)
        print()


if __name__ == "__main__":
    main(sys.argv)
