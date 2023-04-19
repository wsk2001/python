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

def RSI_analysis(code_list, interval='day'):

    start = time.time()
    rsi_dict = {}
    rsi_dict.clear()

    # 코인별 시간별 가격
    for ticker in code_list:
        df = pyupbit.get_ohlcv(ticker, interval=interval, count=60, period=1)
        rsi_s = ta.RSI(df['close'], timeperiod=14)
        rsi = rsi_s[-1]
        print(".", end='')
        sys.stdout.flush()

        rsi_dict[ticker[4:]] = rsi

        time.sleep(0.3)

    print()
    sorted_rsi = dict(sorted(rsi_dict.items(), key=lambda item: item[1], reverse=True))
    for key in sorted_rsi.keys():
        print(f'{key}, {sorted_rsi[key]:.2f}')

    print("\nData 추출 시각 : " + time.strftime('%c', time.localtime(time.time())) + "\n")


# Main function
def main(argv):
    parser = argparse.ArgumentParser(description='옵션 지정 방법')
    parser.add_argument('--interval', required=False, default='day', help='check interval (default=day)')

    args = parser.parse_args()
    interval = args.interval

    code_list, _, _ = market_code()

    try:
        RSI_analysis(code_list, interval)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main(sys.argv)

# py rsi.py --up=60 --down=35
