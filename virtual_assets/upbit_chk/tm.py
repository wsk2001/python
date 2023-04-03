#-*- coding:utf-8 -*-

import time
import datetime
import sys, getopt
import pyupbit
from time import sleep
import requests
from common.utils import market_code
from common.utils import upbit_get_usd_krw
from common.utils import get_binance_btc
from pandas import Series, DataFrame

def ohlcv(v):
    usd = 1.0
    price = 1.0
    btc_ticker = False
    if v.upper().startswith("KRW-"):
        df = pyupbit.get_ohlcv(v, count=1)
    elif v.upper().startswith("BTC-"):
        df = pyupbit.get_ohlcv(v, count=1)
        btc_ticker = True
        usd = upbit_get_usd_krw()
        _, price = get_binance_btc('BTC')

    else:
        df = pyupbit.get_ohlcv("KRW-" + v, count=1)

    o = df['open'][0] * usd * price
    h = df['high'][0] * usd * price
    l = df['low'][0] * usd * price
    c = df['close'][0] * usd * price
    r = ((c / o) - 1) * 100.0

    print(f'{o:.5f} ' + f'{h:.5f} ' + f'{l:.5f} ' + f'{c:.5f} ' + f'{r:.3f}%')


def main(argv):
    ticker = 'BTC'
    try:
        opts, etc_args = getopt.getopt(argv[1:], "ht:", ["ticker="])

    except getopt.GetoptError:
        print(argv[0], '-t <ticker>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(argv[0], '-i <item symbol> -b <base price>')
            sys.exit()

        elif opt in ("-t", "--ticker"):  # upbit item symbol
            ticker = arg

    # ticker 가 한글 일 경우 처리, ticker[0:3] 에서 [1:3] 으로 바꿈
    # 1inch 때문
    if not ticker[1:3].encode().isalpha():
        _, name_to_code, _ = market_code()
        ticker = name_to_code[ticker]
        print(ticker)
    else:
        if not ticker.upper().startswith('BTC-'):
            _, _, code_to_name = market_code()
            print(code_to_name['KRW-' + ticker.upper()])
    while 1:
        ohlcv(ticker)
        sleep(10)


if __name__ == "__main__":
    main(sys.argv)
