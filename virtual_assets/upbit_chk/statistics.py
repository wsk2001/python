import calendar
import datetime
import getopt
import locale
import sys
from time import sleep

import pyupbit

op = 0
cp = 3

# 일자별 통계
def analyze_day(v, count, lastdate):
    ld = [0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0,
          0, 0, 0]

    locale.setlocale(locale.LC_ALL, 'ko_KR')
    df = pyupbit.get_ohlcv(v, interval='day', count=count, to=lastdate, period=1)

    values = df.values.tolist()
    indexs = df.index.tolist()

    j = 0
    for i in indexs:
        d = i.day-1
        e = values[j][3] - values[j][0]
        if 0.0 < e:
            ld[d] = ld[d] + 1
        elif 0.0 > e:
            ld[d] = ld[d] - 1

        j += 1

    print(v[4:], ld)

# 요일별 통계
def analyze_weekday(v, count, lastdate):
    lwd = [0, 0, 0, 0, 0, 0, 0]

    locale.setlocale(locale.LC_ALL, 'ko_KR')
    df = pyupbit.get_ohlcv(v, interval='day', count=count, to=lastdate, period=1)

    # ohlcv
    values = df.values.tolist()

    # date
    indexs = df.index.tolist()

    j = 0
    for i in indexs:
        wd = i.weekday()
        e = values[j][3] - values[j][0]
        if 0.0 < e:
            lwd[wd] = lwd[wd] + 1
        elif 0.0 > e:
            lwd[wd] = lwd[wd] - 1

        j += 1

    print(v[4:]+',', lwd[0], ',', lwd[1], ',', lwd[2], ',', lwd[3], ',', lwd[4], ',', lwd[5], ',', lwd[6])


def get_ticker_list():
    return pyupbit.get_tickers(fiat="KRW")


def main(argv):
    lasttime = " 23:59:59"
    lastdate = datetime.datetime.now().strftime('%Y%m%d')

    worktype = 'days'
    try:
        opts, etc_args = getopt.getopt(argv[1:], "hc:dwl:"
                                       , ["help", "count=", "day", "week", "lastdate="])

    except getopt.GetoptError:
        print('usage:', argv[0], '-c <days> -d -w -l <last date(yyyymmdd)>')
        print('ex) python', f'{argv[0]}', '-c 365')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('usage:', argv[0], '-c <days> -d -w -l <last date(yyyymmdd)>')
            print('ex) python', f'{argv[0]}', '-c 365 -d')
            print('ex) python', f'{argv[0]}', f'-c 365 -w -l {lastdate}')
            print('')
            sys.exit()

        elif opt in ("-c", "--count"):  # count
            cnt = int(arg.strip())

        elif opt in ("-d", "--day"):  # count
            worktype = 'days'

        elif opt in ("-w", "--week"):  # count
            worktype = 'weeks'

        elif opt in ("-l", "--lastdate"):  # count
            lastdate = arg.strip()

    lst = get_ticker_list()

    for v in lst:
        sleep(0.1)
        if worktype == "weeks":
            analyze_weekday(v, cnt, lastdate + lasttime)
        else:
            analyze_day(v, cnt, lastdate + lasttime)

if __name__ == "__main__":
    main(sys.argv)
