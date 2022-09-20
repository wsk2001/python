import sys, time
import pyupbit
import talib

from common.utils import market_code, get_interval
from datetime import datetime, date
import argparse
import sqlite3
import pandas as pd


##############################################################################
# 스토캐스틱 (Stochastic)지표로 매매하는 법
# 주로 횡보장이나 박스권에서 많이 씁니다.
# 5-3-3, 10-6-6, 20-12-12 숫자가 적어질수록 단기적인 움직임을 보기 용이하며
# 긴 흐름을 가져 가실 때는 20 12 12 로 보시면 됩니다.
# upbit 에서는 default 로 9,3,3 또는 14,3,3 으로 되어 있음
##############################################################################
# 다이버전스 를 이용한 추세 전환 분석
# 과매수와 과매도 수준을 판단하고 이를 활용한 매수/매도
# %K 와 %D 선의 교차를 통해 진입 시점 판단.
#    매수 신호 = %K선이 과매도 영역 에서 아래 에서 %D선을 교차 합니다.
#    매도 신호 = %K선이 과매수 영역 에서 위에서 %D선을 교차 합니다.
# 스토캐스틱 선들의 방향과 봉우리 모양
##############################################################################
def AddStochastic(priceData, period=9, screen_window=3, slow_window=3):
    ndayhigh = priceData['high'].rolling(window=period, min_periods=1).max()
    ndaylow = priceData['low'].rolling(window=period, min_periods=1).min()
    fast_k = (priceData['close'] - ndaylow) / (ndayhigh - ndaylow) * 100
    fast_d = fast_k.rolling(window=screen_window).mean()
    slow_k = fast_k.rolling(window=slow_window).mean()
    slow_d = fast_d.rolling(window=slow_window).mean()
    return priceData.assign(slow_k=slow_k, slow_d=slow_d).dropna().copy()


def stocastic_list(ticker, cnt, interval='day'):
    if not ticker.startswith('KRW-') and not ticker.startswith('BTC-') and not ticker.startswith('USDT-'):
        ticker = 'KRW-' + ticker

    df = pyupbit.get_ohlcv(ticker, count=cnt, period=1)
    df = AddStochastic(df, 9, 3, 3)

    vals = df.values.tolist()
    idxs = df.index.tolist()

    last = len(idxs) - 1

    print('stochastic, symbol:', ticker[4:])
    print('일자 , 종가, SLOW K%, SLOW D%')

    for indexs, v in zip(idxs, vals):
        print(str(indexs)[:10], f'{v[3]:.2f}, {v[6]:.2f}, {v[7]:.2f}')

    print()
    print(str(idxs[last])[:10], f'{vals[last][3]:.2f}, {vals[last][6]:.2f}, {vals[last][7]:.2f}')


def stocastic(ticker, interval='day', count=60, period=9, perk=3, perd=3):
    if not ticker.startswith('KRW-') and not ticker.startswith('BTC-') and not ticker.startswith('USDT-'):
        ticker = 'KRW-' + ticker

    df = pyupbit.get_ohlcv(ticker, interval=interval, count=count, period=1)

    dft = AddStochastic(df, period, perk, perd)
    vals = dft.values.tolist()
    idxs = dft.index.tolist()
    last = len(idxs) - 1
    k = vals[last][6]
    d = vals[last][7]

    return ticker[4:], k, d


def check_stocastic(symbol='ALL', interval='day', count=0, period=9, periodk=3, periodd=3):
    if symbol.startswith('ALL'):
        code_list, _, _ = market_code()
        code_list.sort()
    else:
        code_list = [symbol]
    if count == 0:
        count = datetime.now().timetuple().tm_yday - 1

    print('symbol, %K, %D')
    for v in code_list:
        ticker, k, d = stocastic(v, interval, count, period, periodk, periodd)

        if d <= 20 and 20 < k:
            if d < k:
                print(f'{ticker}, {k:.2f}, {d:.2f} buy')
        elif 80 <= d:
            if d > k:
                print(f'{ticker}, {k:.2f}, {d:.2f} sell')

        # else:
        #     print(f'{ticker}, {k:.2f}, {d:.2f}')
        time.sleep(0.3)

def main(argv):
    parser = argparse.ArgumentParser(description='옵션 지정 방법')
    parser.add_argument('--symbol', required=False, default='ALL', help='symbol (default=ALL)')
    parser.add_argument('--count', required=False, default=60, help='candle count(default=60)')
    parser.add_argument('--period', required=False, default=9, help='period nday (default=9)')
    parser.add_argument('--periodk', required=False, default=3, help='period K (default=3)')
    parser.add_argument('--periodd', required=False, default=3, help='period D (default=3)')
    parser.add_argument('--interval', required=False, default='day', help='interval day or minute1~240 (default=day)')

    args = parser.parse_args()
    count = args.count
    symbol = args.symbol
    period = int(args.period)
    periodk = int(args.periodk)
    periodd = int(args.periodd)
    interval = args.interval

    check_stocastic(symbol, interval, count, period, periodk, periodd)


if __name__ == "__main__":
    main(sys.argv)

# run: python get_ohlcv.py -c 7 -t kava -i d
# 일단위 data 수집시, 최고가 일자 _data, 최저가 일자 _data print 하도록 수정 필요.
# BTC market 가격 반영
