import time
import datetime
import sys, getopt
import pyupbit
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
import argparse

def view(v, cnt, interval=None, to=None):
    if v.capitalize().startswith('KRW-'):
        df = pyupbit.get_ohlcv(v, count=cnt)
    else:
        df = pyupbit.get_ohlcv('KRW-' + v, interval=interval, to=to, count=cnt)
    dfs = df['close']
    ax = plt.gca()
    dfs.plot(kind='line', x='name', y='currency', ax=ax)
    plt.title(v + ' (' + str(to)[:10] + ')')
    plt.grid(True)
    plt.show()

def main(argv):

    parser = argparse.ArgumentParser(description='옵션 지정 방법')
    parser.add_argument('--count', required=False, default=1440, help='수집 data 갯수 (default=10000)')
    parser.add_argument('--symbol', required=False, default='btc', help='심볼 (BTC, ETH, ADA, ..., default=all)')
    parser.add_argument('--interval', required=False, default='minute1', help='candle 종류 (day, week, month, minute1, ...)')
    parser.add_argument('--enddate', required=False, default=None, help='종료 일자(yyyymmdd, default=현재 일자)')
    parser.add_argument('--endtime', required=False, default=None, help='종료 시각(hh:mm:ss, default=현재 시각)')

    args = parser.parse_args()
    count = int(args.count)
    symbol = args.symbol
    interval = args.interval
    enddate = args.enddate
    endtime = args.endtime
    to = None

    if enddate is None and endtime is None:
        to = datetime.datetime.now()

    if enddate is not None and endtime is None:
        to = enddate + ' ' + '08:59:00'

    if enddate is not None and endtime is not None:
        to = enddate + ' ' + endtime

    if interval is None:
        interval = 'minute1'

    view(symbol, count, interval, to)


if __name__ == "__main__":
    main(sys.argv)

# python view_graph.py -t SXP
