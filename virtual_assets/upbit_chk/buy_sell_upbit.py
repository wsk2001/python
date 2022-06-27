# -*- coding:utf-8 -*-

import time, sys, getopt, signal
import requests
import json
from common.utils import get_binance_btc
from common.dominance import get_dominance
import ccxt, cbpro, datetime

from tradingview_ta import TA_Handler, Interval, Exchange
import pyupbit


# Coinbase Index
def get_usdt_price():
    handler = TA_Handler(
        symbol="USDTUSD",
        screener="CRYPTO",
        exchange="KRAKEN",
        interval=Interval.INTERVAL_1_MINUTE
    )
    usdt = float(handler.get_analysis().indicators['close'])
    return usdt


def get_ta(symbol, screener, exchange, interval):
    return TA_Handler(
        symbol=symbol,
        screener=screener,
        exchange=exchange,
        interval=interval,
    ).get_analysis().summary


def earning(v):
    df = pyupbit.get_ohlcv('KRW-' + v, count=1)
    open_price = df['open'][0]
    close_price = df['close'][0]
    res = ((close_price / open_price) - 1.0) * 100.0
    return res, close_price


# Interval
# "1m", "5m", "15m", "30m", "1h", "2h", "4h", "1d", "1W", "1M"

def buy_sell_upbit(ticker, interval):
    dt = get_ta(ticker + "KRW", "CRYPTO", "UPBIT", interval)
    cur = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    earn, p = earning(ticker)
    recmd = dt['RECOMMENDATION']
    pr = "{:0,.3f}".format(p)
    print(cur + ': ' f'{ticker:<6}', f'{recmd:<10}', f'{str(dt["BUY"]):>4}',
          f'{str(dt["SELL"]):>4}', f'{str(dt["NEUTRAL"]):>4}', f'  {pr:>14}', f'{earn:6.2f}%')


def get_binance_price(ticker, interval):
    handler = TA_Handler(
        symbol=ticker + "USDT",
        screener="CRYPTO",
        exchange="Binance",
        interval=interval
    )
    print(handler.get_analysis().indicators)


def buy_sell_binance(ticker, interval):
    dt = get_ta(ticker + "USDT", "CRYPTO", "Binance", interval)
    cur = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    op_btc, price = get_binance_btc(ticker)
    earn = ((price / op_btc) - 1.0) * 100.0
    p = price
    recmd = dt['RECOMMENDATION']
    pr = "{:0,.3f}".format(p)
    print(cur + ': ' f'{ticker:<6}', f'{recmd:<10}', f'{str(dt["BUY"]):>4}',
          f'{str(dt["SELL"]):>4}', f'{str(dt["NEUTRAL"]):>4}', f'  {pr:>14}', f'{earn:6.2f}%')


def usage(app):
    print(app, '-s <sleep seconds> -i <interval> -f <filename> -b [binance]')
    print('')
    print('interval')
    print('\t1m  \tInterval 1 minute')
    print('\t5m  \tInterval 5 minutes')
    print('\t15m \tInterval 15 minutes')
    print('\t30m \tInterval 30 minutes')
    print('\t1h  \tInterval 1 hour')
    print('\t2h  \tInterval 2 hours')
    print('\t4h  \tInterval 4 hours')
    print('\t1d  \tInterval 1 day')
    print('\t1W  \tInterval 1 week')
    print('\tall  \tInterval all-1m ~ 1d')
    print('\t1M  \tInterval 1 month(X)')
    sys.exit()


def main(argv):
    sleep_sec = 10.0
    interval = "5m"
    filename = ''
    binance = 0
    symbols = []
    symbols.clear()

    try:
        opts, etc_args = getopt.getopt(argv[1:], "hs:i:f:b", ["sleep=", "interval=", "filename="])
    except getopt.GetoptError:
        usage(argv[0])

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage(argv[0])

        elif opt in ("-s", "--sleep"):
            sleep_sec = int(arg.strip())

        elif opt in ("-i", "--interval"):
            interval = arg.strip()

        elif opt in ("-f", "--filename"):
            filename = arg.strip()

        elif opt == '-b':
            binance = 1

    if len(filename) <= 0:
        lst = pyupbit.get_tickers(fiat="KRW")
        for v in lst:
            symbols.append(v[4:])
    else:
        file = open(filename, "r", encoding='UTF8')
        lines = file.readlines()

        for l in lines:
            line = l.strip()
            if not line:
                continue

            if line.startswith("#") or line.startswith("//"):
                continue

            if len(line) <= 0:
                continue

            strings = line.split()
            symbols.append(strings[0])

        file.close()

    while True:
        print('Interval: ' + interval)
        print('Date and Time        Symbol Urge        Buy  Sell Neut           Price   Fluctuation')

        for s in symbols:
            if binance:
                buy_sell_binance(s, interval)
            else:
                buy_sell_upbit(s, interval)

            time.sleep(0.1)

        print('')
        time.sleep(sleep_sec)
        # break


def exit_gracefully(signal, frame):
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit_gracefully)
    main(sys.argv)
