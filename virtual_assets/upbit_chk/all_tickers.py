import time, datetime, sys, getopt
import pyupbit
import pandas as pd

def save_ticker(v):
    df = pyupbit.get_ohlcv(v, count=3000, period=1)
    f = open('./data_files/' + v + '_' + datetime.datetime.now().strftime('%Y%m%d') + '.txt', 'w')
    print(v, file=f)
    print(df, file=f)
    print(v)
    f.close()

def save_ticker_cur(v):
    df = pyupbit.get_ohlcv(v, count=1)
    o = df['open'][0]
    h = df['high'][0]
    l = df['low'][0]
    c = df['close'][0]
    vol = df['volume'][0]
    p = ((c / o) - 1.0) * 100.0

    df = pyupbit.get_ohlcv(v, count=1, period=1)
    d = datetime.datetime.now().strftime('%Y%m%d')
    f = open(d + '.txt', 'a')
    print(d, v, o, h, l, c, vol, f'{p:3.2f}',  file=f)
    print(d, v, o, h, l, c, vol, f'{p:3.2f}')
    f.close()

def main(argv):
    pd.set_option('display.max_rows', 3500)
    lst = pyupbit.get_tickers(fiat="KRW")

    for v in lst:
        time.sleep(0.1)
        save_ticker(v)
        # save_ticker_cur(v)


if __name__ == "__main__":
    main(sys.argv)
