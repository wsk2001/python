import time
import datetime
import sys, getopt
import pyupbit
from pandas import Series, DataFrame
import matplotlib.pyplot as plt

def view(v, cnt):
    if v.capitalize().startswith('KRW-'):
        df = pyupbit.get_ohlcv(v, count=cnt)
    else:
        df = pyupbit.get_ohlcv('KRW-' + v, interval='minute1', count=cnt)
    dfs = df['close']
    ax = plt.gca()
    dfs.plot(kind='line', x='name', y='currency', ax=ax)
    plt.title(v)
    plt.show()

def main(argv):
    ticker = 'KRW-BTC'
    count = 1440
    try:
        opts, etc_args = getopt.getopt(argv[1:], "ht:c:", ["help", "ticker=", "count="])

    except getopt.GetoptError:
        print(argv[0], '-t <ticker symbol> -c <count>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(argv[0], '-t <ticker symbol> -c <count>')
            sys.exit()

        elif opt in ("-t", "--ticker"):  # ticker symbol
            ticker = arg

        elif opt in ("-c", "--count"):  # ticker symbol
            count = int(arg.strip())

    view(ticker, count)


if __name__ == "__main__":
    main(sys.argv)

# python view_graph.py -t SXP
