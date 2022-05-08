# -*- Encoding: UTF-8 -*- #

from datetime import date, timedelta
import sys, getopt
import pyupbit
from time import sleep
import getopt
import sys, time

op = 0
cp = 3

def rcmd(v, days=10, up=7):
    df = pyupbit.get_ohlcv(v, count=days, period=1)
    lst = df.values.tolist()
    up_cnt = 0

    fo = 0
    lc = 0
    i = 0
    for t in lst:
        if i == 0:
            fo = t[op]
            i += 1
        if t[op] < t[cp]:
            up_cnt += 1
        lc = t[cp]

    if up <= up_cnt:
        earn = ((lc / fo) - 1.0) * 100.0
        print(v[4:]+',', str(up_cnt)+',', str(fo)+',', str(lc)+',', f'{earn:6.2f}', '%')


def get_ticker_list():
    return pyupbit.get_tickers(fiat="KRW")


def main(argv):
    days = 10
    up_cnt = 7

    try:
        opts, etc_args = getopt.getopt(argv[1:], "hd:u:"
                                       , ["help", "days=", "upcount="])

    except getopt.GetoptError:
        print(argv[0], '-d <day count> -u <up count>')
        print('ex) python', f'{argv[0]}', '-d 10 -u 7')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(argv[0], '-d <day count> -u <up count>')
            print('ex) python', f'{argv[0]}', '-d 10 -u 7')
            sys.exit()

        elif opt in ("-d", "--days"):  # days
            days = int(arg.strip())

        elif opt in ("-u", "--upcount"):  # up count
            up_cnt = int(arg.strip())

    print('check days:', str(days), ' up count:', str(up_cnt))
    print('종목, 상승일수,', str(days) + ' 일전 시가, 종가(현재가), 상승률', )
    lst = get_ticker_list()
    for v in lst:
        sleep(0.2)
        rcmd(v, days, up_cnt)

if __name__ == "__main__":
    main(sys.argv)
