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
        'CREATE TABLE market_value(no INTEGER, symbol TEXT, ko TEXT, mv REAL)')
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


def select_statistics(symbol):
    symbol_updata(symbol)

    query = \
        f"select A.symbol, round(A.v1_3, 2) as a, round(B.v4_6, 2) as b, round(C.v7_9, 2) as c,                      " \
    "	round(D.v10_12, 2) as d, round(E.v13_15, 2) as e, round(F.v16_18, 2) as f, 			    " \
    "	round(G.v19_21, 2) as g, round(H.v22_24, 2) as h, round(I.v25_27, 2) as i, round(J.v28_31, 2) as j  " \
    "FROM 													    " \
    "(select dc.symbol AS symbol, sum(dc.earn) as v1_3 from day_candle dc, tmp_t tt				    " \
    "where (dc.date like \'%01\' or dc.date like \'%02\' or dc.date like \'%03\' )				    " \
    "and dc.symbol = tt.symbol										    " \
    "and dc.date like tt.remark) A,										    " \
    "(select dc.symbol AS symbol, sum(dc.earn) as v4_6 from day_candle dc, tmp_t tt				    " \
    "where (dc.date like \'%04\' or dc.date like \'%05\' or dc.date like \'%06\' )				    " \
    "and dc.symbol = tt.symbol										    " \
    "and dc.date like tt.remark) B,										    " \
    "(select dc.symbol AS symbol, sum(dc.earn) as v7_9 from day_candle dc, tmp_t tt				    " \
    "where (dc.date like \'%07\' or dc.date like \'%08\' or dc.date like \'%09\' )				    " \
    "and dc.symbol = tt.symbol										    " \
    "and dc.date like tt.remark) C,										    " \
    "(select dc.symbol AS symbol, sum(dc.earn) as v10_12 from day_candle dc, tmp_t tt			    " \
    "where (dc.date like \'%10\' or dc.date like \'%11\' or dc.date like \'%12\' )				    " \
    "and dc.symbol = tt.symbol										    " \
    "and dc.date like tt.remark) D,										    " \
    "(select dc.symbol AS symbol, sum(dc.earn) as v13_15 from day_candle dc, tmp_t tt			    " \
    "where (dc.date like \'%13\' or dc.date like \'%14\' or dc.date like \'%15\' )				    " \
    "and dc.symbol = tt.symbol										    " \
    "and dc.date like tt.remark) E,										    " \
    "(select dc.symbol AS symbol, sum(dc.earn) as v16_18 from day_candle dc, tmp_t tt			    " \
    "where (dc.date like \'%16\' or dc.date like \'%17\' or dc.date like \'%18\' )				    " \
    "and dc.symbol = tt.symbol										    " \
    "and dc.date like tt.remark) F,										    " \
    "(select dc.symbol AS symbol, sum(dc.earn) as v19_21 from day_candle dc, tmp_t tt			    " \
    "where (dc.date like \'%19\' or dc.date like \'%20\' or dc.date like \'%21\' )				    " \
    "and dc.symbol = tt.symbol										    " \
    "and dc.date like tt.remark) G,										    " \
    "(select dc.symbol AS symbol, sum(dc.earn) as v22_24 from day_candle dc, tmp_t tt			    " \
    "where (dc.date like \'%22\' or dc.date like \'%23\' or dc.date like \'%24\' )				    " \
    "and dc.symbol = tt.symbol										    " \
    "and dc.date like tt.remark) H,										    " \
    "(select dc.symbol AS symbol, sum(dc.earn) as v25_27 from day_candle dc, tmp_t tt			    " \
    "where (dc.date like \'%25\' or dc.date like \'%26\' or dc.date like \'%27\' )				    " \
    "and dc.symbol = tt.symbol										    " \
    "and dc.date like tt.remark) I,										    " \
    "(select dc.symbol AS symbol, sum(dc.earn) as v28_31 from day_candle dc, tmp_t tt			    " \
    "where (dc.date like \'%28\' or dc.date like \'%29\' or dc.date like \'%30\' or dc.date like \'%31\' )	    " \
    "and dc.symbol = tt.symbol										    " \
    "and dc.date like tt.remark) J;										    "

    con = sqlite3.connect(database_name)
    df = pd.read_sql_query(query, con)
    vals = df.values.tolist()
    idxs = df.index.tolist()


    try:
        for indexs, v in zip(idxs, vals):
            print(f'{v[0]}, {v[1]/3:.2f}, {v[2]/3:.2f}, {v[3]/3:.2f}, {v[4]/3:.2f}, {v[5]/3:.2f}, {v[6]/3:.2f}, {v[7]/3:.2f}, {v[8]/3:.2f}, {v[9]/3:.2f}, {v[10]/3.5:.2f}')
    except:
        pass
    finally:
        con.close()

def insert_db(start_date):
    lst = get_tickers('KRW')

    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    for v in lst:
        ticker = v
        if not ticker.upper().startswith('KRW-'):
            ticker = 'KRW-' + v.upper()
        print(ticker)

        df = pyupbit.get_ohlcv(ticker, count=100, period=1)
        for ind, row in df.iterrows():
            rdate = ind.strftime('%Y-%m-%d')
            if rdate < start_date:
                continue
            earn = ((row["close"] / row["open"]) - 1.0) * 100.0
            high = ((row["high"] / row["open"]) - 1.0) * 100.0
            low = ((row["low"] / row["open"]) - 1.0) * 100.0

            cur.execute("INSERT INTO day_candle VALUES(?,?,?,?,?,?,?,?,?,?);",
                        (rdate, row["open"], row["high"], row["low"],
                         row["close"], row["volume"], high, low, earn, v[4:]))

        time.sleep(0.2)

    conn.commit()
    conn.close()


def delete_db(start_date):
    lst = get_tickers('KRW')

    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    sql = "DELETE FROM day_candle WHERE date" + ">= '" + str(start_date) + "';"
    cur.execute(sql)

    conn.commit()
    conn.close()


def main():
    # Quadruple_Witching_Day()

    #######################################
    #tickers, nct, _ = market_code()
    #tickers.sort()

    #for t in tickers:
    #    if t.startswith('KRW-'):
    #        select_statistics(t[4:])
    #######################################

    work_date = '2022-09-29'
    delete_db(work_date)
    insert_db(work_date)

    # theme_updata('USDT')
    # theme_updata('BTC')
    # theme_updata('KRW')


if __name__ == "__main__":
    main()

# command line 에서 sqlite3 script 호출 하는 방법
# $ sqlite3.exe auction.db < work_script.sql

# py association_analysis.py --symbol=PUNDIX --earning=20 --range=3 --pick=20
