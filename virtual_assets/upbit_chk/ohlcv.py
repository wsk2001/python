import calendar
import getopt
import sys, time
import pyupbit
from common.utils import market_code
from datetime import datetime
import argparse

class ohlc:
    def __init__(self):
        self.day = ''
        self.o = 0.0
        self.h = 0.0
        self.l = 0.0
        self.c = 0.0


start_date = ''
hv = ohlc()
lv = ohlc()

open_p = 0
high_p = 1
low_p = 2
close_p = 3
vol_p = 4


def get_earning(start, end):
    return ((end / start) - 1) * 100.0


def what_day_is_it(date):
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    day = date.weekday()
    return days[day]


def krw_btc_price():
    df = pyupbit.get_ohlcv('KRW-BTC', count=1)
    return df['close'][0]


def analyze(ticker, cnt, interval='day', to=None):
    if not ticker.startswith('KRW-') and not ticker.startswith('BTC-') and not ticker.startswith('USDT-'):
        ticker = 'KRW-' + ticker

    df = pyupbit.get_ohlcv(ticker, interval=interval, count=cnt, to=to, period=1)
    vals = df.values.tolist()
    idxs = df.index.tolist()

    st_o = 0.0
    en_c = 0.0
    print('symbol:', ticker[4:])
    if interval.startswith('month'):
        print('month , open, close, earning%')
    else:
        print('date, wd, open, high, low, close, volume, high%, low%, close%')

    for indexs, values in zip(idxs, vals):
        if st_o == 0:
            st_o = values[open_p]
        en_c = values[close_p]
        rc = get_earning(values[open_p], values[close_p])
        rh = get_earning(values[open_p], values[high_p])
        rl = get_earning(values[open_p], values[low_p])
        # vr = rh - rl
        if interval.startswith('day'):

            chk_date = datetime.strptime(str(indexs)[:10], "%Y-%m-%d")

            week_day = (what_day_is_it(chk_date))
            print(str(indexs)[:10], ',', week_day, ',', f'{values[open_p]:.3f}, {values[high_p]:.3f},',
                  f'{values[low_p]:.3f}, {values[close_p]:.3f}, {values[vol_p]:.3f}, {rh:.3f}%', ',',
                  f'{rl:.3f}%, {rc:.3f}%')
            if hv.o == 0.0:
                start_date = str(indexs)[:10]
                hv.day = str(indexs)[:10]
                hv.o = values[open_p]
                hv.h = values[high_p]
                hv.l = values[low_p]
                hv.c = values[close_p]

            if lv.o == 0.0 or values[close_p] < lv.c:
                lv.day = str(indexs)[:10]
                lv.o = values[open_p]
                lv.h = values[high_p]
                lv.l = values[low_p]
                lv.c = values[close_p]

            if hv.c < values[close_p]:
                hv.day = str(indexs)[:10]
                hv.o = values[open_p]
                hv.h = values[high_p]
                hv.l = values[low_p]
                hv.c = values[close_p]

        else:
            if interval.startswith('month'):
                print(f'{str(indexs)[:7]}, {values[open_p]:.2f}, {values[close_p]:.2f}, {rc:.2f}')
            else:
                print(f'{indexs}, {values[open_p]:.3f}, {values[high_p]:.3f},',
                      f'{values[low_p]:.3f}, {values[close_p]:.3f}, {values[vol_p]:.3f}, {rh:.3f}%', ',',
                      f'{rl:.3f}%, {rc:.3f}%')

    earn = ((en_c / st_o) - 1) * 100.0

    print('')

    if interval.startswith('day'):
        print(f'earning(count = {cnt} days): {earn:.3f}%')
        print(f'start   :  {start_date} , Open, High, Low, Close')
        print('highest : ', hv.day, ',', f'{hv.o:.3f} , {hv.h:.3f}, {hv.l:.3f}, {hv.c:.3f}')
        print('lowest  : ', lv.day, ',', f'{lv.o:.3f} , {lv.h:.3f}, {lv.l:.3f}, {lv.c:.3f}')
    else:
        print(f'earning: {earn:.3f}%')

arr_interval = ['day', 'week', 'month', 'minute1', 'minute3', 'minute5',
                'minute10', 'minute15', 'minute30', 'minute60', 'minute240']

def main(argv):
    parser = argparse.ArgumentParser(description='옵션 지정 방법')
    parser.add_argument('-c', '--count', required=False, default=28, help='수집 data 갯수 (default=10000)')
    parser.add_argument('-s', '--symbol', required=False, default='btc', help='심볼 (BTC, ETH, ADA, ..., default=all)')
    parser.add_argument('-d', '--enddate', required=False, default=None, help='종료 일자(yyyy-mm-dd, default=현재 일자)')
    parser.add_argument('-t', '--endtime', required=False, default=None, help='종료 시각(hh:mm:ss, default=현재 시각)')
    parser.add_argument('-i', '--interval', required=False, default='day',
                        help='candle 종류 (day, week, month, minute1, ...)')

    args = parser.parse_args()
    count = int(args.count)
    symbol = args.symbol
    interval = args.interval
    enddate = args.enddate
    endtime = args.endtime
    to = None

    if arr_interval.count(interval) <= 0:
        parser.print_help()
        exit(0)

    if enddate is not None and endtime is None:
        to = enddate + ' ' + '09:00:00'

    if enddate is not None and endtime is not None:
        to = enddate + ' ' + endtime

    analyze(symbol, count, interval, to)


if __name__ == "__main__":
    main(sys.argv)

# run: python get_ohlcv.py -c 7 -t kava -i d
# 일단위 data 수집시, 최고가 일자 _data, 최저가 일자 _data print 하도록 수정 필요.
# BTC market 가격 반영

