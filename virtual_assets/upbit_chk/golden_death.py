# -*- coding: utf-8 -*-

import sys
from common.utils import get_binance_btc, get_fng
from common.utils import upbit_get_usd_krw
from common.dominance import get_dominance
import argparse
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

database_name = './dbms/virtual_asset.db'

def select_data(symbol, start_date, end_date='9999-12-31'):

    query = f"select date, open, high, low, close, volume, rsi from day_candle " \
            f"where symbol = '{symbol.upper()}' and " \
            f"date >= '{start_date}' and " \
            f"date <= '{end_date}' and " \
            f"rsi is not null order by Date;"

    con = sqlite3.connect(database_name)
    df = pd.read_sql_query(query, con)

    con.close()

    return df

def view(ticker, df):

    # 이동평균 계산
    short_ma = df['close'].rolling(window=3).mean()
    long_ma = df['close'].rolling(window=10).mean()

    # 골든 크로스와 데스 크로스 확인
    if (short_ma.shift(1) > long_ma.shift(1)) & (short_ma < long_ma):
        golden_crosses = True
    else:
        golden_crosses = False

    if (short_ma.shift(1) < long_ma.shift(1)) & (short_ma > long_ma):
        death_crosses = True
    else:
        death_crosses = False

    # 결과 출력
    print(golden_crosses)
    print(death_crosses)

    # 차트 그리기
    plt.plot(df['close'])
    plt.plot(short_ma, color='red')
    plt.plot(long_ma, color='blue')
    plt.show()


def main(argv):
    parser = argparse.ArgumentParser(description='옵션 지정 방법')
    parser.add_argument('-t', '--ticker', required=False, default='BTC', help='ticker')
    parser.add_argument('-s', '--start', required=False, default='2023-05-01', help='start date (yyyy-mm-dd)')
    parser.add_argument('-e', '--end', required=False, default='9999-12-31', help='end date (yyyy-mm-dd)')

    args = parser.parse_args()
    ticker = args.ticker
    start = args.start
    end = args.end
    ticker = ticker.upper()

    df = select_data(ticker, start, end)
    view(ticker, df)

if __name__ == "__main__":
    main(sys.argv)
