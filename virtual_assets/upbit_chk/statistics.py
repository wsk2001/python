# -*- coding: utf-8 -*-

import sqlite3
import pandas as pd
import pyupbit
import argparse

database_name = './dbms/virtual_asset.db'
ticker_list = pyupbit.get_tickers('KRW')

def stat_wd(start_date, ticker):
    query = \
        "select symbol, strftime('%w', date) as wd, round(avg(earn),2) as earn from day_candle " \
        "where symbol='" + ticker + "' " \
                                    "and date >= '" + start_date + "' " \
                                                                   "group by wd; "

    con = sqlite3.connect(database_name)
    df = pd.read_sql_query(query, con)
    vals = df.values.tolist()

    return ticker, vals


def stat_day(start_date, ticker):
    query = \
        "select symbol, strftime('%d', date) as md, round(avg(earn),2) as earn from day_candle " \
        "where symbol='" + ticker + "' " \
                                    "and date >= '" + start_date + "' " \
                                                                   "group by md " \
                                                                   "order by md; "

    con = sqlite3.connect(database_name)
    df = pd.read_sql_query(query, con)
    vals = df.values.tolist()

    return ticker, vals


def stat_month(start_date, ticker):
    query = \
        "select symbol, strftime('%m', date) as md, round(avg(earn),2) as earn from day_candle " \
        "where symbol='" + ticker + "' " \
                                    "and date >= '" + start_date + "' " \
                                                                   "group by md " \
                                                                   "order by md; "

    con = sqlite3.connect(database_name)
    df = pd.read_sql_query(query, con)
    vals = df.values.tolist()

    return ticker, vals


def main():
    parser = argparse.ArgumentParser(description='statistics')
    parser.add_argument('--start', required=False, default='2000-01-01', help='start_date')
    parser.add_argument('--mode', required=False, default='W', help='statistic mode (W,D,M) default=W')

    args = parser.parse_args()
    start_date = args.start
    work_mode = args.mode.upper()

    if work_mode == 'W':
        for t in sorted(ticker_list):
            ticker, vals = stat_wd(start_date, t[4:])
            print(ticker)
            print(vals)
    elif work_mode == 'D':
        for t in sorted(ticker_list):
            ticker, vals = stat_day(start_date, t[4:])
            print(ticker)
            print(vals)
    else:
        for t in sorted(ticker_list):
            ticker, vals = stat_month(start_date, t[4:])
            print(ticker, end='')
            for v in vals:
                print(',', v[1], v[2], end='')
            print()

if __name__ == "__main__":
    main()
