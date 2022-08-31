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

database_name = './dbms/virtual_asset.db'


def wlog(v1, v2, v3, v4):
    f = open("./dbms/association_analysys.txt", 'a')
    data = v1 + v2 + v3 + v4 + '\n'
    f.write(data)
    f.close()


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
        'CREATE TABLE day_candle(date TEXT, open REAL, high REAL, low REAL, '
        'close REAL, volume REAL, hearn REAL, learn REAL, earn REAL, symbol TEXT)')
    conn.close()


def insert_db():
    lst = get_tickers('KRW')

    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    for v in lst:
        ticker = v
        if not ticker.upper().startswith('KRW-'):
            ticker = 'KRW-' + v.upper()
        print(ticker)

        df = pyupbit.get_ohlcv(ticker, count=10000, period=1)
        for ind, row in df.iterrows():
            earn = ((row["close"] / row["open"]) - 1.0) * 100.0
            high = ((row["high"] / row["open"]) - 1.0) * 100.0
            low = ((row["low"] / row["open"]) - 1.0) * 100.0
            cur.execute("INSERT INTO day_candle VALUES(?,?,?,?,?,?,?,?,?,?);",
                        (ind.strftime('%Y-%m-%d'), row["open"], row["high"], row["low"],
                         row["close"], row["volume"], high, low, earn, v[4:]))

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

            sql = "select symbol from day_candle dc" \
                  " WHERE" \
                  " 	'{start}' <= dc.date " \
                  " and dc.date <= '{end}'" \
                  " and '{pick}' <= earn" \
                  " and '{ticker}' not like dc.symbol" \
                  " group by symbol;" \
                .format(start=str_from, end=str_to, pick=p, ticker=ticker[4:].upper())
            cur.execute(sql)
            rows = cur.fetchall()
            str_items = ''
            i = 0
            if 0 < len(rows):
                for ro in rows:
                    if i == 0:
                        str_items = str_items + ro[0]
                    else:
                        str_items = str_items + ',' + ro[0]
                    i += 1

                print(v + ',', str(round(rc, 2)) + '%,', base_date + ',', str_items)
                wlog(v + ',', str(round(rc, 2)) + '%,', base_date + ',', str_items)
            else:
                continue
    cur.close()
    conn.close()


def bond_strength(v, e, r, p):
    ticker = v
    if not ticker.upper().startswith('KRW-'):
        ticker = 'KRW-' + v.upper()

    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    dictionary = {}
    dictionary.clear()
    detect_count = 0
    df = pyupbit.get_ohlcv(ticker, count=10000, period=1)
    for ind, row in df.iterrows():
        rc = ((row["close"] / row["open"]) - 1.0) * 100.0
        if e <= rc:
            base_date = ind.strftime('%Y-%m-%d')
            str_from, str_to = make_from_to(base_date, r)
            str_from = base_date

            sql = "select symbol from day_candle dc" \
                  " WHERE" \
                  " 	'{start}' <= dc.date " \
                  " and dc.date <= '{end}'" \
                  " and '{pick}' <= earn" \
                  " and '{ticker}' not like dc.symbol" \
                  " group by symbol;" \
                .format(start=str_from, end=str_to, pick=p, ticker=ticker[4:].upper())
            cur.execute(sql)
            rows = cur.fetchall()

            if 0 < len(rows):
                detect_count += 1
                for ro in rows:
                    key = ro[0]
                    value = dictionary.__contains__(key)
                    if value:
                        iv = dictionary[key]
                        iv += 1
                        dictionary[key] = iv
                    else:
                        value = 1
                        dictionary[key] = value
            else:
                continue
    print(ticker[4:], detect_count)

    for k, val in dictionary.items():
        if 2 <= val:
            dval = round(val/detect_count, 4)*100.0
            if 30.0 <= dval:
                print(k+',', str(val)+',',f'{dval:4.2f}', '(%)')
    print()

    cur.close()
    conn.close()


# 거래소 table 의 data 를 동기화 한다.
def sync_exchange_data(v, sync_date, cur):
    ticker = v
    if not ticker.upper().startswith('KRW-'):
        ticker = 'KRW-' + v.upper()

    df = pyupbit.get_ohlcv(ticker, count=1, to=sync_date, period=1)
    earn = hearn = learn =ov = hv = lv = cv = vv = 0.0

    for ind, row in df.iterrows():
        earn = ((row["close"] / row["open"]) - 1.0) * 100.0
        hearn = ((row["high"] / row["open"]) - 1.0) * 100.0
        learn = ((row["low"] / row["open"]) - 1.0) * 100.0
        ov = row["open"]
        hv = row["high"]
        lv = row["low"]
        cv = row["close"]
        vv = row["volume"]
        break

    cur.execute("UPDATE day_candle    "
                "SET open = ?,	      "
                "        high = ?,    "
                "        low = ?,     "
                "        close = ?,   "
                "        volume = ?,  "
                "        hearn = ?,   "
                "        learn = ?,   "
                "        earn = ?     "
                "WHERE		          "
                "        date = ?     "
                "AND symbol = ?	      ",
                (ov, hv, lv, cv, vv, hearn, learn, earn, sync_date, ticker[4:]))


def sync_data(sync_date):
    lst = get_tickers('KRW')

    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    for v in lst:
        ticker = v
        sync_exchange_data(ticker, sync_date, cur)
        time.sleep(0.3)

    cur.close()
    conn.close()


def main():
    # create_table()
    # insert_db()

    parser = argparse.ArgumentParser(description='옵션 지정 방법')
    parser.add_argument('--symbol', required=True, help='심볼 (BTC, ETH, ADA, ...)')
    parser.add_argument('--earning', required=False, default=10.0, help='실적 (5.1, 단위 %, default=10)')
    parser.add_argument('--range', required=False, default=7, help='비교 범위 기간(default=7, 7일 이내)')
    parser.add_argument('--pick', required=False, default=5, help='비교 범위 (default=5, 5% 이상 상승 종목)')

    args = parser.parse_args()
    symbol = args.symbol
    earning = float(args.earning)
    r = int(args.range)
    p = float(args.pick)

    # sync_data('2022-08-22')

    if symbol.upper().startswith('ALL'):
        lst = get_tickers('KRW')
        for v in lst:
            bond_strength(v[4:], earning, r, p)
            # analysis(v[4:], earning, r, p)
    else:
        ticker = symbol
        bond_strength(ticker, earning, r, p)
        # analysis(ticker, earning, r, p)


if __name__ == "__main__":
    main()

# py association_analysis.py --symbol=PUNDIX --earning=20 --range=3 --pick=20
