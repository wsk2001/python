import time
import datetime
import sys, getopt
import pyupbit
from time import sleep

open_posi = 0
close_posi = 3


def get_minutes(start_dt, end_dt, fm='%Y-%m-%d %H:%M:%S'):
    time_1 = datetime.datetime.strptime(start_dt, fm)
    time_2 = datetime.datetime.strptime(end_dt, fm)
    minutes = int((time_2 - time_1).seconds / 60)
    return minutes


def plus_minus(t, to, cnt):
    if not t.upper().startswith('KRW-'):
        t = 'KRW-' + t

    df = pyupbit.get_ohlcv(t, interval='minute10', to=to, count=int(cnt+1), period=1)
    values = df.values.tolist()
    indexs = df.index.tolist()
    start_v = 0.0

    lst = []
    times = []
    lst.clear()
    times.clear()

    for i in range(len(values)):
        if i == 0:
            start_v =  values[i][open_posi]
            i = 1

        if values[i][close_posi] < start_v:
            lst.append(-1)
        elif start_v < values[i][close_posi]:
            lst.append(1)
        else:
            lst.append(0)

        times.append(str(indexs[i])[11:16])

    return times, lst


def get_ticker_list():
    return pyupbit.get_tickers(fiat="KRW")

def check_time_BT09():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if '09:00:00' < now[12:18]:
        return False
    else:
        return True


def main(argv):
    all = []
    all.clear()

    lst = get_ticker_list()
    if check_time_BT09():
        to = datetime.datetime.now() - datetime.datetime.timedelta(1)
    else:
        to = datetime.datetime.now()

    start_dt = to.strftime('%Y-%m-%d') + ' 09:00:01'
    end_dt = to.strftime('%Y-%m-%d %H:%M:%S')
    cnt = get_minutes(start_dt, end_dt) / 10

    print('upbit ', end_dt, ' 기준 종목 수:', len(lst))
    print('시각, 상승, 하락')

    for v in lst:
        sleep(0.2)
        times, fl = plus_minus(v, to, cnt)
        all.append(fl)

    for i in range(len(times)):
        plus_count = 0
        minus_count = 0

        for j in range(len(all)):
            if 0 < all[j][i]:
                plus_count += 1
            elif all[j][i] < 0:
                minus_count += 1

        if i == 0:
            continue

        print(str(times[i])+' 분,', str(plus_count)+',', minus_count)


if __name__ == "__main__":
    main(sys.argv)
