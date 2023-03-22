# importing package
import matplotlib.pyplot as plt
import time, sys, getopt
import datetime
import sqlite3
import pandas as pd
import numpy as np
from datetime import date, timedelta
import argparse

# 한글 폰트 사용을 위해서 세팅 (아래 4줄)
from matplotlib import font_manager, rc
font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

database_name = './dbms/virtual_asset.db'


def select_ytd(symbol, start, end):
    query = \
        "select date, close from day_candle " \
        "where  1 = 1 " \
        "and symbol = '" + symbol.upper() + "' " \
        "and '" + start + "' <= date " \
        "and date <= '" + end + "';"

    con = sqlite3.connect(database_name)
    df = pd.read_sql_query(query, con)

    con.close()

    return df


def main(argv):
    parser = argparse.ArgumentParser(description='옵션 지정 방법')
    parser.add_argument('--symbol', required=False, default='btc', help='심볼 (BTC, ETH, ADA, ..., default=all)')
    parser.add_argument('--marker', required=False, default='yes', help='꼭지점 마커 표시(yes/no)')
    parser.add_argument('--start', required=False, default=None, help='시작 일자(yyyy-mm-dd, default=현재 일자-100)')
    parser.add_argument('--end', required=False, default=None, help='종료 일자(yyyy-mm-dd, default=현재 일자)')

    args = parser.parse_args()
    symbol = args.symbol.upper()
    start = args.start
    end = args.end
    marker = args.marker

    today = date.today()

    if start is None:
        tmpday = today - timedelta(days=100)  # 100 일전
        start = tmpday.strftime('%Y-%m-%d')

    if end is None:
        end = today.strftime('%Y-%m-%d')

    df = select_ytd(symbol, start, end)

    x = df['date'].values.tolist()
    close = df['close'].values.tolist()

    plt.xticks(np.arange(0, len(x), step=30))

    plt.title( symbol + ' : ' + start + ' ~ ' + end)
    plt.grid(which='both')

    if len(x) < 70 or marker.lower().startswith('yes'):
        plt.plot(x, close, label=symbol, color="green", marker='o', markersize=4)
    else:
        plt.plot(x, close, label=symbol, color="green")

    plt.legend()
    plt.show()


if __name__ == "__main__":
    main(sys.argv)
