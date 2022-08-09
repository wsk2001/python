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


open_p = 0
high_p = 1
low_p = 2
close_p = 3


def ohlcv(v):
    usd = 1.0
    price = 1.0
    btc_ticker = False
    if v.upper().startswith("KRW-"):
        df = pyupbit.get_ohlcv(v, count=1440, interval="minute1")
    elif v.upper().startswith("BTC-"):
        df = pyupbit.get_ohlcv(v, count=1440, interval="minute1")
        btc_ticker = True
        usd = upbit_get_usd_krw()
        _, price = get_binance_btc('BTC')

    else:
        df = pyupbit.get_ohlcv("KRW-" + v, count=1440, interval="minute1")

    values = df.values.tolist()
    indexs = df.index.tolist()
    current_time = datetime.datetime.now()
    cur_date = current_time.strftime("%Y-%m-%d")

    open_v = 0
    for i in range(len(values)):
        chk_date = indexs[i].strftime("%Y-%m-%d")
        if chk_date == cur_date:
            if open_v == 0:
                open_v = values[i][open_p]
            rate = ((values[i][close_p] / open_v) - 1) * 100.0
            print(v + ',', indexs[i].strftime("%Y-%m-%d %H:%M:%S") + ',', values[i][open_p], values[i][close_p], f'{rate:.3f}%')


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

    ohlcv(ticker)


if __name__ == "__main__":
    main(sys.argv)
