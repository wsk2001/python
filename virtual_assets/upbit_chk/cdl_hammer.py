# -*- coding: utf-8 -*-

"""
detect hammer pattern
"""

import pyupbit
import argparse
import talib as ta
from common.utils import get_tickers
import sys, time

def main():
    parser = argparse.ArgumentParser(description='옵션 지정 방법')
    parser.add_argument('--symbol', required=False, default='ALL', help='심볼 (default:ALL)')
    parser.add_argument('--interval', required=False, default='day', help='interval(day,minute60, ..., default=day)')
    parser.add_argument('--count', required=False, default=100, help='count of candle')

    args = parser.parse_args()
    symbol = args.symbol
    interval = args.interval
    count = int(args.count)

    if symbol.upper().startswith('ALL'):
        lst = get_tickers('KRW')
        for v in lst:
            df = pyupbit.get_ohlcv(v, interval=interval, count=count, period=1)
            ser = ta.CDLHAMMER(df['open'], df['high'], df['low'], df['close'])

            vals = ser.values.tolist()
            idxs = ser.index.tolist()

            if 0 < vals[-1]:
                print(f'\n{v[4:]}, {str(idxs[-1])[:10]}, {vals[-1]}')
            else:
                print('.', flush=True, end='')

            time.sleep(0.3)


if __name__ == "__main__":
    main()

# py cdldoji.py --symbol=GMT --interval=minute240 --count=30
