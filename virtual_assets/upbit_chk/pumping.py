import time, sys, getopt
import pyupbit
from datetime import datetime

open_p = 0
high_p = 1
low_p = 2
close_p = 3


def check_rate(v, chk_date, r):
    if v.upper().startswith('KRW-BTC'):
        return
    df = pyupbit.get_ohlcv(v, count=1, to=chk_date, period=1)
    if df is None:
        return
    values = df.values.tolist()
    rc = ((values[0][high_p] / values[0][open_p]) - 1) * 100.0
    if r <= rc:
        print(v[4:] + ',', chk_date.strftime("%Y-%m-%d") + ',', str(values[0][open_p]) + ',',
              str(values[0][close_p]) + ',', f'{rc:.3f}%')


def pumping_hi_30(v):
    p_count = 0
    df = pyupbit.get_ohlcv(v, count=10000, period=1)
    values = df.values.tolist()
    indexs = df.index.tolist()
    for i in range(len(values)):
        rc = ((values[i][high_p] / values[i][open_p]) - 1) * 100.0
        if 30.0 <= rc:
            chk_date = indexs[i].strftime("%Y-%m-%d")
            print(v + ',',  chk_date + ',', str(values[i][open_p]) + ',', str(values[i][high_p]) + ',', f'{rc:.3f}%')
            p_count += 1


def pumping_close_20(v):
    p_count = 0
    df = pyupbit.get_ohlcv(v, count=10000, period=1)
    values = df.values.tolist()
    indexs = df.index.tolist()
    for i in range(len(values)):
        rc = ((values[i][close_p] / values[i][open_p]) - 1) * 100.0
        if 20.0 <= rc:
            chk_date = indexs[i].strftime("%Y-%m-%d")
            print(v[4:] + ',',  chk_date + ',', str(values[i][open_p]) + ',', str(values[i][close_p]) + ',', f'{rc:.3f}%')


# It takes a long time to work. correlation analysis.
# correlation_analysis('KRW-BTC', 3.0, 10.0)
def correlation_analysis(v, chk_rate, rp):
    df = pyupbit.get_ohlcv(v, count=10000, period=1)
    values = df.values.tolist()
    indexs = df.index.tolist()

    date_lst = []
    val_lst = []
    date_lst.clear()
    val_lst.clear()

    print('symbol, date, open, high, rate')
    for i in range(len(values)):
        rate = ((values[i][high_p] / values[i][open_p]) - 1) * 100.0

        if chk_rate <= rate:
            date_lst.append(indexs[i])
            val_lst.append(values[i])

    for i in range(len(date_lst)):
        lst = pyupbit.get_tickers(fiat="KRW")
        rc = ((val_lst[i][high_p] / val_lst[i][open_p]) - 1) * 100.0
        print('BTC' + ',', date_lst[i].strftime("%Y-%m-%d") + ',', str(val_lst[i][open_p]) + ',',
              str(val_lst[i][high_p]) + ',', f'{rc:.3f}%')

        for v in lst:
            check_rate(v, date_lst[i], rp)
            time.sleep(0.1)

        print('')


def pumping_analysis():
    lst = pyupbit.get_tickers(fiat="KRW")

    for v in lst:
        time.sleep(0.1)
        pumping_close_20(v)


def main(argv):
    pumping_analysis()
    # correlation_analysis('KRW-BTC', 3.0, 10.0)


if __name__ == "__main__":
    main(sys.argv)
