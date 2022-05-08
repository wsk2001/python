import calendar
import datetime
import getopt
import locale
import sys
import time

import pyupbit
from time import sleep
from common.utils import market_code, get_profit

def get_price_100():
    cl, _, _ = market_code()

    for t in cl:
        df = pyupbit.get_ohlcv(t, count=1)
        if 100 <= float(df['close'][0]) <= 999:
            print(t[4:], df['close'][0])
        time.sleep(0.1)

def main_(argv):
    cl, _, _ = market_code()
    days = 21

    print(len(cl))
    print(cl)

    try:
        opts, etc_args = getopt.getopt(argv[1:], "hd:"
                                       , ["help", "days"])

    except getopt.GetoptError:
        print(argv[0], '-d <days>')
        print('ex) python', f'{argv[0]}', '-d 365')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('ex) python', f'{argv[0]}', '-d 365')
            print('')
            sys.exit()

        elif opt in ("-d", "--days"):  # days
            days = int(arg.strip())

    dic_t = {}
    for t in cl:
        df = pyupbit.get_ohlcv(t, count=1)
        temp_dict = {t: df['close'][0]}
        dic_t.update(temp_dict)
        time.sleep(0.2)

    sd = dict(sorted(dic_t.items(), key=lambda item: item[1], reverse=True))

    for key in sd:
        df = pyupbit.get_ohlcv(key, count=days)
        cnt = len(df)
        profit = get_profit(df['open'][0], df['close'][cnt - 1])
        print(key[4:], df['open'][0], df['close'][cnt - 1], f'{profit:4.3f}%')
        time.sleep(0.2)


if __name__ == "__main__":
    get_price_100()
    # main(sys.argv)
