import calendar
import getopt
import sys, time
import pyupbit
from common.utils import market_code, get_interval
from datetime import datetime


class in_a_row:
    def __init__(self):
        self.count = 0
        self.start = ''
        self.end = ''
        self.open_p = 0
        self.close_p = 0

    def clean(self):
        self.count = 0
        self.start = ''
        self.end = ''
        self.open_p = 0
        self.close_p = 0

open_p = 0
close_p = 3

def view_in_a_row(r):
    print(r.count, r.start, r.end)


def check(ticker, cnt, interval='day'):
    if not ticker.startswith('KRW-'):
        ticker = 'KRW-' + ticker

    print(ticker)

    df = pyupbit.get_ohlcv(ticker, interval=interval, count=cnt, period=1)
    values = df.values.tolist()
    indexs = df.index.tolist()

    ov = in_a_row()
    nv = in_a_row()

    print('start date:', str(indexs[0])[:10])
    for i in range(len(values)):
        if values[i][close_p] > values[i][open_p]:
            if nv.count == 0:
                nv.start = str(indexs[i])[:10]
                nv.open_p = values[i][open_p]
            else:
                nv.end = str(indexs[i])[:10]
                nv.close_p = values[i][close_p]
            nv.count += 1
            # view_in_a_row(nv)

        else:
            if 5 < nv.count:
                rc = ((nv.close_p / nv.open_p) - 1) * 100.0
                print(nv.count, nv.start, nv.end, nv.open_p, nv.close_p, f'{rc:.3f}%')

            if ov.count < nv.count:
                ov.count = nv.count
                ov.start = nv.start
                ov.end = nv.end
                ov.open_p = nv.open_p
                ov.close_p = nv.close_p

            nv.clean()

    if 5 < nv.count:
        rc = ((nv.close_p / nv.open_p) - 1) * 100.0
        print(nv.count, nv.start, nv.end, nv.open_p, nv.close_p, f'{rc:.3f}%')

    if ov.count < nv.count:
        ov.count = nv.count
        ov.start = nv.start
        ov.end = nv.end
        ov.open_p = nv.open_p
        ov.close_p = nv.close_p

    print('')
    rc = ((ov.close_p / ov.open_p) - 1) * 100.0
    print(ov.count, ov.start, ov.end, ov.open_p, ov.close_p, f'{rc:.3f}%')
    print('')


def main(argv):
    cnt = 365
    interval = 'day'
    ticker = 'btc'

    try:
        opts, etc_args = getopt.getopt(argv[1:], "hc:t:i:"
                                       , ["help", "count=", "ticker=", "interval"])

    except getopt.GetoptError:
        print(argv[0], '-c <count> -t <ticker symbol> -i <interval>')
        print('ex) python', argv[0], '-c 7 -t bat')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(argv[0], '-c <count> -t <ticker symbol> -i <interval>')
            print('ex) python', argv[0], '-c 7 -t bat -i day')
            print('ex) python', argv[0], '-c 7 -t bat -i m15')
            sys.exit()

        elif opt in ("-t", "--ticker"):  # ticker symbol
            ticker = arg.strip().upper()

        elif opt in ("-c", "--count"):  # count
            cnt = int(arg.strip())

        elif opt in ("-i", "--interval"):  # interval
            interval = arg.strip()

    check(ticker, cnt, interval)
    print('')


if __name__ == "__main__":
    main(sys.argv)

