import time
import datetime
import sys, getopt
import pyupbit
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import argparse


def view(v, cnt, interval=None, to=None, disp='no', save='yes'):
    if v.capitalize().startswith('KRW-'):
        df = pyupbit.get_ohlcv(v, count=cnt)
    else:
        df = pyupbit.get_ohlcv('KRW-' + v, interval=interval, to=to, count=cnt)
    dfs = df['close']
    ax = plt.gca()
    dfs.plot(kind='line', x='name', y='currency', ax=ax)
    plt.title(v + ' (' + str(to)[:10] + ')')
    plt.grid(True)
    #figure(figsize=(8, 6))

    # Image 가 작게 저장됨.
    if save.lower().startswith('yes'):
        manager = plt.get_current_fig_manager()
        #manager.full_screen_toggle()
        #manager.frame.Maximize(True)
        manager.window.state('zoomed')
        plt.savefig('charts/' + v + '_' + str(to)[:10] + '.png')

    if disp.lower().startswith('yes'):
        plt.show()


def str_to_datetime(date_time_str):
    date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
    return date_time_obj


def datetime_to_str(date_time_obj):
    date_time_str = date_time_obj.strftime('%Y-%m-%d %H:%M:%S')
    return date_time_str


# 분(minute) 단위로 계산 한다,
def datetime_minus(date_time_obj, hour):
    date_time_new = date_time_obj - datetime.timedelta(hours=hour)
    return date_time_new


def main(argv):
    parser = argparse.ArgumentParser(description='옵션 지정 방법')
    parser.add_argument('--count', required=False, default=1440, help='수집 data 갯수 (default=10000)')
    parser.add_argument('--symbol', required=False, default='btc', help='심볼 (BTC, ETH, ADA, ..., default=all)')
    parser.add_argument('--interval', required=False, default='minute1',
                        help='candle 종류 (day, week, month, minute1, ...)')
    parser.add_argument('--enddate', required=False, default=None, help='종료 일자(yyyy-mm-dd, default=현재 일자)')
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

    if interval.upper().startswith("MIN"):
        dt_obj = str_to_datetime(to)
        dt_new = datetime_minus(dt_obj, 9)
        to = datetime_to_str(dt_new)

    view(symbol, count, interval, to)


if __name__ == "__main__":
    main(sys.argv)

# py view_graph.py --count=1440 --interval=minute1 --symbol=eth --enddate=2022-09-14
