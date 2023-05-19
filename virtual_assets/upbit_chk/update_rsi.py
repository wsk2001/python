# -*- coding: utf-8 -*-

"""
day_candle table 의 rsi 를 update 한다.

"""

import sys
from datetime import datetime, date
from common.themes import get_themes, get_all_themes
from common.utils import get_idx_values, get_tickers
import argparse
import sqlite3
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from ast import literal_eval
import pandas as pd
import talib as ta
from common.utils import market_code

database_name = './dbms/virtual_asset.db'


def get_data(ticker, start='2010-01-01', end='9999-12-31'):
    query = \
        f"select date, close from day_candle where symbol='{ticker.upper()}' and '{start}' <= date and date <= '{end}';"

    con = sqlite3.connect(database_name)
    df = pd.read_sql_query(query, con)
    df["rsi"] = ta.RSI(df['close'], timeperiod=14)
    con.close()

    df = df.dropna()

    return df

def set_rsi(ticker, df):
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    for row in df.itertuples(index=False):
        print(ticker, row.date, round(row.rsi, 2))
        cur.execute(f"UPDATE day_candle SET rsi = {int(round(row.rsi, 2))} WHERE symbol = '{ticker.upper()}' and date = '{row.date}'")

    conn.commit()
    conn.close()


def main(argv):
    parser = argparse.ArgumentParser(description='옵션 지정 방법')
    parser.add_argument('-t', '--ticker', required=False, default='ALL', help='ticker')
    parser.add_argument('-s', '--start', required=False, default='2023-05-01', help='start date (yyyy-mm-dd)')
    parser.add_argument('-e', '--end', required=False, default='9999-12-31', help='end date (yyyy-mm-dd)')

    args = parser.parse_args()
    ticker = args.ticker
    start = args.start
    end = args.end
    ticker = ticker.upper()

    if ticker.upper().startswith("ALL"):
        code_list, _, _ = market_code()

        for t in code_list:
            df = get_data(t[4:], start, end)
            set_rsi(t[4:], df)
    else:
        df = get_data(ticker, start, end)
        set_rsi(ticker, df)

if __name__ == "__main__":
    main(sys.argv)

