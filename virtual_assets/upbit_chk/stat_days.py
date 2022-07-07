#-*- coding:utf-8 -*-

import getopt
import sys
from time import sleep
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

    print('total', 'plus:' + str(pt)+',', 'minus:' + '-'+str(mt)+',', 'sum:' + str(ct))
    print('')


def get_ticker_list():
    return pyupbit.get_tickers(fiat="KRW")


def main(argv):
    cnt = 60
    lst = []

    lst.clear()

    try:
        opts, etc_args = getopt.getopt(argv[1:], "hc:a:f:"
                                       , ["help", "count=", "all=", "filename="])

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

        elif opt in ("-a", "--all"):  # count
            lst = get_ticker_list()

        elif opt in ("-f", "--filename"):  # count
            filename = arg.strip()
            file = open(filename, "r", encoding='UTF8')
            lines = file.readlines()

            for l in lines:
                line = l.strip()
                if not line:
                    continue

                if line.startswith("#") or line.startswith("//"):
                    continue

                if len(line) <= 0:
                    continue

                tickers = line.split()
                for ticker in tickers:
                    if ticker.upper().startswith('KRW-'):
                        lst.append(ticker.upper())
                    else:
                        lst.append('KRW-' + ticker.upper())

            file.close()

    for v in lst:
        analyze_day(v, cnt)
        sleep(0.2)


if __name__ == "__main__":
    main(sys.argv)


# 정해진 기간 동안 몇일 오르고 몇일 내렸는지 확인