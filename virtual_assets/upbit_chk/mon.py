# -*- coding: utf-8 -*-

import time
import datetime
import sys, getopt, signal
import pyupbit
from common.utils import get_binance_btc, get_fng
from common.utils import upbit_get_usd_krw
from common.dominance import get_dominance
import requests
from common.dominance import aoa_position
from win10toast import ToastNotifier

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


def check_btc_ticker(v, btc_rate, base, cnt):
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
          + f'{v[4:]:<6}' + ': ' + f'{base:14.4f}' + ', ' + f'{p:14.4f}' + ', ' \
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
          + f'{v[4:]:<6}' + ': ' + f'{base:14.4f}' + ', ' + f'{p:14.4f}' + ', ' \
          + f'{pcnt:6.2f}%' + ', ' + f'{amt:10.2f}' + ', ' + format(int(tot), ',d'))

    return amt, tot


def check_krw_ticker(v, btc_rate, base, cnt, sl=0.0, tp=0.0):
    df = pyupbit.get_ohlcv(v, count=1)
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
              + f'{v[4:]:<6}' + ': ' + f'{base:14.4f}' + ', ' + f'{p:14.4f}' + ', ' \
              + f'{pcnt:6.2f}%' + ', ' + f'{amt:10.2f}' + ', ' + format(int(tot), ',d'))

        return 0, 0
    else:
        print(cur + ' (' + f'{btc_rate:5.2f}' + ', ' + f'{cur_rate:6.2f}' + ' ) ' \
              + f'{v[4:]:<6}' + ': ' + f'{base:14.4f}' + ', ' + f'{p:14.4f}' + ', ' \
              + f'{pcnt:6.2f}%' + ', ' + f'{amt:10.2f}' + ', ' + format(int(tot), ',d'))

        if noti == 'yes':
            if sl != 0.0 and amt < sl:
                toaster = ToastNotifier()
                toaster.show_toast("Toast Notifier",
                                   f' {v[4:]:<6}' + ' Stop loss ' + f'{amt:7.2f}' + ' (' + f'{p:14.2f}' + ')',
                                   duration=5)

            if tp != 0.0 and tp < amt:
                toaster = ToastNotifier()
                toaster.show_toast("Toast Notifier",
                                   f' {v[4:]:<6}' + ' Take profit ' + f'{amt:7.2f}' + ' (' + f'{p:14.2f}' + ')',
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
          + f'{v[4:]:<6}' + ': ' + f'{base:14.4f}' + ', ' + f'{p:14.4f}' + ', ' \
          + f'{pcnt:6.2f}%' + ', ' + f'{amt:10.2f}' + ', ' + format(int(tot), ',d'))


def main(argv):
    global usd, noti
    inv_amt = 0.0
    sleep_sec = 5
    view_binance = False

    try:
        opts, etc_args = getopt.getopt(argv[1:], "hs:bn", ["sleep="])

    except getopt.GetoptError:
        print(argv[0], '-s <sleep seconds> -b [vew binance]')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(argv[0], '-s <sleep seconds> -b [vew binance]')
            sys.exit()

        elif opt in ("-s", "--sleep"):
            sleep_sec = int(arg.strip())

        elif opt in "-b":
            view_binance = True

        elif opt in "-n":
            noti = 'yes'

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

        symbols.append(item(strings[0], float(strings[1]), float(strings[2]), float(strings[3]), float(strings[4])))

    file.close()

    usd = upbit_get_usd_krw()

    i = 0
    chg_posi = False
    disp_cnt = 0
    trader_posi = aoa_position()

    while True:
        amt = 0.0
        mgn = 0.0
        btc_rate, _ = rate('KRW-BTC')

        for itm in symbols:
            if itm.ticker.startswith('BTC-'):
                t_mgn, t_amt = check_btc_ticker(itm.ticker, btc_rate, itm.base, itm.count)
            else:
                t_mgn, t_amt = check_krw_ticker(itm.ticker, btc_rate, itm.base, itm.count, itm.sl, itm.tp)
            mgn += t_mgn
            amt += t_amt

        pcnt = (mgn / (amt + cash)) * 100.0

        if view_binance:
            mod = i % 100
            if mod == 0:
                _, _, _, domi = get_dominance()

            op_btc, price = get_binance_btc('BTC')
            chg24 = ((price / op_btc) - 1.0) * 100.0

            i += 1
            if 1000 <= i:
                i = 0

        if view_binance:
            print(f'fng: {fng}, earning: {mgn:.0f},', f'{pcnt:.2f}%,',
                  f' BTC: $' + format(price, ',.2f'), f'{chg24:.3f}', f'Domi {domi:.3f},',
                  'cash', format(int(cash), ',d'), ',total', format(int(amt + cash), ',d'))
        else:
            print(f'fng: {fng}, earning: {mgn:.0f},', f'{pcnt:.2f}%,',
                  'cash', format(int(cash), ',d'), ',total', format(int(amt + cash), ',d'))

        time.sleep(sleep_sec)
        tmp_posi = aoa_position()
        if not tmp_posi.startswith(trader_posi):
            trader_posi = tmp_posi
            chg_posi = True

        if 0 < chg_posi:
            toaster = ToastNotifier()
            toaster.show_toast("Position change:", trader_posi)
            disp_cnt += 1
            if 10 < disp_cnt:
                chg_posi = False
                disp_cnt = 0

        print()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit_gracefully)
    main(sys.argv)
