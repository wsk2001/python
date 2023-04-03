import time
import datetime
import sys, getopt
import pyupbit
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import argparse

# 한글 폰트 사용을 위해서 세팅 (아래 4줄)
from matplotlib import font_manager, rc
font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

def view(v, cnt, interval=None, to=None, disp='yes', save='no'):
    ticker = v
    if v.upper().startswith('KRW-') or  v.upper().startswith('BTC-'):
        ticker = v
    else:
        ticker = 'KRW-' + v

    df = pyupbit.get_ohlcv(ticker, interval=interval, to=to, count=cnt)

    dfs = df['volume']
    #hds = df['high']
    ax = plt.gca()
    dfs.plot(kind='line', x='name', y='currency', label='volume', ax=ax)
    #hds.plot(kind='line', x='name', y='currency', label='high', ax=ax)
    plt.legend()

    if interval == None:
        plt.title(f'{ticker.upper()[4:]} ({str(to)[:10]})')
    else:
        plt.title(f'{ticker.upper()[4:]}, interval={interval} ({str(to)[:10]})')

    plt.grid(True)
    #figure(figsize=(8, 6))

    # Image 가 작게 저장됨.

    if save.lower().startswith('yes'):
        # manager = plt.get_current_fig_manager()
        # manager.frame.Maximize(True) # AttributeError: 'FigureManagerTk' object has no attribute 'frame'
        # manager.window.state('zoomed')
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

    if enddate is None:
        enddate = datetime.datetime.now().strftime('%Y-%m-%d')

    if enddate is not None and endtime is None:
        to = enddate + ' ' + '17:59:00'

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

# py view_graph.py --count=1440 --interval=minute1 --symbol=bora --enddate=2022-09-19 --endtime=15:44:00
