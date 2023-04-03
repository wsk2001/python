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

def RSI_analysis(code_list, code_to_name, target_up=70, target_down=30):

    start = time.time()
    up_dict = {}
    down_dict = {}
    up_dict.clear()
    down_dict.clear()

    # 코인별 시간별 가격
    for i in range(len(code_list)):
        df = pyupbit.get_ohlcv(code_list[i], count=60, period=1)
        rsi_s = ta.RSI(df['close'], timeperiod=14)
        rsi = rsi_s[-1]

        if target_up <= rsi:
            up_dict[code_list[i][4:]] = rsi

        if rsi <= target_down:
            down_dict[code_list[i][4:]] = rsi

        time.sleep(0.3)

    if 0 < len(up_dict):
        print(f'RSI {target_up} 이상 종목')
        for key in up_dict.keys():
            print(f'{key}, {up_dict[key]:.2f}')

    if 0 < len(down_dict):
        print(f'\nRSI {target_down} 이하 종목')
        for key in down_dict.keys():
            print(f'{key}, {down_dict[key]:.2f}')

    print("\nData 추출 시각 : " + time.strftime('%c', time.localtime(time.time())) + "\n")


# Main function
def main(argv):
    parser = argparse.ArgumentParser(description='옵션 지정 방법')
    parser.add_argument('--up', required=False, default=70, help='check upper limit (default=70)')
    parser.add_argument('--down', required=False, default=30, help='check lower limit (default=30)')

    args = parser.parse_args()
    rsi_up = int(args.up)
    rsi_down = int(args.down)

    code_list, name_to_code, code_to_name = market_code()

    try:
        RSI_analysis(code_list, code_to_name, rsi_up, rsi_down)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main(sys.argv)

# py rsi.py --up=60 --down=35
