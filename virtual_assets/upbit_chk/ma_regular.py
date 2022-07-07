import time
import datetime
import sys, getopt
import pyupbit
from time import sleep
import requests
from pandas import Series, DataFrame

to_interval = {'m240': 'minute240',
          'm60': 'minute60',
          'm30': 'minute30',
          'm15': 'minute15',
          'm10': 'minute10',
          'm5': 'minute5',
          'm3': 'minute3',
          'm1': 'minute1',
          'day': 'day'
          }


def get_ma(df, n):
    return df['close'].rolling(window=n).mean()


def check_ma(t, cnt, i):
    if not t.upper().startswith('KRW-'):
        t = 'KRW-' + t
    df = pyupbit.get_ohlcv(t, interval=i, count=cnt, period=1)
    ma5 = get_ma(df, 5)[-1]
    ma20 = get_ma(df, 20)[-1]
    ma60 = get_ma(df, 60)[-1]

    if ma5 > ma20 > ma60:
        print(f'{t[4:]}, {ma5:.2f}, {ma20:.2f}, {ma60:.2f}')


def get_ticker_list():
    return pyupbit.get_tickers(fiat="KRW")


def usage(app):
    print('python', app, '-c <count> -i <interval>')
    print('<interval>')
    print('\t\t\t minutes option: m240, m60, m30, m15, m10, m5, m3, m1')
    print('\t\t\t day option: day')
    print('ex) python', app, '-c 180 -i m240')
    print('ex) python', app, '-c 180 -i day')
    sys.exit()


def main(argv):
    global to_interval
    count = 180
    interval = 'day'
    try:
        opts, etc_args = getopt.getopt(argv[1:], "hc:i:", ["count=", "interval="])

    except getopt.GetoptError:
        usage(argv[0])

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage(argv[0])

        elif opt in ("-c", "--count"):
            count = int(arg.strip())

        elif opt in ("-i", "--interval"):
            tmp = arg.strip()
            interval = to_interval[tmp]

    if count < 90:
        count = 90

    lst = get_ticker_list()

    print('업비트 이평선 정배열 종목(interval=', interval, ') MA5, MA20, MA60')
    print('')
    for t in lst:
        sleep(0.3)
        check_ma(t, count, interval)


if __name__ == "__main__":
    main(sys.argv)
