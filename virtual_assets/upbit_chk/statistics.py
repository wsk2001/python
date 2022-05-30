import calendar
import getopt
import locale
import sys
from time import sleep
from datetime import datetime

import pyupbit


def what_day_is_it(date):
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    day = date.weekday()
    return days[day]


def analyze_day(v, count):
    df = pyupbit.get_ohlcv(v, interval='day', count=count, period=1)

    stat = {'Mon': 0, 'Tue': 0, 'Wed': 0, 'Thu': 0, 'Fri': 0, 'Sat': 0, 'Sun': 0}
    plus_cnt = 0
    minus_cnt = 0

    for ind, row in df.iterrows():
        wd = what_day_is_it(ind.to_pydatetime())
        earn = ((row["close"] / row["open"]) - 1.0) * 100.0
        if earn < 0:
            stat[wd] = stat[wd] - 1
            minus_cnt = minus_cnt + 1
        elif 0 < earn:
            stat[wd] = stat[wd] + 1
            plus_cnt = plus_cnt + 1

    return v, stat, plus_cnt, minus_cnt


def get_ticker_list():
    return pyupbit.get_tickers(fiat="KRW")


def main(argv):
    cnt = 1

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

    print('종목,', '월,', '화,', '수,', '목,', '금,', '토,', '일,', '상승,', '하락')

    for v in lst:
        rv, st, p, m = analyze_day(v, cnt)
        print(rv[4:]+',', str(st['Mon'])+',', str(st['Tue'])+',', str(st['Wed'])+',',
              str(st['Thu'])+',', str(st['Fri'])+',', str(st['Sat'])+',',
              str(st['Sun'])+',', str(p)+',', m)
        sleep(0.2)


if __name__ == "__main__":
    main(sys.argv)
