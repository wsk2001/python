# -*- coding: utf-8 -*-

"""
주어진 기간동안 모든 종목의 실적을 조회 한다.
"""

import time, sys, getopt
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
    lst = pyupbit.get_tickers(fiat="KRW")
    lst.sort()

    print('심볼, 시가, 종가, 실적, 표준편차율')
    for v in lst:
        start, end, earn, stdev = check_earning(v, 28)
        print(v[4:]+',', f'{start}, {end}, {earn:.2f}%, {stdev:.2f}')
        time.sleep(0.1)


if __name__ == "__main__":
    main(sys.argv)
