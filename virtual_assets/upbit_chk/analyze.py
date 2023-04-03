import time
import datetime
import sys, getopt
import pyupbit
from time import sleep

open_posi = 0
close_posi = 3


def earning(t):
    if not t.upper().startswith('KRW-'):
        t = 'KRW-' + t
    df = pyupbit.get_ohlcv(t, interval='day', count=1, period=1)
    if df is None:
        return 0

    # ohlcv
    v = df.values.tolist()
    if v[0][close_posi] < v[0][open_posi]:
        return -1
    elif v[0][open_posi] < v[0][close_posi]:
        return 1
    else:
        return 0


def get_ticker_list():
    return pyupbit.get_tickers(fiat="KRW")


def main(argv):
    sleep_min = 10
    try:
        opts, etc_args = getopt.getopt(argv[1:], "hs:", ["sleep="])

    except getopt.GetoptError:
        print(argv[0], '-s <sleep minutes>')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(argv[0], '-s <sleep minutes>')
            sys.exit()

        elif opt in ("-s", "--sleep"):
            sleep_min = int(arg.strip())

    now = time
    print("업비트 원화 마켓", now.strftime('%m-%d'))

    while True:
        total_count = 0
        plus_count = 0
        minus_count = 0

        lst = get_ticker_list()

        for v in lst:
            total_count += 1
            sleep(0.2)
            i = earning(v)
            if i == 1:
                plus_count += 1
            elif i == -1:
                minus_count += 1

        now = time
        print(now.strftime('%H:%M:%S'),
              "상승:" + str(plus_count),
              ", 하락:" + str(minus_count),
              ", 종목수 : " + str(total_count))

        sleep(sleep_min * 60)


if __name__ == "__main__":
    main(sys.argv)
