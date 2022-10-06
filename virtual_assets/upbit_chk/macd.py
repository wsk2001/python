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


def macd_func(symbol, count, interval='day'):
    if not symbol.startswith('KRW-') and not symbol.startswith('BTC-') and not symbol.startswith('USDT-'):
        symbol = 'KRW-' + symbol

    df = pyupbit.get_ohlcv(symbol, count=count, interval=interval, period=1)
    macd, macdsignal, macdhist = ta.MACD(df['close'], fastperiod=12, slowperiod=26, signalperiod=9)
    return macd, macdsignal, macdhist


def check_golden_cross(macd, macd_signal):
    if macd[-5] < macd_signal[-5] and macd[-4] < macd_signal[-4] and macd[-3] < macd_signal[-3] and \
            macd[-2] < macd_signal[-2] and macd[-1] > macd_signal[-1]:
        return True
    else:
        return False


def check_death_cross(macd, macd_signal):
    if macd[-5] > macd_signal[-5] and macd[-4] > macd_signal[-4] and macd[-3] > macd_signal[-3] and \
            macd[-2] > macd_signal[-2] and macd[-1] < macd_signal[-1]:
        return True
    else:
        return False


# Main function
# macd 가 macdsignal 을 상향 돌파 하는지 확인.

def main(argv):
    parser = argparse.ArgumentParser(description='옵션 지정 방법')
    parser.add_argument('--count', required=False, default=90, help='data gettering size (default=90)')
    parser.add_argument('--interval', required=False, default='day',
                        help='candle 종류 (day, week, month, minute1, ...)')

    args = parser.parse_args()
    count = int(args.count)
    interval = args.interval

    print('symbol, macd, signal, remark')
    try:
        code_list, _, _ = market_code()
        code_list.sort()
        for t in code_list:
            macd, macdsignal, macdhist = macd_func(t, count, interval)
            price = round(pyupbit.get_current_price(t),4)
            if check_golden_cross(macd, macdsignal):
                print(f'{t[4:]}, {round(macd[-1], 2)}, {round(macdsignal[-1], 2)}, price={price}, Golden Cross')
            elif check_death_cross(macd, macdsignal):
                print(f'{t[4:]}, {round(macd[-1], 2)}, {round(macdsignal[-1], 2)}, price={price}, Death Cross')
            time.sleep(0.3)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main(sys.argv)

# py rsi.py --up=60 --down=35
