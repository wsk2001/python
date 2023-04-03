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


def obv(symbol, count):
    if not symbol.startswith('KRW-') and not symbol.startswith('BTC-') and not symbol.startswith('USDT-'):
        symbol = 'KRW-' + symbol

    df = pyupbit.get_ohlcv(symbol, count=count, period=1)
    rl = ta.OBV(df['close'], df['volume'])
    print('OBV(On Balance Volume)')
    print(rl)


# Main function
def main(argv):
    parser = argparse.ArgumentParser(description='옵션 지정 방법')
    parser.add_argument('--symbol', required=False, default='BTC', help='symbol, default=BTC')
    parser.add_argument('--count', required=False, default=90, help='data gettering size (default=90)')

    args = parser.parse_args()
    symbol = args.symbol
    count = int(args.count)

    #code_list, name_to_code, code_to_name = market_code()

    try:
        obv(symbol, count)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main(sys.argv)

# py rsi.py --up=60 --down=35
