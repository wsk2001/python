import calendar
import getopt
import sys, time
import pyupbit
from common.utils import market_code, get_interval
from datetime import datetime


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


def analyze(ticker, cnt, interval='day'):
    if not ticker.startswith('KRW-'):
        ticker = 'KRW-' + ticker

    df = pyupbit.get_ohlcv(ticker, interval=interval, count=cnt, period=1)
    vals = df.values.tolist()
    idxs = df.index.tolist()

    st_o = 0.0
    en_c = 0.0
    print('symbol:', ticker[4:])
    print('date , open, high, low, close, volume, high %, low %, close %')

    for indexs, values in zip(idxs, vals):
        if st_o == 0:
            st_o = values[open_p]
        en_c = values[close_p]
        rc = get_earning(values[open_p], values[close_p])
        rh = get_earning(values[open_p], values[high_p])
        rl = get_earning(values[open_p], values[low_p])
        if interval.startswith('day'):

            chk_date = datetime.strptime(str(indexs)[:10], "%Y-%m-%d")

            week_day = (what_day_is_it(chk_date))
            print(str(indexs)[:10], week_day, ',', values[open_p], ',', values[high_p], ',',
                  values[low_p], ',',  values[close_p], ',', values[vol_p], ',', f'{rh:.3f}%', ',',
                  f'{rl:.3f}%', ',', f'{rc:.3f}%')
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
            print(indexs, ',', values[open_p], ',', values[high_p], ',', values[low_p], ',',
                  values[close_p], ',',  values[vol_p], ',', f'{rh:.3f}%', ',', f'{rl:.3f}%', ',', f'{rc:.3f}%')

    earn = ((en_c / st_o) - 1) * 100.0

    print('')

    if interval.startswith('day'):
        print(f'earning(count = {cnt} days): {earn:.3f}%')
        print(f'start :  {start_date} , Open, High, Low, Close')
        print('top   : ', hv.day, ',', hv.o, ',', hv.h, ',', hv.l, ',', hv.c)
        print('bottom: ', lv.day, ',', lv.o, ',', lv.h, ',', lv.l, ',', lv.c)
    else:
        print(f'earning: {earn:.3f}%')


def main(argv):
    ticker = None
    cnt = 14
    all_flag = None
    interval = 'day'

    try:
        opts, etc_args = getopt.getopt(argv[1:], "hc:t:i:a"
                                       , ["help", "count=", "ticker=", "interval", "all"])

    except getopt.GetoptError:
        print(argv[0], '-c <count> -t <ticker symbol> -i <interval> -a')
        print('ex) python', f'{argv[0]}', '-c 7 -t bat')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(argv[0], '-c <count> -t <ticker symbol> -i <interval>')
            print('ex) python', f'{argv[0]}', '-c 7 -t bat -i d')
            print('ex) python', f'{argv[0]}', '-c 7 -t bat -i m15')
            sys.exit()

        elif opt in ("-t", "--ticker"):  # ticker symbol
            ticker = arg

        elif opt in ("-c", "--count"):  # count
            cnt = int(arg.strip())

        elif opt in ("-i", "--interval"):  # interval
            iv = arg.strip()
            interval = get_interval(iv)

        elif opt in ("-a", "--all"):  # count
            all_flag = True

    if all_flag is None:
        analyze(ticker, cnt, interval)
    else:
        code_list, _, _ = market_code()
        for t in code_list:
            analyze(t, cnt, interval)
            print('')
            time.sleep(0.3)


if __name__ == "__main__":
    main(sys.argv)

# run: python get_ohlcv.py -c 7 -t kava -i d
# 일단위 data 수집시, 최고가 일자 _data, 최저가 일자 _data print 하도록 수정 필요.

