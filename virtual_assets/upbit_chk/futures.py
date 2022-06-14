import time
import datetime
import sys, getopt, signal
import pyupbit
from common.utils import get_binance_btc, get_fng
from common.utils import upbit_get_usd_krw
from common.dominance import get_dominance
import requests
import json

item_list = []

usd = 1270

class item:
    def __init__(self, ticker, enter, count, pay_off, magn):
        self.ticker = ticker
        self.enter = enter
        self.count = count
        self.pay_off = pay_off
        self.magn = magn

def exit_gracefully(signal, frame):
    sys.exit(0)


def get_binance_btc_json(ticker, enter, count, pay_off, magn):
    ep = 'https://api.binance.com'
    ping = '/api/v1/ping'
    ticker24h = '/api/v1/ticker/24hr'

    params = {'symbol': ticker + 'USDT'}
    r1 = requests.get(ep + ping)
    r2 = requests.get(ep + ticker24h, params=params)

    cur = datetime.datetime.now().strftime('%H:%M:%S')
    open_price = float(r2.json()['openPrice'])
    close_price = float(r2.json()['lastPrice'])
    price_change = float(r2.json()['priceChangePercent'])
    # pcnt = (mgn / base) * 100.0

    cur_rate = ((close_price / enter) - 1.0) * 100.0 * count * magn
    cur_tot = (close_price - enter) * count

    # If short
    posi_short = False
    if enter < pay_off:
        cur_rate *= -1.0
        cur_tot *= -1.0
        posi_short = True

    if posi_short:
        print(cur + f' {ticker:<6}' + f' ({price_change:4.2f}%) S' + f' {count:6.4f}' + ', ' +
              f'{enter:6.2f}' + ', ' + f'{close_price:6.2f}' + ', ' + f'{pay_off:6.2f}' + ', ' +
              format(int(magn), ',d') + f' {cur_rate:4.2f}%' + ', ' + f'{cur_tot:4.2f}')
    else:
        print(cur + f' {ticker:<6}' + f' ({price_change:4.2f}%) L' + f' {count:6.4f}' + ', ' +
              f'{enter:6.2f}' + ', ' + f'{close_price:6.2f}' + ', ' + f'{pay_off:6.2f}' + ', ' +
              format(int(magn), ',d') + f' {cur_rate:4.2f}%' + ', ' + f'{cur_tot:4.2f}')


def main(argv):
    global usd
    inv_amt = 0.0
    sleep_sec = 5
    view_binance = False

    try:
        opts, etc_args = getopt.getopt(argv[1:], "hs:", ["sleep="])

    except getopt.GetoptError:
        print(argv[0], '-s <sleep seconds>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(argv[0], '-s <sleep seconds>')
            sys.exit()

        elif opt in ("-s", "--sleep"):  # upbit item symbol
            sleep_sec = int(arg.strip())

    file = open("futures.txt", "r")
    lines = file.readlines()
    cash = 0.0
    usd = upbit_get_usd_krw()
    fng = get_fng()

    for l in lines:
        line = l.strip()
        if not line:
            continue

        if line.startswith("#") or line.startswith("//"):
            continue

        if len(line) <= 0:
            continue

        strings = line.split()

        item_list.append(item(strings[0], float(strings[1]), float(strings[2]),float(strings[3]), float(strings[4][1:])))

    file.close()

    i = 0
    while True:
        i = 0
        for itm in item_list:
            get_binance_btc_json(itm.ticker, itm.enter, itm.count, itm.pay_off, itm.magn)
            i += 1
            time.sleep(0.1)

        time.sleep(sleep_sec)

        if 1 < i:
            print()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit_gracefully)
    main(sys.argv)
