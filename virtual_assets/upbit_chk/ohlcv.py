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


def what_day_is_it(date):
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    day = date.weekday()
    return days[day]


def analyze(ticker, cnt, interval='day'):
    if not ticker.startswith('KRW-'):
        ticker = 'KRW-' + ticker
    df = pyupbit.get_ohlcv(ticker, interval=interval, count=cnt, period=1)
    # ohlcv
    values = df.values.tolist()

    # date
    indexs = df.index.tolist()

    st_o = 0.0
    en_c = 0.0
    print('ticker symbol:', ticker[4:])
    print('date , open, high, low, close, volume, high %, low %, close %')
    for i in range(len(values)):
        if st_o == 0:
            st_o = values[i][open_p]
        en_c = values[i][close_p]
        rc = ((values[i][close_p] / values[i][open_p]) - 1) * 100.0
        rh = ((values[i][high_p] / values[i][open_p]) - 1) * 100.0
        rl = ((values[i][low_p] / values[i][open_p]) - 1) * 100.0
        if interval.startswith('day'):
            chk_date = datetime.strptime(str(indexs[i])[:10], "%Y-%m-%d")
            week_day = (what_day_is_it(chk_date))
            print(str(i), str(indexs[i])[:10], week_day, ',', values[i][open_p], ',', values[i][high_p], ',',
                  values[i][low_p], ',',  values[i][close_p], ',', values[i][vol_p], ',', f'{rh:.3f}%', ',',
                  f'{rl:.3f}%', ',', f'{rc:.3f}%')
            if hv.o == 0.0:
                start_date = str(indexs[i])[:10]
                hv.day = str(indexs[i])[:10]
                hv.o = values[i][open_p]
                hv.h = values[i][high_p]
                hv.l = values[i][low_p]
                hv.c = values[i][close_p]

            if lv.o == 0.0 or values[i][close_p] < lv.c:
                lv.day = str(indexs[i])[:10]
                lv.o = values[i][open_p]
                lv.h = values[i][high_p]
                lv.l = values[i][low_p]
                lv.c = values[i][close_p]

            if hv.c < values[i][close_p]:
                hv.day = str(indexs[i])[:10]
                hv.o = values[i][open_p]
                hv.h = values[i][high_p]
                hv.l = values[i][low_p]
                hv.c = values[i][close_p]

            # if values[i][close_p] < lv.c:
            #     lv.day = str(indexs[i])[:10]
            #     lv.o = values[i][open_p]
            #     lv.h = values[i][high_p]
            #     lv.l = values[i][low_p]
            #     lv.c = values[i][close_p]

        else:
            print(indexs[i], ',', values[i][open_p], ',', values[i][high_p], ',', values[i][low_p], ',',
                  values[i][close_p], ',',  values[i][vol_p], ',', f'{rh:.3f}%', ',', f'{rl:.3f}%', ',', f'{rc:.3f}%')

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

