import time
import datetime
import sys, getopt
import pyupbit
from time import sleep

open_posi = 0
close_posi = 3

chk_mins = ['00:01:00', '00:11:00', '00:21:00', '00:31:00', '00:41:00', '00:51:00',
            '01:01:00', '01:11:00', '01:21:00', '01:31:00', '01:41:00', '01:51:00',
            '02:01:00', '02:11:00', '02:21:00', '02:31:00', '02:41:00', '02:51:00',
            '03:01:00', '03:11:00', '03:21:00', '03:31:00', '03:41:00', '03:51:00',
            '04:01:00', '04:11:00', '04:21:00', '04:31:00', '04:41:00', '04:51:00',
            '05:01:00', '05:11:00', '05:21:00', '05:31:00', '05:41:00', '05:51:00',
            '06:01:00', '06:11:00', '06:21:00', '06:31:00', '06:41:00', '06:51:00',
            '07:01:00', '07:11:00', '07:21:00', '07:31:00', '07:41:00', '07:51:00',
            '08:01:00', '08:11:00', '08:21:00', '08:31:00', '08:41:00', '08:51:00',
            '09:01:00', '09:11:00', '09:21:00', '09:31:00', '09:41:00', '09:51:00',
            '10:01:00', '10:11:00', '10:21:00', '10:31:00', '10:41:00', '10:51:00',
            '11:01:00', '11:11:00', '11:21:00', '11:31:00', '11:41:00', '11:51:00',
            '12:01:00', '12:11:00', '12:21:00', '12:31:00', '12:41:00', '12:51:00',
            '13:01:00', '13:11:00', '13:21:00', '13:31:00', '13:41:00', '13:51:00',
            '14:01:00', '14:11:00', '14:21:00', '14:31:00', '14:41:00', '14:51:00',
            '15:01:00', '15:11:00', '15:21:00', '15:31:00', '15:41:00', '15:51:00',
            '16:01:00', '16:11:00', '16:21:00', '16:31:00', '16:41:00', '16:51:00',
            '17:01:00', '17:11:00', '17:21:00', '17:31:00', '17:41:00', '17:51:00',
            '18:01:00', '18:11:00', '18:21:00', '18:31:00', '18:41:00', '18:51:00',
            '19:01:00', '19:11:00', '19:21:00', '19:31:00', '19:41:00', '19:51:00',
            '20:01:00', '20:11:00', '20:21:00', '20:31:00', '20:41:00', '20:51:00',
            '21:01:00', '21:11:00', '21:21:00', '21:31:00', '21:41:00', '21:51:00',
            '22:01:00', '22:11:00', '22:21:00', '22:31:00', '22:41:00', '22:51:00',
            '23:01:00', '23:11:00', '23:21:00', '23:31:00', '23:41:00', '23:51:00'
            ]


def earning(t, to):
    if not t.upper().startswith('KRW-'):
        t = 'KRW-' + t

    if to[11:] < '09:00:00':
        dfs = pyupbit.get_ohlcv(t, interval='day', count=2, period=1, to=to[:10])
    else:
        dfs = pyupbit.get_ohlcv(t, interval='day', count=1, period=1, to=to[:10])

    dft = pyupbit.get_ohlcv(t, interval='minute1', count=1, period=1, to=to)

    # ohlcv
    vs = dfs.values.tolist()
    vt = dft.values.tolist()
    if vt[0][close_posi] < vs[0][open_posi]:
        return -1
    elif vs[0][open_posi] < vt[0][close_posi]:
        return 1
    else:
        return 0


def get_ticker_list():
    return pyupbit.get_tickers(fiat="KRW")


def main(argv):
    str_day = "2022-06-03 "
    lst = get_ticker_list()
    print("업비트 원화 마켓 종목수 : " + str(len(lst)))

    for m in chk_mins:
        total_count = 0
        plus_count = 0
        minus_count = 0

        for v in lst:
            total_count += 1
            sleep(0.3)
            i = earning(v, str_day + m)
            if i == 1:
                plus_count += 1
            elif i == -1:
                minus_count += 1

        print(str_day + m, "상승:" + str(plus_count),  ", 하락:" + str(minus_count))


if __name__ == "__main__":
    main(sys.argv)
