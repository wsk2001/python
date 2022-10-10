import datetime
import numpy as np
import pyupbit
import matplotlib.pyplot as plt
import talib as ta
import argparse
import sys

# 한글 폰트 사용을 위해서 세팅 (아래 4줄)
from matplotlib import font_manager, rc

font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

def view(v, cnt, interval=None, to=None):
    if v.capitalize().startswith('KRW-'):
        df = pyupbit.get_ohlcv(v, count=cnt)
    else:
        df = pyupbit.get_ohlcv('KRW-' + v, interval=interval, to=to, count=cnt)

    close = df['close']

    macd, macdsignal, macdhist = ta.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)

    plt.plot(macd,label='MACD')
    plt.plot(macdsignal,label='MACD Signal')
    plt.bar(macdhist.index,macdhist ,label='MACD Oscillator')
    plt.xlabel('date')
    plt.ylabel('indicator value')
    plt.legend()
    plt.title(f'{v.upper()} MACD, interval={interval}, count={cnt}')
    plt.show()



def str_to_datetime(date_time_str):
    date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
    return date_time_obj


def datetime_to_str(date_time_obj):
    date_time_str = date_time_obj.strftime('%Y-%m-%d %H:%M:%S')
    return date_time_str


# py view_stocastic.py --count=60 --interval=day --symbol=TT
def main(argv):
    parser = argparse.ArgumentParser(description='옵션 지정 방법')
    parser.add_argument('--count', required=False, default=90, help='수집 data 갯수 (default=10000)')
    parser.add_argument('--symbol', required=False, default='ada', help='심볼 (BTC, ETH, ADA, ..., default=all)')
    parser.add_argument('--interval', required=False, default='day',
                        help='candle 종류 (day, week, month, minute1, ...)')

    args = parser.parse_args()
    count = int(args.count)
    symbol = args.symbol
    interval = args.interval
    to = None

    if interval is None:
        interval = 'minute1'

    view(symbol, count, interval, to)


if __name__ == "__main__":
    main(sys.argv)

# py view_stocastic.py --count=60 --interval=day --symbol=TT