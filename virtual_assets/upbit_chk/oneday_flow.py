import sys, getopt
import pyupbit
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import pytz


def local_time_to_utc(str_time):
    local = pytz.timezone("Asia/Seoul")
    naive = datetime.strptime(str_time, "%Y-%m-%d %H:%M:%S")
    local_dt = local.localize(naive, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)

    return utc_dt.strftime("%Y-%m-%d %H:%M:%S")


def view(v, to_time):
    end_time = local_time_to_utc(to_time)
    if v.upper().startswith('KRW-'):
        df = pyupbit.get_ohlcv(v, interval='minute1', count=1440, to=end_time, period=1)
    else:
        df = pyupbit.get_ohlcv('KRW-' + v, interval='minute1', count=1440, to=end_time, period=1)

    plt.rcParams['axes.facecolor'] = 'black'
    plt.rcParams['lines.linewidth'] = 1
    plt.rcParams['axes.grid'] = True
    dfs = df['close']
    plt.plot(dfs, 'g')
    plt.title(v + ' (' + to_time[:10] + ')')
    plt.show()

    # print(df)


def usage(app):
    print(app, '-s <symbol> -d <date> -t <time>')
    print('ex) python', app, '-s btc -d 2022-07-06 -t 09:00:01')
    print('ex) python', app, '-s eth -d 2022-07-06 -t 00:00:01')
    print('ex) python', app, '-s ada -d 20220706 -t 090001')
    sys.exit(2)



def main(argv):
    symbol = 'btc'
    last_time = " 09:00:01"
    last_date = ''

    try:
        opts, etc_args = getopt.getopt(argv[1:], "hs:d:t:"
                                       , ["help", "symbol=", "date=", "time="])
    except getopt.GetoptError:
        usage(argv[0])

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage(argv[0])

        elif opt in ("-s", "--symbol"):
            symbol = arg

        elif opt in ("-d", "--date"):
            last_date = arg.strip()
            if len(last_date) < 10:
                last_date = last_date[0:4] + '-' + last_date[4:6] + '-' + last_date[6:8]

        elif opt in ("-t", "--time"):
            last_time = arg.strip()
            if len(last_time) < 8:
                last_time = last_time[0:2] + ':' + last_time[2:4] + ':' + last_time[4:6]
            last_time = ' ' + last_time

    if 0 < len(last_date):
        last_date = last_date + last_time
    else:
        usage(argv[0])

    pd.set_option('display.max_rows', 16000)
    view(symbol, last_date)


if __name__ == "__main__":
    main(sys.argv)

# py .\oneday_flow.py -t iost -l "2021-12-06"
# 하루가 1440 분 이지만 거래가 없으면 해당 시간의 data 는 없고, 따라서 이전 data 를 가져 온다.
# 1분 단위의 종가 graph draw
