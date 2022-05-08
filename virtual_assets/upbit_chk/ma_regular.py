import time
import datetime
import sys, getopt
import pyupbit
from time import sleep
import requests
from pandas import Series, DataFrame

open_posi = 0
close_posi = 3

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

def main(argv):
    count = 180
    interval = 'day'
    try:
        opts, etc_args = getopt.getopt(argv[1:], "hc:i:", ["count=", "interval="])

    except getopt.GetoptError:
        print(argv[0], '-c <count> -i <interval>')
        print('<interval>')
        print('\t\t minute240, minute60, minute30, minute15, minute10, minute5, minute3, minute1')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(argv[0], '-c <count> -i <interval>')
            print('<interval>')
            print('\t\t minute240, minute60, minute30, minute15, minute10, minute5, minute3, minute1')
            sys.exit()

        elif opt in ("-c", "--count"):  # day count
            count = int(arg.strip())

        elif opt in ("-i", "--interval"):  # interval = day, minute240, minute60, ...
            interval = arg.strip()

    if count < 90:
        count = 90

    lst = get_ticker_list()

    print('업비트 이평선 정배열 종목(interval=',interval, ') MA5, MA20, MA60')
    print('')
    for t in lst:
        sleep(0.3)
        check_ma(t, count, interval)

if __name__ == "__main__":
    main(sys.argv)
