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
import json
import jwt
import hashlib
import os
import requests
import uuid
from urllib.parse import urlencode, unquote

symbols = []
usd = 1270
noti = 'no'

server_url = "https://api.upbit.com"

class item:
    def __init__(self, ticker, base, count):
        self.ticker = ticker
        self.base = base
        self.count = count

def load_key():
    global g_access, g_secret
    with open("C:\\Temp\\ub_api_key.json") as f:
        setting_loaded = json.loads(f.read())

    # Upbit
    access_key = setting_loaded["access_key"]
    secret_key = setting_loaded["secret_key"]
    pyupbit.Upbit(access_key, secret_key)

    return access_key, secret_key

## monitoring data
def load_mon_item():
    file = open("C:\\Temp\\mon_tickers.json")
    data = json.load(file)
    for key, val in data.items():
        df = pyupbit.get_ohlcv('KRW-' + key.upper(), count=1)

        if df is None:
            open_price = 100.0
        else:    
            open_price = float(df['open'][0])

        symbols.append(item(
            'KRW-' + key.upper(), 
            open_price, 
            float(val)
            ))

def unixtime_to_str(unixtime):
    time_obj = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(unixtime))
    return time_obj

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

    print(cur + ' (' + f'{btc_rate:5.2f}, {cur_rate:6.2f}' + ' ) ' \
          + f'{v[4:]:<6}: {base:12.2f}, {p:12.2f}, ' \
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
    print(f'{cur} ({btc_rate:5.2f}, {cur_rate:6.2f}) ' \
          f'{v[4:]:<6} : {base:12.2f}, {p:12.2f}, ' \
          f'{pcnt:6.2f}%, {amt:10.2f}, ' + (format(int(tot), ',d')  if cnt != 1 else '0'))

    if cnt == 1:
        return 0, 0
    else:
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


def get_my_account(akey, skey):
    payload = {
    'access_key': akey,
    'nonce': str(uuid.uuid4()),
    }

    jwt_token = jwt.encode(payload, skey)
    authorization = 'Bearer {}'.format(jwt_token)
    headers = {
    'Authorization': authorization,
    }

    res = requests.get(server_url + '/v1/accounts', headers=headers)

    cash = 0.0 
    va_items = res.json()
    for va in va_items:
        if va['currency'] == 'KRW':
            cash = float(va['balance']) + float(va['locked'])
            continue
        if float(va['avg_buy_price']) <= 0.0:
            continue
        
        symbols.append(item(
            va['unit_currency'] + '-' + va['currency'], 
            float(va['avg_buy_price']), 
            float(va['balance']) +float(va['locked'])
            ))
    return cash

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

    usd = upbit_get_usd_krw()
    fng = get_fng()

    akey, skey = load_key()
    cash = get_my_account(akey, skey)
    load_mon_item()
 
    binance = ccxt.binance()

    while True:
        amt = 0.0
        mgn = 0.0
        usd = upbit_get_usd_krw()
        btc_rate, btc_price = rate('KRW-BTC')

        item_count = 0
        for itm in symbols:
            if itm.ticker.startswith('BTC-'):
                t_mgn, t_amt = check_btc_ticker(itm.ticker, btc_rate, btc_price, itm.base, itm.count)
            else:
                t_mgn, t_amt = check_krw_ticker(itm.ticker, btc_rate, itm.base, itm.count)

            if t_mgn is None or t_amt is None:
                continue
            item_count += 1
            mgn += t_mgn
            amt += t_amt
            time.sleep(0.2)

        pcnt = (mgn / (amt + cash)) * 100.0

        btc_ohlcv = binance.fetch_ohlcv('BTC/USDT', timeframe='1d', limit=1)
        btc_price = btc_ohlcv[-1][4]
        btc_rate = ((btc_ohlcv[-1][4] / btc_ohlcv[-1][1]) - 1.0) * 100.0

        print(f'fng: {fng}, earn: {mgn:.0f}, {pcnt:.2f}%,',
            f'BTC: ${btc_price:.2f} (${btc_rate:.2f}%),',
            f'cash, {int(cash):,d}, total {int(amt + cash):,d}')

        if 0 < item_count:
            print()

        time.sleep(sleep_sec)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit_gracefully)
    main(sys.argv)
