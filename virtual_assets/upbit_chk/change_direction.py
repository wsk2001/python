# -*- coding: utf-8 -*-

"""
코인 포지션이 전환되는 일자와 등락%의 평균값을 구하는 App
업비트 원화마켓 의 모든 코인이 기준입니다.
"""

import time, sys, getopt
import pyupbit
from datetime import datetime

open_p = 0
high_p = 1
low_p = 2
close_p = 3

# 추세 전환 평균 일자 구하기
def change_direction(v):
    ticker = v
    if not ticker.upper().startswith('KRW-'):
        ticker = 'KRW-' + v.upper()

    df = pyupbit.get_ohlcv(ticker, count=10000, period=1)
    values = df.values.tolist()

    plus_lst = []
    minus_lst = []
    plus_per = []
    minus_per = []
    plus_lst.clear()
    minus_lst.clear()

    plus_per.clear()
    minus_per.clear()

    change_flag = 0
    duration = 0
    per = 0

    for i in range(len(values)):
        rc = ((values[i][close_p] / values[i][open_p]) - 1) * 100.0

        if i == 0:
            duration += 1
            per += rc
            if 0 < rc:
                change_flag = 1
            else:
                change_flag = -1
            continue

        if 0 < rc:
            if change_flag == 1: # plus -> plus
                duration += 1
                per += rc
                continue
            if change_flag == -1: # minus -> plus (change)
                minus_lst.append(duration * -1)
                minus_per.append(per)
                duration = 1
                per = rc
                change_flag = 1
                continue

        elif rc < 0:
            if change_flag == -1: # minus -> minus
                duration += 1
                per += rc
                continue
            if change_flag == 1: # plus -> minus (change)
                plus_lst.append(duration)
                plus_per.append(per)
                duration = 1
                per = rc
                change_flag = -1
                continue

    return plus_lst, minus_lst, plus_per, minus_per


def check_direction():
    lst = pyupbit.get_tickers(fiat="KRW")

    print('symbol, plus->minus days, plus->minus %, minus->plus days, minus->plus %')
    for v in lst:
        lp, lm, plus_per, minus_per = change_direction(v)

        pc = (sum(lp, 0.0) / len(lp))
        mc = (sum(lm, 0.0) / len(lm)) * -1

        pp = (sum(plus_per, 0.0) / len(plus_per))
        mp = (sum(minus_per, 0.0) / len(minus_per))

        print(f'{v[4:]}, {pc:.2f}, {pp:.2f}%, {mc:.2f}, {mp:.2f}%')
        time.sleep(0.1)

# change direction of days
def cd_days(v, days):
    ticker = v
    if not ticker.upper().startswith('KRW-'):
        ticker = 'KRW-' + v.upper()

    df = pyupbit.get_ohlcv(ticker, count=10000, period=1)
    values = df.values.tolist()

    plus_lst = []
    plus_lst.clear()

    cnt = 0
    detect = 0

    for i in range(len(values)):
        rc = ((values[i][close_p] / values[i][open_p]) - 1) * 100.0
        if rc < 0.0:
            cnt += 1
            if cnt < days:
                continue
            else:
                detect += 1
        elif 0.0 < rc:
            if days <= cnt:
                plus_lst.append(1)

            cnt = 0

    if 0 < detect:
        up_sum = sum(plus_lst, 0.0)
        up_rate = (up_sum / detect) * 100.0
        print(f'{v}, {days}, {detect}, {up_sum}, {up_rate:.2f}%')


def main(argv):
    # check_direction()

    lst = pyupbit.get_tickers(fiat="KRW")

    print('symbol, 연속 하락 일, 총 하락 수, 연속 하락 후 상승 수, 상슬률%')
    for v in lst:
        for i in range(10):
            cd_days(v[4:], i+1)
            time.sleep(0.1)

if __name__ == "__main__":
    main(sys.argv)
