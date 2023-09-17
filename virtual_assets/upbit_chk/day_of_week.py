# -*- coding: utf-8 -*-

import sqlite3
import pandas as pd
import pyupbit
import argparse
from datetime import datetime

database_name = './dbms/virtual_asset.db'
ticker_list = pyupbit.get_tickers('KRW')

def stat_wd(start_date, ticker):
    query = \
        "SELECT " \
        "    strftime('%w', date) AS day_of_week, " \
        "    round((CAST(SUM(CASE WHEN earn > 0 THEN 1 ELSE 0 END) AS REAL) / COUNT(*)),2) AS inc " \
        "FROM " \
        "    day_candle " \
        "WHERE " \
        "    symbol='" + ticker + "' " \
        "and date >= '" + start_date + "' " \
        "group by day_of_week; "

    con = sqlite3.connect(database_name)
    df = pd.read_sql_query(query, con)
    vals = df['inc'].values * 100

    return ticker, vals


def wd_earn(start_date, ticker):
    query = \
        "SELECT " \
        "    strftime('%w', date) AS wd,  round(sum(earn),2) as earn " \
        "FROM " \
        "    day_candle " \
        "WHERE " \
        "    symbol='" + ticker + "' " \
        "and date >= '" + start_date + "' " \
        "group by wd " \
        "order by wd; "

    con = sqlite3.connect(database_name)
    df = pd.read_sql_query(query, con)
    vals = df['earn'].values * 100

    return ticker, vals



def main():
    parser = argparse.ArgumentParser(description='statistics')
    parser.add_argument('-s', '--start', required=False, default='2023-01-01', help='start_date')

    args = parser.parse_args()
    start_date = args.start
    now = datetime.now()


    print("요일별 상승 확률 시작일(" + start_date + ") ~ 현재(" + now.strftime('%Y-%m-%d') + ") 50% 미만은 하락")
    print("SYMBOL, 일, 월, 화, 수, 목, 금, 토")
    for t in sorted(ticker_list):
        ticker, vals = stat_wd(start_date, t[4:])
        if vals is not None and 7 <= len(vals):
            print(ticker, ', ', round(vals[0],2), ',', round(vals[1],2), ',', round(vals[2],2), ',', 
                round(vals[3],2), ',', round(vals[4],2), ',', round(vals[5],2), ',', round(vals[6],2))

if __name__ == "__main__":
    main()
