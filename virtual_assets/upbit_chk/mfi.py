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


def mfi(symbol, count):
    if not symbol.startswith('KRW-') and not symbol.startswith('BTC-') and not symbol.startswith('USDT-'):
        symbol = 'KRW-' + symbol

    df = pyupbit.get_ohlcv(symbol, count=count, period=1)
    rl = ta.MFI(high=df['high'], low=df['low'], close=df['close'], volume=df['volume'], timeperiod=14)
    return rl[-2], rl[-1]


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

    print(f'심볼, 당일지수, 전일지수, 시그널')

    try:
        code_list, _, _ = market_code()
        code_list.sort()
        for t in code_list:
            v2, v1 = mfi(t, count)
            if sell_signal <= v2:
                if v2 > v1:
                    print(f'{t[4:]}, {v1:.2f}, {v2:.2f}, sell')
            elif v2 <= buy_signal:
                if v1 > v2:
                    print(f'{t[4:]}, {v1:.2f}, {v2:.2f}, buy')

            time.sleep(0.3)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main(sys.argv)

# py rsi.py --up=60 --down=35
