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


def macd_func(symbol, count):
    if not symbol.startswith('KRW-') and not symbol.startswith('BTC-') and not symbol.startswith('USDT-'):
        symbol = 'KRW-' + symbol

    df = pyupbit.get_ohlcv(symbol, count=count, period=1)
    macd, macdsignal, macdhist = ta.MACD(df['close'], fastperiod=12, slowperiod=26, signalperiod=9)
    return macd, macdsignal, macdhist


# Main function
def main(argv):
    parser = argparse.ArgumentParser(description='옵션 지정 방법')
    parser.add_argument('--count', required=False, default=90, help='data gettering size (default=90)')
    parser.add_argument('--buy', required=False, default=20, help='buy signal (default=20)')
    parser.add_argument('--sell', required=False, default=80, help='sell signal (default=80)')

    args = parser.parse_args()
    count = int(args.count)
    sell_signal = float(args.sell)
    buy_signal = float(args.buy)

    try:
        code_list, _, _ = market_code()
        code_list.sort()
        for t in code_list:
            macd, macdsignal, macdhist = macd_func(t, count)
            print(macdsignal)
            time.sleep(0.3)
            break
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main(sys.argv)

# py rsi.py --up=60 --down=35
