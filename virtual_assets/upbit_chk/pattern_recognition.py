import talib 
import calendar
import getopt
import sys, time
import pyupbit
from common.utils import market_code
from datetime import datetime
import argparse


def get_candlestick_pattern(symbol, df):
    # 캔들스틱 패턴을 인식합니다.
    res = symbol

    lst = talib.CDL2CROWS(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[-1] != 0:
        res += ',' + 'CDL2CROWS'
    




    # 캔들스틱 패턴을 반환합니다.
    # 미완성 (마지막 날짜 Data 만 취합 해서 확인 할 수 있도록 수정 필요)
    return res

def get_ohlcv(ticker):
    if not ticker.startswith('KRW-') and not ticker.startswith('BTC-') and not ticker.startswith('USDT-'):
        ticker = 'KRW-' + ticker

    df = pyupbit.get_ohlcv(ticker)

    return df

def main(argv):
    parser = argparse.ArgumentParser(description='캔들 패턴 인식')
    parser.add_argument('-s', '--symbol', required=False, default='btc', help='심볼 (BTC, ETH, ADA, ..., default=all)')

    args = parser.parse_args()
    symbol = args.symbol

    # 캔들스틱 데이터를 가져옵니다.
    ohlcv = get_ohlcv(symbol)

    # 캔들스틱 패턴을 인식합니다.
    patterns = get_candlestick_pattern(symbol, ohlcv)

    # 캔들스틱 패턴을 출력합니다.
    print(patterns)
    
    # ptns = talib.get_functions()

    # for ptn in ptns:
    #     if ptn.startswith("CDL"):
    #         print(ptn)

if __name__ == "__main__":
    main(sys.argv)

