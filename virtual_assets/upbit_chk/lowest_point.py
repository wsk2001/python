import time
import datetime
import sys, getopt
import pyupbit
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
import pandas as pd

def view(t, to_time):

    if t.capitalize().startswith('KRW-'):
        df = pyupbit.get_ohlcv(t, interval='minute1', count=1440, to=to_time, period=1)
    else:
        df = pyupbit.get_ohlcv('KRW-' + t, interval='minute1', count=1440, to=to_time, period=1)

    indexs = df.index.tolist()
    values = df.values.tolist()

    hv = 0.0
    lv = 0.0
    ht = ''
    lt = ''

    i = 0
    for v in values:
        if lv == 0.0:
            lv = v[0]
        if v[0] < lv:
            lv = v[0]
            lt = indexs[i]
        if hv < v[0]:
            hv = v[0]
            ht = indexs[i]
        i += 1

    print('low:', lt, lv, ', high:', ht, hv)


def main(argv):
    ticker = 'btc'
    lasttime = " 23:59:59"
    lastdate = datetime.datetime.now().strftime('%Y%m%d')
    pd.set_option('display.max_rows', 16000)
    try:
        opts, etc_args = getopt.getopt(argv[1:], "ht:l:"
                                       , ["help", "ticker=", "lastdate="])

    except getopt.GetoptError:
        print(argv[0], '-t <ticker symbol> -l <last date>')
        print('ex) python', f'{argv[0]}', '-t iost', f'{lastdate}')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(argv[0], '-t <ticker symbol> -l <last date>')
            print('ex) python', f'{argv[0]}', '-t iost', f'{lastdate}')
            sys.exit()

        elif opt in ("-t", "--ticker"):  # ticker symbol
            ticker = arg

        elif opt in ("-l", "--lastdate"):  # lastdate
            lastdate = arg.strip()

    if lastdate is not None:
        lastdate = lastdate + lasttime

    view(ticker, lastdate)


if __name__ == "__main__":
    main(sys.argv)

# python .\oneday_flow.py -t iost -l "20211206"

