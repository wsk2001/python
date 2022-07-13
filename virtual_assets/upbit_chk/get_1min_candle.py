import sys, getopt
import pyupbit
import pandas as pd
from datetime import datetime, timedelta
import pytz


open_p = 0
close_p = 3
dt_fmt = "%Y-%m-%d %H:%M:%S"


def local_time_to_utc(str_time):
    local = pytz.timezone("Asia/Seoul")
    naive = datetime.strptime(str_time, dt_fmt)
    local_dt = local.localize(naive, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)

    return utc_dt.strftime(dt_fmt)


def get_minutes(start_dt, end_dt, fm=dt_fmt):
    time_1 = datetime.strptime(start_dt, fm)
    time_2 = datetime.strptime(end_dt, fm)
    minutes = int((time_2 - time_1).seconds / 60)
    return minutes


def view(v, to_time):
    end_time = datetime.strptime(local_time_to_utc(to_time), dt_fmt)
    end_time = end_time + timedelta(1)
    oneday_minutes = 1440

    if datetime.now() < end_time:
        end_time = datetime.now()
        str_etime = datetime.strftime(end_time, dt_fmt)
        str_stime = str_etime[:11] + '09:00:01'
        oneday_minutes = get_minutes(str_stime, str_etime)

    if v.upper().startswith('KRW-'):
        df = pyupbit.get_ohlcv(v, interval='minute1', count=oneday_minutes, to=end_time, period=1)
    else:
        df = pyupbit.get_ohlcv('KRW-' + v, interval='minute1', count=oneday_minutes, to=end_time, period=1)

    values = df.values.tolist()
    indexes = df.index.tolist()

    for i in range(len(values)):
        close_price = values[i][close_p]
        chk_time = datetime.strptime(str(indexes[i]), dt_fmt)
        print(i, close_price)
        # print(chk_time, close_price)


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

# 사용법: py get_1min_candle.py -s btc -d "2022-07-06" > ..\2020-07-06
# 하루가 1440 분 이지만 거래가 없으면 해당 시간의 data 는 없고, 따라서 이전 data 를 가져 온다.
# 일자별 1분 단위 종가를 가져 온다.
# 목적: 정해진 기간 중 일별, 시간대별, 등락 유형을 보기 위한 data 추출.
#
# gnuplot 를 이용하여 ploting 함. (wgnuplot 실행 후)
# gnuplot> plot '2022-07-06' with l, '2022-07-07' with l, '2022-07-08' with l, '2022-07-09' with l, '2022-07-10' with l, '2022-07-11' with l, '2022-07-12' with l

