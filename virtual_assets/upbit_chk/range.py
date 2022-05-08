import time
import datetime
import sys, getopt
import pyupbit
from time import sleep
import requests
from pandas import Series, DataFrame

open_posi = 0
close_position = 3

def cur_rate(v, h, l):
    df = pyupbit.get_ohlcv(v, count=1)
    lst = df.values.tolist()
    start_amt = lst[0][open_posi]
    end_amt = lst[0][close_position]
    rate = ((end_amt / start_amt) - 1.0) * 100.0

    if l <= rate <= h:
        print(f'{v[4:]}: {start_amt:.3f}  {end_amt:.3f} {rate:.3f}%')

def get_ticker_list():
    return pyupbit.get_tickers(fiat="KRW")

def main(argv):
    upper = 1.0
    lower = -1.0
    try:
        opts, etc_args = getopt.getopt(argv[1:], "hu:l:", ["upper=", "lower="])

    except getopt.GetoptError:
        print(argv[0], '-u <upper limit> -l <low limit>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(argv[0], '-u <upper limit> -l <low limit>')
            sys.exit()

        elif opt in ("-u", "--upper"):  # befor day count
            upper = float(arg.strip()) * 1.0

        elif opt in ("-l", "--lower"):  # befor day count
            lower = float(arg.strip()) * 1.0


    lst = get_ticker_list()
    for v in lst:
        sleep(0.3)
        cur_rate(v, upper, lower)


if __name__ == "__main__":
    main(sys.argv)
