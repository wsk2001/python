# -*- coding: utf-8 -*-

"""
연관성 분석 App
특정 종목이 주어진 % 이상 상승 했을때 전/후로 특정% 이상 상승한 종목을 이용해 연관성 분석.
1. 지정 옵션: symbol, 기간 10,000일, earn(원본 종목의 상승%), comp earn(비교하 종목들의 상승%)
2. 모든 종목들의 일간 상승률 저장 plus 인 경우만 저장. (일자, 상승%, symbol)
3.
"""

import sqlite3
import pandas as pd
from datetime import date, timedelta

database_name = './dbms/virtual_asset.db'


def insert_ytd(ymd, o, c, ytd, alt):
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    cur.execute("INSERT INTO ytd VALUES(?,?,?,?,?);",
                (ymd, o, c, ytd, alt))
    conn.commit()
    conn.close()


# 연초 대비 인덱스 생성
def select_ytd(ymd):
    query = \
        "select round(sum(S.open),2) as open, round(sum(E.close),2) as close, round((((close / open) -1) * 100),2) as YTD FROM " \
        "( " \
        "       ( " \
        "                select symbol, date, open from day_candle " \
        "                where date = '2024-01-01' " \
        "        ) S, " \
        "        ( " \
        "                select symbol, date, close from day_candle " \
        "                where date = '" + ymd + "' " \
        "        ) E " \
        ") " \
        "WHERE S.symbol = E.symbol; "

    con = sqlite3.connect(database_name)
    df = pd.read_sql_query(query, con)
    vals = df.values.tolist()

    con.close()

    return ymd, vals[0][0], vals[0][1], vals[0][2]

def select_ytd_btc(ymd):
    query = \
        "select round(sum(S.open),2) as open, round(sum(E.close),2) as close, round((((close / open) -1) * 100),2) as YTD FROM " \
        "( " \
        "       ( " \
        "                select symbol, date, open from day_candle " \
        "                where date = '2024-01-01' and symbol = 'BTC'" \
        "        ) S, " \
        "        ( " \
        "                select symbol, date, close from day_candle " \
        "                where date = '" + ymd + "' and symbol = 'BTC'" \
        "        ) E " \
        ") " \
        "WHERE S.symbol = E.symbol; "

    con = sqlite3.connect(database_name)
    df = pd.read_sql_query(query, con)
    vals = df.values.tolist()

    con.close()

    return ymd, vals[0][0], vals[0][1], vals[0][2]



def delete_ytd(day):
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    sql = "DELETE FROM ytd WHERE ymd" + " = '" + day + "';"
    cur.execute(sql)

    conn.commit()
    conn.close()


def list_year_to_today(start=None):
    today = date.today()
    yesterday = today - timedelta(days=1)  # 어제 날짜 계산
    year = today.year

    if start is None:
        start = 10
    elif start < 0:
        start = start * -1

    # start_date = date(year, 1, 1)  # 해당 년도의 1월 1일
    start_date = today - timedelta(days=start)
    end_date = yesterday

    delta = timedelta(days=1)  # 1일씩 증가하도록 timedelta 생성

    date_list = []

    while start_date <= end_date:
        date_list.append(start_date.strftime('%Y-%m-%d'))
        start_date += delta

    return date_list

def main():
    # days = [
    #     '2023-03-09', '2023-03-10', '2023-03-11', '2023-03-12', '2023-03-13',
    # ]

    days = list_year_to_today(7)

    for day in days:
        ymd, open, close, ytd = select_ytd(day)
        _, _, _, btc = select_ytd_btc(day)
        delete_ytd(day)
        insert_ytd(ymd, open, close, ytd, btc)
        print(ymd, open, close, ytd, btc)

if __name__ == "__main__":
    main()
