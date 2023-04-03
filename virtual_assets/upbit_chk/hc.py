import time
import datetime
import sys, getopt
import pyupbit
from time import sleep
import requests
from pandas import Series, DataFrame

open_posi = 0
close_position = 3

def check_hot(v, check_rate):
    df = pyupbit.get_ohlcv(v, count=1)
    lst = df.values.tolist()
    start_amt = lst[0][open_posi]
    end_amt = lst[0][close_position]
    rate = ((end_amt / start_amt) - 1.0) * 100.0

    if start_amt < end_amt:
        if check_rate <= rate:
            print(f'{v[4:]}: {start_amt:.2f}  {end_amt:.2f} {rate:.2f}%')

def check_cool(v, check_rate):
    df = pyupbit.get_ohlcv(v, count=1)
    lst = df.values.tolist()

    curr_start_amt = lst[0][open_posi]
    curr_end_amt = lst[0][close_position]
    curr_rate = ((curr_end_amt / curr_start_amt) - 1.0) * 100.0

    if curr_rate <= check_rate:
        print(f'{v[4:]}: {curr_start_amt:.2f}  {curr_end_amt:.2f} {curr_rate:.2f}%')

def get_ticker_list():
    return pyupbit.get_tickers(fiat="KRW")

def main(argv):
    check_rate = -1.0
    try:
        opts, etc_args = getopt.getopt(argv[1:], "hr:", ["rate="])

    except getopt.GetoptError:
        print(argv[0], '-r <rate>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(argv[0], '-r <rate>')
            sys.exit()

        elif opt in ("-r", "--rate"):  # befor day count
            check_rate = float(arg.strip())

    lst = get_ticker_list()

    print('Hot tickers')
    if check_rate < 0.0 :
        check_rate *= -1.0
    for v in lst:
        sleep(0.3)
        check_hot(v, check_rate)

    print('')

    print('Cool tickers')
    if 0.0 < check_rate :
        check_rate *= -1.0
    for v in lst:
        sleep(0.3)
        check_cool(v, check_rate)


if __name__ == "__main__":
    main(sys.argv)
