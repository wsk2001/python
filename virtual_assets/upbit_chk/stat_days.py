import calendar
import getopt
import locale
import sys
from time import sleep
from datetime import datetime

import pyupbit


class StatEarn:
    """
    StatEarn Class
    """

    def __init__(self, plus, minus):
        self._plus = plus
        self._minus = minus
        self._calc = plus - minus

    def inc_plus(self):
        self._plus += 1
        self._calc = self._plus - self._minus

    def inc_minus(self):
        self._minus += 1
        self._calc = self._plus - self._minus

    def get_earn(self):
        return self._plus, self._minus, self._calc


def analyze_day(v, count):
    df = pyupbit.get_ohlcv(v, interval='day', count=count, period=1)
    lst = [StatEarn(0,0) for i in range(31)]
    start_flag = 0
    start_date = ''
    end_date = ''
    for ind, row in df.iterrows():
        earn = ((row["close"] / row["open"]) - 1.0) * 100.0
        idx = int(str(ind)[8:10])
        if start_flag == 0:
            start_flag = 1
            start_date = str(ind)
        end_date = str(ind)

        if 0 < earn:
            lst[idx-1].inc_plus()
        else:
            lst[idx-1].inc_minus()

    print(v, start_date[:10], '~', end_date[:10])
    print('day : plus, minus, sum')
    i = 1
    pt = 0
    mt = 0
    ct = 0
    for l in lst:
        p, m, c = l.get_earn()
        pt += p
        mt += m
        ct += c
        print(i, ':',  str(p)+',', '-'+str(m)+',', str(c))
        i += 1

    print('total', ':',  str(pt)+',', '-'+str(mt)+',', str(ct))


def get_ticker_list():
    return pyupbit.get_tickers(fiat="KRW")


def main(argv):
    cnt = 60

    try:
        opts, etc_args = getopt.getopt(argv[1:], "hc:"
                                       , ["help", "count="])

    except getopt.GetoptError:
        print('usage:', argv[0], '-c <days>')
        print('ex) python', f'{argv[0]}', '-c 365')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('usage:', argv[0], '-c <days>')
            print('ex) python', f'{argv[0]}', '-c 365')
            print('')
            sys.exit()

        elif opt in ("-c", "--count"):  # count
            cnt = int(arg.strip())

    lst = get_ticker_list()

    # i = 1
    for v in lst:
        analyze_day(v, cnt)
        sleep(0.2)
        # i += 1
        # if 2 < i:
        #     break


if __name__ == "__main__":
    main(sys.argv)
