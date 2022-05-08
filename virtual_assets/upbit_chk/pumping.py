import sys, getopt
import pyupbit
from time import sleep

open_posi = 0
high_posi = 1
close_posi = 3
check_day = 30
pump_cnt = 10
rate = 10.0

def rcmd(v):
    cnt = 0
    df = pyupbit.get_ohlcv(v, count=check_day)
    lst = df.values.tolist()

    for t in lst:
        cv = t[close_posi] - t[open_posi]
        rv = (cv / t[open_posi]) * 100.0

        if rate < rv:
            cnt = cnt + 1

    if pump_cnt <= cnt:
        print(f'ticker = {v[4:]}: count = {cnt}')


def get_ticker_list():
    return pyupbit.get_tickers(fiat="KRW")

def main(argv):
    global check_day, pump_cnt, rate
    try:
        opts, etc_args = getopt.getopt(argv[1:], "hd:c:r:", ["days=", "count=", "rate"])

    except getopt.GetoptError:
        print(argv[0], '-d <days> -r <rate> -c <count>')
        print('ex:', argv[0], '-d <days> -r <rate> -c <count>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(argv[0], '-d <days> -r <rate> -c <count>')
            sys.exit()

        elif opt in ("-d", "--days"):  # befor day count
            check_day = int(arg.strip())

        elif opt in ("-r", "--rate"):  # befor day count
            rate = float(arg.strip())

        elif opt in ("-c", "--count"):  # befor day count
            pump_cnt = int(arg.strip())

    lst = get_ticker_list()
    for v in lst:
        sleep(0.3)
        rcmd(v)


if __name__ == "__main__":
    main(sys.argv)

# python pumping.py -d 30 -r 10 -c 8
