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

    dfs = df['close']
    #hds = df['high']
    ax = plt.gca()
    dfs.plot(kind='line', x='name', y='currency', label='close', ax=ax)
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


def view_2_axes(v, cnt, interval=None, to=None, disp='yes', save='no'):
    ticker = v
    if v.upper().startswith('KRW-') or  v.upper().startswith('BTC-'):
        ticker = v
    else:
        ticker = 'KRW-' + v

    df = pyupbit.get_ohlcv(ticker, interval=interval, to=to, count=cnt)

    fig, ax1 = plt.subplots()
    plt.grid(True)

    color_1 = 'tab:blue'
    ax1.set_title(f'{ticker.upper()[4:]}, interval={interval} ({str(to)[:10]})', fontsize=16)
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Close (blue)', fontsize=14, color=color_1)
    ax1.plot(df.index, df.close, color=color_1)
    #ax1.plot(df.index, df.close, marker='s', color=color_1)
    ax1.tick_params(axis='y', labelcolor=color_1)

    # right side with different scale
    ax2 = ax1.twinx() # instantiate a second axes that shares the same x-axis
    color_2 = 'tab:red'
    ax2.set_ylabel('Volume (red)', fontsize=14, color=color_2)

    # 바 차트
    ax2.bar(df.index, df.volume, color=color_2)

    # 라인 차트
    #ax2.plot(df.index, df.volume, color=color_2)
    # ax2.plot(df.index, df.volume, marker='o', color=color_2)
    ax2.tick_params(axis='y', labelcolor=color_2)

    # 3개도 가능
    # ax3 = ax1.twinx() # instantiate a second axes that shares the same x-axis
    # color_3 = 'tab:green'
    # ax3.set_ylabel('High (green)', fontsize=14, color=color_3)
    # ax3.plot(df.index, df.high, color=color_3)
    # ax3.tick_params(axis='y', labelcolor=color_3)

    fig.tight_layout()
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
    parser.add_argument('--endtime', required=False, default='09:00:00', help='종료 시각(hh:mm:ss, default=현재 시각)')

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
    #view_2_axes(symbol, count, interval, to)


if __name__ == "__main__":
    main(sys.argv)

# py vg.py --symbol=ENJ --enddate=2023-04-08