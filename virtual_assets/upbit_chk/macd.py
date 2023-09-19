# -*- coding: utf-8 -*-

import requests
from ast import literal_eval
import numpy as np
import pandas as pd
import operator
from common.utils import market_code
import time, datetime, sys, getopt
import json
import argparse
import talib as ta
import pyupbit


def get_ohlcv(ticker, interval='day'):
    if not ticker.startswith('KRW-') and not ticker.startswith('BTC-') and not ticker.startswith('USDT-'):
        ticker = 'KRW-' + ticker

    df = pyupbit.get_ohlcv(ticker, interval=interval)

    return df


def macd_trend(ticker, df, posi=-1):
    if len(df) < 26:
        return 'MACD no signal'
    
    macd_line = df['close'].ewm(span=12, min_periods=12).mean() - df['close'].ewm(span=26, min_periods=26).mean()

    signal_line = macd_line.ewm(span=9, min_periods=9).mean()

    zero_line = 0
    b = 0
    s = 0
    h = 0
    if macd_line[posi] > signal_line[posi] and macd_line[posi] > zero_line:
        print(ticker,'매수')
        b = 1
    elif macd_line[posi] < signal_line[posi] and macd_line[posi] < zero_line:
        print(ticker,'매도')
        s = 1
    else:
        print(ticker,'홀드')
        h = 1
    return b, s, h
# Main function
# macd 가 macdsignal 을 상향 돌파 하는지 확인.

def main(argv):
    parser = argparse.ArgumentParser(description='옵션 지정 방법')
    parser.add_argument('-i', '--interval', required=False, default='minute5',
                        help='candle 종류 (day, week, month, minute1, ...)')
    parser.add_argument('-s', '--symbol', required=False, default='all',
                        help='symbol (default:all)')

    args = parser.parse_args()
    interval = args.interval
    symbol = args.symbol

    buy = 0
    sell = 0
    hold = 0

    if not symbol.lower().startswith('all'):
        df = get_ohlcv(symbol, interval)
        macd_trend(symbol, df)
    else:
        try:
            lst = pyupbit.get_tickers(fiat="KRW")
            lst.sort()

            ptn_score_list = []
            ptn_score_list.clear()

            for v in lst:
                time.sleep(0.1)
                df = get_ohlcv(v[4:], interval)
                b, s, h = macd_trend(v[4:], df)
                buy += b
                sell += s
                hold += h
        except Exception as e:
            print(e)

        print()
        print('interval=', interval)
        print('매수:', buy, ', 매도:', sell, ', 홀드:', hold)

if __name__ == "__main__":
    main(sys.argv)

# py rsi.py --up=60 --down=35
