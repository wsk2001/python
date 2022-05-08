import datetime
import getopt
import configparser
import openpyxl as xl
import sys
import time
import pybithumb

def hot_tickers(rate):
    tks = pybithumb.get_tickers()
    for t in tks:
        res = pybithumb.Bithumb.get_ohlc(t)
        o = res.get(t)[0]
        c = res.get(t)[3]
        r = (c - o) / o * 100.0

        if rate <= r:
            print('{}: {}, {}, {:0.3f}%'
                  .format(t, o, c, r))
        time.sleep(0.1)

def cool_tickers(rate):
    pass

def main(argv):
    hot_tickers(7.0)
    cool_tickers(-3.0)


if __name__ == "__main__":
    main(sys.argv)
