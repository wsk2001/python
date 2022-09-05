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


def main():
    theme_updata('USDT')
    theme_updata('BTC')
    theme_updata('KRW')



if __name__ == "__main__":
    main()

# py association_analysis.py --symbol=PUNDIX --earning=20 --range=3 --pick=20
