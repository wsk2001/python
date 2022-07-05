import sys, getopt
import pyupbit
import pandas as pd


def view(v, to_time):

    if v.upper().startswith('KRW-'):
        df = pyupbit.get_ohlcv(v, interval='minute1', count=1440, to=to_time, period=1)
    else:
        df = pyupbit.get_ohlcv('KRW-' + v, interval='minute1', count=1440, to=to_time, period=1)

    print(df)
    print(to_time)


def usage(app):
    print(app, '-t <ticker symbol> -d <last date>')
    print('ex) python', app, '-t iost -d 20220706')
    sys.exit(2)


def main(argv):
    ticker = 'btc'
    last_time = " 08:50:00"
    last_date = ''

    try:
        opts, etc_args = getopt.getopt(argv[1:], "ht:d:"
                                       , ["help", "ticker=", "date="])
    except getopt.GetoptError:
        usage(argv[0])

    for opt, arg in opts:

        print(opt, arg)

        if opt in ("-h", "--help"):
            print('222')
            usage(argv[0])

        elif opt in ("-t", "--ticker"):
            ticker = arg

        elif opt in ("-d", "--date"):
            print('get date')
            last_date = arg.strip()

    if 0 < len(last_date):
        last_date = last_date + last_time
    else:
        print('111')
        usage(argv[0])

    pd.set_option('display.max_rows', 16000)
    view(ticker, last_date)


if __name__ == "__main__":
    main(sys.argv)

# py .\oneday_flow.py -t iost -l "20211206"

