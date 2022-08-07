# -*- coding: utf-8 -*-

"""
주어진 기간동안 모든 종목의 실적을 조회 한다.
"""

import time, sys, getopt, datetime
import pyupbit
import numpy

open_p = 0
high_p = 1
low_p = 2
close_p = 3


# 실적 구하기
def check_earning(v, cnt):
    ticker = v
    if not ticker.upper().startswith('KRW-'):
        ticker = 'KRW-' + v.upper()

    df = pyupbit.get_ohlcv(ticker, count=cnt, period=1)
    values = df.values.tolist()

    fst_open_value = 0
    lst_close_value = 0

    ls_vals = []
    ls_vals.clear()

    for i in range(len(values)):
        if i == 0:
            fst_open_value = values[i][open_p]
        lst_close_value = values[i][close_p]
        ls_vals.append(values[i][close_p])

    earning = (( lst_close_value / fst_open_value) - 1) * 100.0
    avg = numpy.mean(ls_vals)
    stdev = numpy.std(ls_vals)

    return fst_open_value, lst_close_value, earning, (stdev/avg)*100


def main(argv):
    days = 28
    lst = pyupbit.get_tickers(fiat="KRW")
    lst.sort()

    try:
        opts, etc_args = getopt.getopt(argv[1:], "hd:", ["days="])

    except getopt.GetoptError:
        print(argv[0], '-d <days>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(argv[0], '-d <days>')
            sys.exit()

        elif opt in ("-d", "--days"):
            days = int(arg.strip())

    print()
    print(str(days) + '일 동안 실적, 작업일', '(' + datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + ')')
    print('일자는 옵션 -d 로 조정 가능')
    print()

    print('심볼, 시가, 종가, 실적, 표준편차율')
    for v in lst:
        start, end, earn, stdev = check_earning(v, days)
        print(v[4:]+',', f'{start}, {end}, {earn:.2f}%, {stdev:.2f}')
        time.sleep(0.1)


if __name__ == "__main__":
    main(sys.argv)
