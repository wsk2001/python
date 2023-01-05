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
import requests
from ast import literal_eval
import pandas as pd
import ccxt

database_name = './dbms/virtual_asset.db'

# 거래소 table 의 data 를 동기화 한다.
def theme_updata(market):
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    lst = get_tickers(market.upper())

    for v in lst:
        t = v
        if market.upper().startswith('USDT'):
            t = v[5:]
        else:
            t = v[4:]

        sql = " UPDATE coin_theme SET MARKET = ? WHERE SYMBOL = ?"
        data = ('UPBIT_' + market.upper(), t)

        print(sql, data)

        cur.execute(sql, data)
        conn.commit()

    cur.close()
    conn.close()

def sync_data(sync_date):

    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    for v in lst:
        ticker = v
        sync_exchange_data(ticker, sync_date, cur)
        time.sleep(0.3)

    cur.close()
    conn.close()


# 마켓코드조회
def market_code():
    url = "https://api.upbit.com/v1/market/all"
    querystring = {"isDetails": "false"}
    response = requests.request("GET", url, params=querystring)

    # 코인이름 - 마켓코드 매핑
    r_str = response.text
    r_str = r_str.lstrip('[')  # 첫 문자 제거
    r_str = r_str.rstrip(']')  # 마지막 문자 제거
    r_list = r_str.split("}")  # str를 }기준으로 쪼개어 리스트로 변환

    # name to code
    ntc = {}
    # code to name
    ctn = {}
    # code list
    cl = []

    for i in range(len(r_list) - 1):
        r_list[i] += "}"
        if i != 0:
            r_list[i] = r_list[i].lstrip(',')
        r_dict = literal_eval(r_list[i])  # element to dict

        temp_dict = {r_dict["market"]: r_dict["korean_name"]}
        ctn.update(temp_dict)  # 코드 - 코인이름 매핑
        temp_dict = {r_dict["korean_name"]: r_dict["market"]}
        ntc.update(temp_dict)  # 코인이름 - 코드 매핑
        cl.append(r_dict["market"])  # 코드 리스트

    return cl, ntc, ctn


def create_table():
    global database_name

    conn = sqlite3.connect(database_name)
    conn.execute(
        'CREATE TABLE month_candle(ym TEXT, symbol TEXT, o REAL, h REAL, l REAL, c REAL, v REAL)')
    conn.close()


def make_month_table():
    lst = get_tickers('KRW')

    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    for v in lst:
        ticker = v
        if not ticker.upper().startswith('KRW-'):
            ticker = 'KRW-' + v.upper()
        print(ticker)

        df = pyupbit.get_ohlcv(ticker, count=200, interval='month', period=1)
        for ind, row in df.iterrows():
            rdate = ind.strftime('%Y-%m-%d')

            cur.execute("INSERT INTO month_candle VALUES(?,?,?,?,?,?,?);",
                        (rdate[:7], v[4:], row["open"], row["high"], row["low"],
                         row["close"], round(row["volume"], 2)))

        time.sleep(0.2)

    conn.commit()
    conn.close()

def make_market_value():
    _, nct, _ = market_code()

    file = open("market_value.csv", "r", encoding='UTF8')
    lines = file.readlines()

    create_table()

    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    for l in lines:
        if len(l.strip()) <= 0:
            continue
        no, ko, price = l.strip().split(',')
        ticker = nct[ko]
        if ticker.startswith('BTC-'):
            ticker = ticker[4:]
        if ticker.startswith('KRW-'):
            ticker = ticker[4:]
        if ticker.startswith('USDT-'):
            ticker = ticker[5:]
        print( no, ticker, ko, price)

        cur.execute("INSERT INTO market_value VALUES(?,?,?,?);",
                    (no, ticker, ko, price))
        conn.commit()

    conn.close()



def Quadruple_Witching_Day():
    query = \
        "select date, symbol, hearn as high, learn as low, earn as close,  hearn-learn as variable from day_candle " \
        "where date in ('2021-03-11', '2021-06-10', '2021-09-09', '2021-12-09', '2022-03-10', '2022-06-09') " \
        "order by symbol, date; "

    con = sqlite3.connect(database_name)
    df = pd.read_sql_query(query, con)
    vals = df.values.tolist()
    idxs = df.index.tolist()

    print(f'종목, 일자, 고가%, 저가%, 종가%, 변동률%')

    for indexs, v in zip(idxs, vals):
        print(f'{v[1]}, {v[0]}, {v[2]:.2f}%, {v[3]:.2f}%, {v[4]:.2f}%, {v[5]:.2f}%')

    con.close()

def symbol_updata(symbol):
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    sql = " UPDATE tmp_t SET symbol = ? WHERE symbol != ?"
    data = (symbol, symbol)
    cur.execute(sql, data)
    conn.commit()

    cur.close()
    conn.close()


def insert_db(start_date):
    lst = get_tickers('KRW')

    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    rdate = start_date
    for v in lst:
        ticker = v
        if not ticker.upper().startswith('KRW-'):
            ticker = 'KRW-' + v.upper()

        print(ticker[4:])

        df = pyupbit.get_ohlcv(ticker, count=20, period=1)
        for ind, row in df.iterrows():
            rdate = ind.strftime('%Y-%m-%d')
            if rdate < start_date:
                continue
            earn = round(((row["close"] / row["open"]) - 1.0) * 100.0,2)
            high = round(((row["high"] / row["open"]) - 1.0) * 100.0,2)
            low = round(((row["low"] / row["open"]) - 1.0) * 100.0,2)

            cur.execute("INSERT INTO day_candle VALUES(?,?,?,?,?,?,?,?,?,?);",
                        (rdate, row["open"], row["high"], row["low"],
                         row["close"], round(row["volume"], 2), high, low, earn, v[4:]))

        time.sleep(0.2)

    conn.commit()
    conn.close()
    print('\nLast update: ' + rdate)


def delete_db(start_date):
    lst = get_tickers('KRW')

    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    sql = "DELETE FROM day_candle WHERE date" + ">= '" + str(start_date) + "';"
    cur.execute(sql)

    conn.commit()
    conn.close()


# 등락 통계
def statistics(ticker):
    query = \
        "select date, symbol, earn from day_candle " \
        "where symbol = '" + ticker.upper() + "' order by date; "

    con = sqlite3.connect(database_name)
    df = pd.read_sql_query(query, con)
    vals = df.values.tolist()
    idxs = df.index.tolist()

    lst = []
    lst.clear()

    start_date = ''
    end_date = ''
    flag = 0
    count = 0

    for indexs, v in zip(idxs, vals):
        fearn = float(v[2])
        if count == 0:
            if 0.0 < fearn:
                flag = 1
            elif fearn < 0.0:
                flag = -1
            count += 1
            start_date = v[0]
            end_date = v[0]
            continue
        else:
            if flag == 1:
                if 0.0 < fearn:
                    count += 1
                    end_date = v[0]
                    continue
                elif fearn < 0.0:
                    lst.append([start_date, end_date, count])
                    count = 1
                    flag = -1
                    start_date = v[0]
                    end_date = v[0]
            elif flag == -1:
                if 0.0 < fearn:
                    lst.append([start_date, end_date, -1 * count])
                    count = 1
                    flag = 1
                    start_date = v[0]
                    end_date = v[0]
                elif fearn < 0.0:
                    count += 1
                    end_date = v[0]
                    continue
            else:
                end_date = v[0]
                continue

    if flag == -1:
        lst.append([start_date, end_date, -1 * count])
    else:
        lst.append([start_date, end_date, count])


    pv_cnt = 0
    for l in lst:
        print(f'{l[0]} ~ {l[1]}, {l[2]}')
        pv_cnt += 1

    print()
    print(f'{ticker.upper()} change direction count = {pv_cnt} / total count = {len(vals)},  duration={round(len(vals)/pv_cnt, 2)}')


    con.close()


def create_minute_table():
    global database_name

    conn = sqlite3.connect(database_name)
    conn.execute(
        'CREATE TABLE minute_candle(ymd TEXT, hms TEXT, symbol TEXT, o REAL, c REAL, earn REAL)')
    conn.close()


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

        if hms.startswith('00:00:00'):
            start_value = row["open"]

        if 0.0 < start_value:
            earn = round(((row["close"] / start_value) - 1.0) * 100.0, 2)
            print(ticker[4:], ymd, hms, start_value, row["close"], earn )
            cur.execute("INSERT INTO minute_candle VALUES(?,?,?,?,?,?);",
                            (ymd, hms, ticker[4:], start_value, row["close"], earn))

        else :
            earn = round(((row["close"] / row["open"]) - 1.0) * 100.0, 2)
            print(ticker[4:], ymd, hms, row["open"], row["close"], earn )
            cur.execute("INSERT INTO minute_candle VALUES(?,?,?,?,?,?);",
                            (ymd, hms, ticker[4:], row["open"], row["close"], earn))

    conn.commit()
    conn.close()

def get_binance_ohlcv(ticker, count=1):
    binance = ccxt.binance()
    parameters = {
        'start': '1',
        'limit': '1',
        'convert': 'USD'
    }

    # 2017-08-17
    start_date = '2017-01-01'
    start = int(time.mktime(datetime.strptime(start_date + ' 00:00', '%Y-%m-%d %H:%M').timetuple())) * 1000

    ohlcv = binance.fetch_ohlcv(ticker.upper()+'/USDT', timeframe='1d', limit=count, since=start)
    df = pd.DataFrame(ohlcv, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
    df.set_index('datetime', inplace=True)
    print(df)


def main():
    # Quadruple_Witching_Day()

    #create_table()
    #make_month_table()

    ##create_minute_table()
    #get_date('BTC', 30000, 'minute5')

    #get_binance_ohlcv('BTC', 10000)

    work_date = '2023-01-03'
    delete_db(work_date)
    insert_db(work_date)

    # statistics('btc')

    # theme_updata('USDT')
    # theme_updata('BTC')
    # theme_updata('KRW')


if __name__ == "__main__":
    main()

# command line 에서 sqlite3 script 호출 하는 방법
# $ sqlite3.exe auction.db < work_script.sql

# py association_analysis.py --symbol=PUNDIX --earning=20 --range=3 --pick=20
