import time
import datetime
import sys, getopt
import pyupbit
from time import sleep
import requests
from pandas import Series, DataFrame

open_posi = 0
close_posi = 3

def check_plus(t, cnt):
    if not t.upper().startswith('KRW-'):
        t = 'KRW-' + t
    df = pyupbit.get_ohlcv(t, interval='day', count=cnt, period=1)
    # ohlcv
    values = df.values.tolist()

    f = list()
    f.append(t[4:])

    plus = 0
    for v in values:
        if 0 < (v[close_posi] - v[open_posi]):
            plus += 1
            s = format(((v[close_posi] / v[open_posi]) - 1) * 100.0, ".2f")
            f.append(s)

    if cnt <= plus:
        print(f)

def get_ticker_list():
    return pyupbit.get_tickers(fiat="KRW")

def main(argv):
    count = 3
    try:
        opts, etc_args = getopt.getopt(argv[1:], "hc:", ["count="])

    except getopt.GetoptError:
        print(argv[0], '-c <count>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(argv[0], '-c <count>')
            sys.exit()

        elif opt in ("-c", "--count"):  # day count
            count = int(arg.strip())

    lst = get_ticker_list()

    for v in lst:
        sleep(0.3)
        check_plus(v, count)

if __name__ == "__main__":
    main(sys.argv)
