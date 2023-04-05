# -*- coding: utf-8 -*-

"""
연관성 분석 App
특정 종목이 주어진 % 이상 상승 했을때 전/후로 특정% 이상 상승한 종목을 이용해 연관성 분석.
1. 지정 옵션: symbol, 기간 10,000일, earn(원본 종목의 상승%), comp earn(비교하 종목들의 상승%)
2. 모든 종목들의 일간 상승률 저장 plus 인 경우만 저장. (일자, 상승%, symbol)
3.
"""

import sys, time
import pyupbit
from common.utils import get_idx_values, get_tickers
import argparse
import sqlite3
from datetime import datetime, timedelta
import requests
from ast import literal_eval
import pandas as pd
import ccxt

database_name = './dbms/virtual_asset.db'


def get_date(symbol, count, interval):
    ticker = symbol
    if not ticker.upper().startswith('KRW-'):
        ticker = 'KRW-' + symbol.upper()

    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    df = pyupbit.get_ohlcv(ticker, count=count, interval=interval, period=1)
    start_value = 0.0
    for ind, row in df.iterrows():
        ymd = ind.strftime('%Y-%m-%d')
        hms = ind.strftime('%H:%M:%S')

        earn = round(((row["close"] / row["open"]) - 1.0) * 100.0, 2)
        print(ticker[4:], ymd, hms, row["open"], row["close"], earn )
        cur.execute("INSERT INTO minute_candle VALUES(?,?,?,?,?,?);",
                        (ymd, hms, ticker[4:], row["open"], row["close"], earn))

    conn.commit()
    conn.close()


def delete_db(symbol):
    lst = get_tickers('KRW')

    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    sql = "DELETE FROM minute_candle WHERE symbol" + " = '" + symbol.upper() + "';"
    cur.execute(sql)

    conn.commit()
    conn.close()


def main(argv):
    parser = argparse.ArgumentParser(description='update minute table')
    parser.add_argument('--symbol', required=False, default='BTC', help='심볼 (default:BTC)')
    parser.add_argument('--interval', required=False, default='minute10', help='interval(minute60, default=minute10)')
    parser.add_argument('--count', required=False, default=1008, help='count of candle')

    args = parser.parse_args()
    symbol = args.symbol
    interval = args.interval
    count = int(args.count)

    delete_db(symbol)
    get_date(symbol, count, interval)

if __name__ == "__main__":
    main(sys.argv)
