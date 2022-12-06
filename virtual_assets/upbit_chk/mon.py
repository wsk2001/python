# -*- coding: utf-8 -*-

import time
import datetime
import sys, getopt, signal
import pyupbit
from common.utils import get_binance_btc, get_fng
from common.utils import upbit_get_usd_krw
from common.dominance import get_dominance
import requests
import ccxt
from win10toast import ToastNotifier
import argparse

symbols = []
usd = 1270
noti = 'no'


class item:
    def __init__(self, ticker, base, count, sl, tp):
        self.ticker = ticker
        self.base = base
        self.count = count
        self.sl = sl
        self.tp = tp


def what_day_is_it(date):
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    day = date.weekday()
    return days[day]


def exit_gracefully(signal, frame):
    sys.exit(0)


def check_btc_ticker(v, btc_rate, btc_price, base, cnt):
    df = pyupbit.get_ohlcv(v, count=1)
    p = df['close'][0] * btc_price
    cur_rate = ((df['close'][0] / df['open'][0]) - 1.0) * 100.0
    mgn = p - base
    amt = mgn * cnt
    tot = p * cnt
    pcnt = (mgn / base) * 100.0
    cur = datetime.datetime.now().strftime('%H:%M:%S')

    print(cur + ' (' + f'{btc_rate:5.2f}' + ', ' + f'{cur_rate:6.2f}' + ' ) ' \
          + f'{v[4:]:<6}' + ': ' + f'{base:12.2f}' + ', ' + f'{p:12.2f}' + ', ' \
          + f'{pcnt:6.2f}%' + ', ' + f'{amt:10.2f}' + ', ' + format(int(tot), ',d'))

    return amt, tot


def check_usdt_ticker(v, btc_rate, base, cnt):
    df = pyupbit.get_ohlcv(v, count=1)
    _, price = get_binance_btc('BTC')
    p = df['close'][0] * usd * price
    cur_rate = ((df['close'][0] / df['open'][0]) - 1.0) * 100.0
    mgn = p - base
    amt = mgn * cnt
    tot = p * cnt
    pcnt = (mgn / base) * 100.0
    cur = datetime.datetime.now().strftime('%H:%M:%S')

    print(cur + ' (' + f'{btc_rate:5.2f}' + ', ' + f'{cur_rate:6.2f}' + ' ) ' \
          + f'{v[4:]:<6}' + ': ' + f'{base:12.2f}' + ', ' + f'{p:12.2f}' + ', ' \
          + f'{pcnt:6.2f}%' + ', ' + f'{amt:10.2f}' + ', ' + format(int(tot), ',d'))

    return amt, tot


def check_krw_ticker(v, btc_rate, base, cnt, sl=0.0, tp=0.0):
    df = pyupbit.get_ohlcv(v, count=1)
    if df is None:
        return None, None
    p = df['close'][0]
    cur_rate = ((df['close'][0] / df['open'][0]) - 1.0) * 100.0
    mgn = p - base
    amt = mgn * cnt
    tot = p * cnt
    pcnt = (mgn / base) * 100.0
    cur = datetime.datetime.now().strftime('%H:%M:%S')

    # monitoring ticker
    if cnt == 1:
        tot = 0.0
        print(cur + ' (' + f'{btc_rate:5.2f}' + ', ' + f'{cur_rate:6.2f}' + ' ) ' \
              + f'{v[4:]:<6}' + ': ' + f'{base:12.2f}' + ', ' + f'{p:12.2f}' + ', ' \
              + f'{pcnt:6.2f}%' + ', ' + f'{amt:10.2f}' + ', ' + format(int(tot), ',d'))

        return 0, 0
    else:
        print(cur + ' (' + f'{btc_rate:5.2f}' + ', ' + f'{cur_rate:6.2f}' + ' ) ' \
              + f'{v[4:]:<6}' + ': ' + f'{base:12.2f}' + ', ' + f'{p:12.2f}' + ', ' \
              + f'{pcnt:6.2f}%' + ', ' + f'{amt:10.2f}' + ', ' + format(int(tot), ',d'))

        if noti == 'yes':
            if sl != 0.0 and amt < sl:
                toaster = ToastNotifier()
                toaster.show_toast("Toast Notifier",
                                   f' {v[4:]:<6}' + ' Stop loss ' + f'{amt:7.2f}' + ' (' + f'{p:12.2f}' + ')',
                                   duration=5)

            if tp != 0.0 and tp < amt:
                toaster = ToastNotifier()
                toaster.show_toast("Toast Notifier",
                                   f' {v[4:]:<6}' + ' Take profit ' + f'{amt:7.2f}' + ' (' + f'{p:12.2f}' + ')',
                                   duration=5)

        return amt, tot


def rate(v):
    df = pyupbit.get_ohlcv(v, count=1)
    open_price = df['open'][0]
    close_price = df['close'][0]
    res = ((close_price / open_price) - 1.0) * 100.0
    return res, close_price


def get_binance_btc_json(t, btc_rate, base, cnt):
    ep = 'https://api.binance.com'
    ping = '/api/v1/ping'
    ticker24h = '/api/v1/ticker/24hr'

    params = {'symbol': t + 'USDT'}
    r1 = requests.get(ep + ping)
    r2 = requests.get(ep + ticker24h, params=params)

    cur = datetime.datetime.now().strftime('%H:%M:%S')
    open_price = float(r2.json()['openPrice'])
    close_price = float(r2.json()['lastPrice'])
    p = close_price - base
    mgn = p - base
    amt = mgn * cnt
    tot = p * cnt
    pcnt = (mgn / base) * 100.0

    cur_rate = ((close_price / open_price) - 1.0) * 100.0
    print(cur + ' (' + f'{btc_rate:5.2f}' + ', ' + f'{cur_rate:6.2f}' + ' ) ' \
          + f'{v[4:]:<6}' + ': ' + f'{base:12.2f}' + ', ' + f'{p:12.2f}' + ', ' \
          + f'{pcnt:6.2f}%' + ', ' + f'{amt:10.2f}' + ', ' + format(int(tot), ',d'))


def main(argv):
    global usd, noti
    inv_amt = 0.0
    sleep_sec = 5
    view_binance = False

    parser = argparse.ArgumentParser(description='옵션 지정 방법')
    parser.add_argument('--sleep', required=False, default=10, help='sleep sec (default=10)')
    parser.add_argument('--binance', required=False, default='yes', help='binance 지수 확인 (yes/no, default=yes)')
    parser.add_argument('--noti', required=False, default='no', help='over limit noti (yes/no default=no)')

    args = parser.parse_args()
    sleep_sec = int(args.sleep)
    noti = args.noti

    file = open("items.txt", "r", encoding='UTF8')
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
        if strings[0].upper().startswith('CASH'):
            cash = float(strings[1])
            continue

        inv_amt += float(strings[1]) * float(strings[2])
        if not strings[0].startswith('BTC-'):
            strings[0] = 'KRW-' + strings[0]

        # low_limit = float(strings[3])
        # upper_limit = float(strings[4])
        low_limit = -10000.0
        upper_limit = 10000.0

        symbols.append(item(strings[0], float(strings[1]), float(strings[2]), low_limit, upper_limit))

    file.close()

    binance = ccxt.binance()
    parameters = {
        'start': '1',
        'limit': '1',
        'convert': 'USD'
    }
    while True:
        amt = 0.0
        mgn = 0.0
        usd = upbit_get_usd_krw()
        btc_rate, btc_price = rate('KRW-BTC')

        for itm in symbols:
            if itm.ticker.startswith('BTC-'):
                t_mgn, t_amt = check_btc_ticker(itm.ticker, btc_rate, btc_price, itm.base, itm.count)
            else:
                t_mgn, t_amt = check_krw_ticker(itm.ticker, btc_rate, itm.base, itm.count, itm.sl, itm.tp)

            if t_mgn is None or t_amt is None:
                continue

            mgn += t_mgn
            amt += t_amt
            time.sleep(0.2)

        pcnt = (mgn / (amt + cash)) * 100.0

        btc_ohlcv = binance.fetch_ohlcv('BTC/USDT', timeframe='1d', limit=1)
        eth_ohlcv = binance.fetch_ohlcv('CHZ/USDT', timeframe='1d', limit=1)
        btc_price = btc_ohlcv[0][4]
        eth_price = eth_ohlcv[0][4]
        btc_rate = ((btc_ohlcv[0][4] / btc_ohlcv[0][1]) - 1.0) * 100.0
        etc_rate = ((eth_ohlcv[0][4] / eth_ohlcv[0][1]) - 1.0) * 100.0

        print(f'fng: {fng}, earn: {mgn:.0f},', f'{pcnt:.2f}%,',
            f' BTC: ${btc_price:.2f} (${btc_rate:.2f}%), CHZ(L) 0.1629: ${eth_price:.5f} ({etc_rate:.2f}%)',
            f'cash, {int(cash):,d}, total {int(amt + cash):,d}')

        print()
        time.sleep(sleep_sec)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit_gracefully)
    main(sys.argv)
