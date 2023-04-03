# -*- coding: utf-8 -*-

"""
연관성 분석 App
특정 종목이 주어진 % 이상 상승 했을때 전/후로 특정% 이상 상승한 종목을 이용해 연관성 분석.
1. 지정 옵션: symbol, 기간 10,000일, earn(원본 종목의 상승%), comp earn(비교하 종목들의 상승%)
2. 모든 종목들의 일간 상승률 저장 plus 인 경우만 저장. (일자, 상승%, symbol)
3.
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
    parser.add_argument('--count', required=False, default=200, help='count of candle')

    args = parser.parse_args()
    symbol = args.symbol
    interval = args.interval
    count = int(args.count)

    if symbol.upper().startswith('ALL'):
        lst = get_tickers('KRW')
        for v in lst:
            df = pyupbit.get_ohlcv(v, interval=interval, count=count, period=1)
            doji = ta.CDLDOJI(high=df['high'], low=df['low'], open=df['open'], close=df['close'])

            vals = doji.values.tolist()
            idxs = doji.index.tolist()

            v_cnt = 0

            if 0 < vals[-2]:
                v_cnt += 1
            if 0 < vals[-3]:
                v_cnt += 1

            if 1 < v_cnt:
                print(f'{v[4:]}, {v_cnt}')
            # for indexs, values in zip(idxs, vals):
            #     print(str(indexs)[:10], values)

            time.sleep(0.3)
    else:
        if not symbol.startswith('KRW-') and not symbol.startswith('BTC-') and not symbol.startswith('USDT-'):
            symbol = 'KRW-' + symbol

        df = pyupbit.get_ohlcv(symbol, interval=interval, count=count, period=1)
        doji = ta.CDLDOJI(high=df['high'], low=df['low'], open=df['open'], close=df['close'])

        vals = doji.values.tolist()
        idxs = doji.index.tolist()

        v_cnt = 0

        if 0 < vals[-2]:
            v_cnt += 1
        if 0 < vals[-3]:
            v_cnt += 1

        if 1 < v_cnt:
            print(f'{v[4:]}, {v_cnt}')

        # for indexs, values in zip(idxs, vals):
        #     print(str(indexs)[:10], values)


if __name__ == "__main__":
    main()

# py cdldoji.py --symbol=GMT --interval=minute240 --count=30
