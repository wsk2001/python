# -*- coding: utf-8 -*-

"""
코인 포지션이 전환되는 일자와 등락%의 평균값을 구하는 App
업비트 원화마켓 의 모든 코인이 기준입니다.
"""

import time
import pyupbit
from datetime import datetime, date
from common.themes import get_themes, get_all_themes
from common.utils import get_idx_values, get_tickers
import argparse

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
            if change_flag == 1:  # plus -> plus
                duration += 1
                per += rc
                continue
            if change_flag == -1:  # minus -> plus (change)
                minus_lst.append(duration * -1)
                minus_per.append(per)
                duration = 1
                per = rc
                change_flag = 1
                continue

        elif rc < 0:
            if change_flag == -1:  # minus -> minus
                duration += 1
                per += rc
                continue
            if change_flag == 1:  # plus -> minus (change)
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


# 일정 기간 연속 하락 후 상승 할 확률 계산.
def cd_days(v, days, dfs=None):
    if dfs is None:
        ticker = v
        if not ticker.upper().startswith('KRW-'):
            ticker = 'KRW-' + v.upper()

        df = pyupbit.get_ohlcv(ticker, count=10000, period=1)
    else:
        df = dfs

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

    return df


# 일정 기간 연속 상승 후 하락 할 확률 계산.
def cd_days_minus(v, days, dfs=None):
    if dfs is None:
        ticker = v
        if not ticker.upper().startswith('KRW-'):
            ticker = 'KRW-' + v.upper()

        df = pyupbit.get_ohlcv(ticker, count=10000, period=1)
    else:
        df = dfs

    values = df.values.tolist()

    minus_lst = []
    minus_lst.clear()

    cnt = 0
    detect = 0

    for i in range(len(values)):
        rc = ((values[i][close_p] / values[i][open_p]) - 1) * 100.0
        if 0.0 < rc:
            cnt += 1
            if cnt < days:
                continue
            else:
                detect += 1
        elif rc < 0.0:
            if days <= cnt:
                minus_lst.append(1)

            cnt = 0

    if 0 < detect:
        up_sum = sum(minus_lst, 0.0)
        up_rate = (up_sum / detect) * 100.0
        print(f'{v}, {days}, {detect}, {up_sum}, {up_rate:.2f}%')

    return df


# 최근 7일중 마지막 2일 이상 상승한 종목 추출
def seven_days_plus(v):
    ticker = v
    if not ticker.upper().startswith('KRW-'):
        ticker = 'KRW-' + v.upper()

    df = pyupbit.get_ohlcv(ticker, count=7, period=1)

    cnt = 0
    op = '-'
    bef_rc = 0.0

    for ind, row in df.iterrows():
        # print(str(ind)[0:10]) # print date, time
        rc = ((row["close"] / row["open"]) - 1.0) * 100.0
        if 0.0 < rc:
            if bef_rc < rc:
                op = '+'
            else:
                op = '-'
            bef_rc = rc
            cnt += 1
        else:
            cnt = 0

    return cnt, op


def seven_days():
    lst = pyupbit.get_tickers(fiat="KRW")
    lst.sort()

    theme_dict = {}
    theme_dict.clear()

    themes = get_all_themes()
    for t in themes:
        theme_dict[t] = 0

    print(datetime.now())
    print('최근 1주일 중 마지막 일자 기준 연속 3일 이상 상승 종목')
    print('상승 추세는 마지막 일자의 상승률이 전일 상승률 보다 높을 경우 +, 아니면 -')
    print()
    print('symbol, up count, 상승 추세, [관련 테마]')
    for v in lst:
        cnt, op = seven_days_plus(v)
        if 3 <= cnt:
            _, tms = get_themes(v[4:])
            if len(tms):
                print(v[4:] + ',', cnt, ',', op, ',', tms)
            else:
                print(v[4:] + ',', cnt, ',', op)
            for t in tms:
                if not t.lower().startswith('unclassified'):
                    theme_dict[t] += 1

        time.sleep(0.1)

    print()
    for key, val in theme_dict.items():
        if 0 < val:
            print(key + ':', val)


# earning 만큼 오른 다음날 또를 확률 계산.
def shooting_next(v, earning):
    ticker = v
    if not ticker.upper().startswith('KRW-'):
        ticker = 'KRW-' + v.upper()

    df = pyupbit.get_ohlcv(ticker, count=10000, period=1)
    values = df.values.tolist()

    flag = False
    shooting_count = 0
    next_day_up = 0

    for i in range(len(values)):
        rc = ((values[i][close_p] / values[i][open_p]) - 1) * 100.0

        if 0.0 < rc:
            if flag:
                next_day_up += 1
                flag = False
        else:
            flag = False

        if earning <= rc:
            shooting_count += 1
            flag = True

    return shooting_count, next_day_up


def check_shooting(earning=20):
    lst = pyupbit.get_tickers(fiat="KRW")
    lst.sort()

    for v in lst:
        cnt, next_cnt = shooting_next(v, earning)
        if 0 < cnt:
            print(v[4:], cnt, next_cnt)


def view_hlc_stat(count=30, symbol='all', fiat='KRW', interval='day'):
    if symbol.startswith('all'):
        lst = get_tickers(fiat)
    else:
        if symbol.upper() != 'KRW' and symbol.upper() != 'BTC' and symbol.upper() != 'USDT':
            symbol = 'KRW-' + symbol.upper()
        lst = [symbol]

    for v in lst:
        dt, values, _ = get_idx_values(v, cnt=count, interval=interval)
        hv = 0.0
        lv = 0.0
        cv = 0.0
        for i in range(len(values)):
            hv += ((values[i][high_p] / values[i][open_p]) - 1) * 100.0
            lv += ((values[i][low_p] / values[i][open_p]) - 1) * 100.0
            cv += ((values[i][close_p] / values[i][open_p]) - 1) * 100.0
        cnt = len(values)
        if v.upper().startswith('USDT'):
            print(f'{v[5:]:<6}, {hv / cnt:.3f}, {lv / cnt:.3f}, {cv / cnt:.3f}')
        else:
            print(f'{v[4:]:<6}, {hv / cnt:.3f}, {lv / cnt:.3f}, {cv / cnt:.3f}')
        time.sleep(0.1)


def main():
    # check_direction()
    # lst = pyupbit.get_tickers(fiat="KRW")
    # lst.sort()

    parser = argparse.ArgumentParser(description='옵션 지정 방법')
    parser.add_argument('--count', required=False, default=10000, help='수집 data 갯수 (default=10000)')
    parser.add_argument('--symbol', required=False, default='all', help='심볼 (BTC, ETH, ADA, ..., default=all)')
    parser.add_argument('--fiat', required=False, default='KRW', help='자산 종류 (KRW, BTC, USDT, default=KRW)')
    parser.add_argument('--interval', required=False, default='day', help='candle 종류 (day, week, month, minute1, ...)')
    parser.add_argument('--earning', required=False, default=0.0, help='실적 (5.1, -5.2, 단위 %, default=0.0)')

    args = parser.parse_args()
    count = int(args.count)
    symbol = args.symbol
    fiat = args.fiat
    interval = args.interval
    earning = float(args.earning)

    view_hlc_stat(count, symbol, fiat, interval)
    # print()
    # seven_days()

    # check_shooting()

    # for v in lst:
    #     df = None
    #     for i in range(10):
    #         df = cd_days_minus(v[4:], i + 1, df)
    # -- or ---
    #         df = cd_days(v[4:], i + 1, df)
    #         time.sleep(0.1)


if __name__ == "__main__":
    main()
