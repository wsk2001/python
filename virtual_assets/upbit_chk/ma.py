import sys, time
import pyupbit
import talib as ta

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
def add_moving_average(df, period=9, screen_window=3, slow_window=3):
    ma5 = ta.stream_MA(df['close'], 5)
    ma20 = ta.stream_MA(df['close'], 20)
    ma60 = ta.stream_MA(df['close'], 60)

    return df.assign(ma5=ma5, ma20=ma20, ma60=ma60).dropna().copy()


# 골든크로스(Golden cross) 및 데드크로스(Death cross) 확인(20일, 60일 이동편균선)
def chkCross(df):
    chk = 0
    for i in range(len(df)):
        if df['ma20'][i] < df['ma5'][i] and chk == 0:
            print('Golden cross ', str(df.index[i])[:10])
            chk = 1
        elif df['ma20'][i] > df['ma5'][i] and chk == 1:
            print('Death cross ', str(df.index[i])[:10])
            chk = 0
    return chk

def moving_average(ticker, interval='day', count=120, period=9, perk=3, perd=3):
    if not ticker.startswith('KRW-') and not ticker.startswith('BTC-') and not ticker.startswith('USDT-'):
        ticker = 'KRW-' + ticker

    df = pyupbit.get_ohlcv(ticker, interval=interval, count=count, period=1)

    dft = add_moving_average(df, period, perk, perd)
    vals = dft.values.tolist()
    #idxs = dft.index.tolist()
    last = len(vals) - 1
    m5 = vals[last][6]
    m20 = vals[last][7]
    m60 = vals[last][8]

    # chkCross(dft)

    return ticker[4:], m5, m20, m60


def check_ma(symbol='ALL', interval='day', count=120):
    if symbol.startswith('ALL'):
        code_list, _, _ = market_code()
        code_list.sort()
    else:
        code_list = [symbol]
    if count == 0:
        count = datetime.now().timetuple().tm_yday - 1

    print('symbol, ma5, ma20, ma60')
    for v in code_list:
        ticker, ma5, ma20, ma60 = moving_average(v, interval, count)
        if ma60 < ma20 < ma5:
            print(f'{ticker}, {ma5:.2f}, {ma20:.2f}, {ma60:.2f} **정배열**')
        else:
            print(f'{ticker}, {ma5:.2f}, {ma20:.2f}, {ma60:.2f}')

        time.sleep(0.3)

def main(argv):
    parser = argparse.ArgumentParser(description='옵션 지정 방법')
    parser.add_argument('--symbol', required=False, default='ALL', help='symbol (default=BTC)')
    parser.add_argument('--count', required=False, default=120, help='candle count(default=120)')
    parser.add_argument('--interval', required=False, default='day', help='interval day or minute1~240 (default=day)')

    args = parser.parse_args()
    count = args.count
    symbol = args.symbol
    interval = args.interval

    check_ma(symbol, interval, count)


if __name__ == "__main__":
    main(sys.argv)

# run: python get_ohlcv.py -c 7 -t kava -i d
# 일단위 data 수집시, 최고가 일자 _data, 최저가 일자 _data print 하도록 수정 필요.
# BTC market 가격 반영
