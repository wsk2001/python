# -*- coding: utf-8 -*-

"""
연관성 분석 App
특정 종목이 주어진 % 이상 상승 했을때 전/후로 특정% 이상 상승한 종목을 이용해 연관성 분석.
1. 지정 옵션: symbol, 기간 10,000일, earn(원본 종목의 상승%), comp earn(비교하 종목들의 상승%)
2. 모든 종목들의 일간 상승률 저장 plus 인 경우만 저장. (일자, 상승%, symbol)
3.
"""

import time, sys
import pyupbit
from datetime import datetime, date
from common.themes import get_themes, get_all_themes
from common.utils import get_idx_values, get_tickers
import argparse
import sqlite3
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import requests
from ast import literal_eval
import pandas as pd
import ccxt

def get_binance_ohlcv(ticker, count=1):
    binance = ccxt.binance()
    ohlcv = binance.fetch_ohlcv(ticker.upper() + '/USDT', timeframe='1d', limit=count)
    o = 0
    h = 0
    l = 0
    c = 0

    start_flag = True

    for v in ohlcv:
        if start_flag == True:
            o = v[1]
            h = v[2]
            l = v[3]
            c = v[4]
            start_flag = False
        else :
            if h < v[2]:
                h = v[2]
            if l > v[3]:
                l = v[3]

        c = v[4]

    return o, h, l, c

def pp_traditional(high, low, close):
    PP = (high + low + close) / 3
    R1 = PP * 2 - low
    S1 = PP * 2 - high
    R2 = PP + (high - low)
    S2 = PP - (high - low)
    R3 = PP * 2 + (high - 2 * low)
    S3 = PP * 2 - (2 * high - low)
    R4 = PP * 3 + (high - 3 * low)
    S4 = PP * 3 - (3 * high - low)
    R5 = PP * 4 + (high - 4 * low)
    S5 = PP * 4 - (4 * high - low)

    return round(PP,2), round(R1,2), round(R2,2), round(R3,2), round(R4,2), round(R5,2), round(S1,2), round(S2,2), round(S3,2), round(S4,2), round(S5,2)

def pp_fibonacci(high, low, close):
    PP = (high + low + close) / 3
    R1 = PP + 0.382 * (high - low)
    S1 = PP - 0.382 * (high - low)
    R2 = PP + 0.618 * (high - low)
    S2 = PP - 0.618 * (high - low)
    R3 = PP + (high - low)
    S3 = PP - (high - low)

    return round(PP,2), round(R1,2), round(R2,2), round(R3,2), round(S1,2), round(S2,2), round(S3,2)

def main(argv):
    parser = argparse.ArgumentParser(description='옵션 지정 방법')
    parser.add_argument('--high', required=False, default=518, help='high price')
    parser.add_argument('--low', required=False, default=453, help='low price')
    parser.add_argument('--close', required=False, default=468, help='close price')

    args = parser.parse_args()
    h = float(args.high)
    l = float(args.low)
    c = float(args.close)

    _, h, l, c = get_binance_ohlcv('btc', 2)

    print(get_binance_ohlcv('btc', 2))

    print(pp_traditional(h, l, c))
    print(pp_fibonacci(h, l, c))



if __name__ == "__main__":
    main(sys.argv)

# command line 에서 sqlite3 script 호출 하는 방법
# $ sqlite3.exe auction.db < work_script.sql

# py association_analysis.py --symbol=PUNDIX --earning=20 --range=3 --pick=20
