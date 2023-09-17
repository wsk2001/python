import time
import datetime
import sys, getopt
import pyupbit
import matplotlib.pyplot as plt
import argparse

# 한글 폰트 사용을 위해서 세팅 (아래 4줄)
from matplotlib import font_manager, rc

font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)


def AddStochastic(priceData, period=9, screen_window=3, slow_window=3):
    ndayhigh = priceData['high'].rolling(window=period, min_periods=1).max()
    ndaylow = priceData['low'].rolling(window=period, min_periods=1).min()
    fast_k = (priceData['close'] - ndaylow) / (ndayhigh - ndaylow) * 100
    fast_d = fast_k.rolling(window=screen_window).mean()
    slow_k = fast_k.rolling(window=slow_window).mean()
    slow_d = fast_d.rolling(window=slow_window).mean()
    return priceData.assign(slow_k=slow_k, slow_d=slow_d).dropna().copy()


def view(v, cnt, interval=None, to=None, disp='yes', save='yes'):
    if v.capitalize().startswith('KRW-'):
        df = pyupbit.get_ohlcv(v, count=cnt)
    else:
        df = pyupbit.get_ohlcv('KRW-' + v, interval=interval, to=to, count=cnt)

    df = AddStochastic(df, 9, 3, 3)

    sl_k = df['slow_k']
    sl_d = df['slow_d']
    ax = plt.gca()
    sl_d.plot(kind='line', x='name', y='currency', color='blue', label='%D', ax=ax)
    sl_k.plot(kind='line', x='name', y='currency', color='red', label='%K', ax=ax)
    plt.legend()

    if to is not None:
        plt.title(f'스토캐스틱: {v} ({str(to)[:10]}) interval={interval}')
    else:
        plt.title(f'스토캐스틱: {v} ({str(datetime.datetime.now())[:10]}) interval={interval}')

    plt.grid(True)

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
    parser.add_argument('-c', '--count', required=False, default=60, help='수집 data 갯수 (default=10000)')
    parser.add_argument('-s', '--symbol', required=False, default='ada', help='심볼 (BTC, ETH, ADA, ..., default=all)')
    parser.add_argument('-i', '--interval', required=False, default='day',
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

# py stocastic_chart.py --count=60 --interval=day --symbol=TT
