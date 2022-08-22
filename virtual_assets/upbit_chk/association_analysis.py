# -*- coding: utf-8 -*-

"""
연관성 분석 App
특정 종목이 주어진 % 이상 상승 했을때 전/후로 특정% 이상 상승한 종목을 이용해 연관성 분석.
1. 지정 옵션: symbol, 기간 10,000일, earn(원본 종목의 상승%), comp earn(비교하 종목들의 상승%)
2. 모든 종목들의 일간 상승률 저장 plus 인 경우만 저장. (일자, 상승%, symbol)
3.
"""

import time
import pyupbit
from datetime import datetime, date
from common.themes import get_themes, get_all_themes
from common.utils import get_idx_values, get_tickers
import argparse
import sqlite3
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


database_name = './dbms/upbit_days.db'


def make_from_to(date_time_str, days=5):
    date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d')

    from_date = date_time_obj - timedelta(days=days)
    to_date = date_time_obj + timedelta(days=days)

    str_from = from_date.strftime('%Y-%m-%d')
    str_to = to_date.strftime('%Y-%m-%d')

    return str_from, str_to


def create_table():
    global database_name

    conn = sqlite3.connect(database_name)
    conn.execute(
        'CREATE TABLE DAY_CANDLE(id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, open REAL, high REAL, low REAL, '
        'close REAL, volume REAL, earn REAL, symbol TEXT)')
    conn.close()


def insert_db():
    lst = get_tickers('KRW')

    conn = sqlite3.connect(database_name)
    cur = conn.cursor()
    id = 1

    for v in lst:
        ticker = v
        if not ticker.upper().startswith('KRW-'):
            ticker = 'KRW-' + v.upper()

        df = pyupbit.get_ohlcv(ticker, count=10000, period=1)
        for ind, row in df.iterrows():
            rc = ((row["close"] / row["open"]) - 1.0) * 100.0
            cur.execute("INSERT INTO DAY_CANDLE VALUES(?,?,?,?,?,?,?,?,?);",
                        (id, ind.strftime('%Y-%m-%d'), row["open"], row["high"], row["low"],
                         row["close"], row["volume"], rc, v[4:]))
            id += 1

        time.sleep(0.2)

    conn.commit()
    conn.close()


def analysis(v, e, r, p):
    ticker = v
    if not ticker.upper().startswith('KRW-'):
        ticker = 'KRW-' + v.upper()

    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    df = pyupbit.get_ohlcv(ticker, count=10000, period=1)
    for ind, row in df.iterrows():
        rc = ((row["close"] / row["open"]) - 1.0) * 100.0
        if e <= rc:
            base_date = ind.strftime('%Y-%m-%d')
            str_from, str_to = make_from_to(base_date, r)
            # print(str_from, str_to)

            sql = "select symbol from DAY_CANDLE dc" \
                  " WHERE" \
                  " 	'{start}' <= dc.date " \
                  " and dc.date <= '{end}'" \
                  " and '{pick}' <= earn" \
                  " group by symbol;".format(start=str_from, end=str_to, pick=p)
            cur.execute(sql)
            rows = cur.fetchall()
            # for ro in rows:
            #     print(ro)

            print(v, base_date, rows)

    cur.close()
    conn.close()

def main():
    # create_table()
    # insert_db()

    parser = argparse.ArgumentParser(description='옵션 지정 방법')
    parser.add_argument('--symbol', required=True, help='심볼 (BTC, ETH, ADA, ...)')
    parser.add_argument('--earning', required=False, default=10.0, help='실적 (5.1, 단위 %, default=10)')
    parser.add_argument('--range', required=False, default=5, help='비교 범위 기간(default=7, 앞/뒤로 7일)')
    parser.add_argument('--pick', required=False, default=5, help='비교 범위 (default=5, 5% 이상 상승 종목)')

    args = parser.parse_args()
    symbol = args.symbol
    earning = float(args.earning)
    r = int(args.range)
    p = float(args.pick)

    analysis(symbol, earning, r, p)


if __name__ == "__main__":
    main()


# py association_analysis.py --symbol=PUNDIX --earning=20 --range=3 --pick=20
