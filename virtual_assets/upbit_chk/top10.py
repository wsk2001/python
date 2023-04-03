# -*- coding: utf-8 -*-

"""
매일 top3 출력
"""

import time
import pyupbit
from datetime import datetime, date
from common.themes import get_themes, get_all_themes
from common.utils import get_idx_values, get_tickers
import sys
import argparse
import sqlite3
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import requests
from ast import literal_eval
import pandas as pd
import ccxt

database_name = './dbms/virtual_asset.db'

def top3_Day(str_date, limit=3):
    query = \
        "select date, symbol, earn, close from day_candle " \
        "where date = " + "\'" + str_date + "\' " \
        "order by earn desc " \
        "limit " + str(limit) + "; "

    con = sqlite3.connect(database_name)
    df = pd.read_sql_query(query, con)
    vals = df.values.tolist()
    idxs = df.index.tolist()

    for indexs, v in zip(idxs, vals):
        print(f'{v[1]}, {v[0]}, {v[2]:.2f}%, {v[3]}')
    print()

    con.close()


def main(argv):
    # date_time_str = '2017-09-25'
    parser = argparse.ArgumentParser(description='옵션 지정 방법')
    parser.add_argument('--count', required=False, default=3, help='top 개 수 (default=3)')
    parser.add_argument('--start', required=False, default='2017-09-25', help='start date (default=2017-09-25)')
    parser.add_argument('--end', required=False, default=None, help='end date (default=today)')

    args = parser.parse_args()
    count = int(args.count)
    start = args.start

    if args.end is None:
        now = datetime.now()
        end = now.strftime("%Y-%m-%d")
    else:
        end = args.end

    date_time_str = start

    print(f'종목, 일자, 등락률%, 종가')
    i = 0
    while True:
        date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d')
        top3_Day(date_time_str, count)
        future = date_time_obj + relativedelta(days=1)
        date_time_str = future.strftime('%Y-%m-%d')
        if date_time_str.startswith(end):
            break
        i += 1
        if 10000 < i:
            break


if __name__ == "__main__":
    main(sys.argv)

# command line 에서 sqlite3 script 호출 하는 방법
# $ sqlite3.exe auction.db < work_script.sql

# py association_analysis.py --symbol=PUNDIX --earning=20 --range=3 --pick=20
