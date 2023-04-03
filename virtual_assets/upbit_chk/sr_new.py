# https://raw.githubusercontent.com/WestXu/support_resistance_line/master/tests/test_support_resistance_line.py
import getopt
import sys
import pandas as pd
import pyupbit
from common.utils import get_interval
from support_resistance_line import SupportResistanceLine


def draw_sr(t, interval='days', count=100):
    if t.capitalize().startswith('KRW-'):
        df = pd.DataFrame(pyupbit.get_ohlcv(t, interval=interval, count=count, period=1), columns=['close'])
    else:
        df = pd.DataFrame(pyupbit.get_ohlcv('KRW-' + t, interval=interval, count=count, period=1), columns=['close'])

    my_series = df.squeeze()

    SupportResistanceLine(my_series).plot_both(show=True)

def main(argv):
    # input
    ticker = 'LINK'
    cnt = 90
    interval = 'days'

    try:
        opts, etc_args = getopt.getopt(argv[1:], "ht:c:i:"
                                       , ["help", "ticker=", "count=", "interval"])

    except getopt.GetoptError:
        print(argv[0], '-c <days> -t <ticker symbol> -i <interval>')
        print('ex) python', f'{argv[0]}', '-c 365 -t link -i d')
        print('ex) python', f'{argv[0]}', '-c 365 -t link -i m1')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('ex) python', f'{argv[0]}', '-c 365 -t link -i d')
            print('ex) python', f'{argv[0]}', '-c 365 -t link -i m1')
            print('')
            sys.exit()

        elif opt in ("-t", "--ticker"):  # ticker symbol
            ticker = arg

        elif opt in ("-c", "--count"):  # count
            cnt = int(arg.strip())

        elif opt in ("-i", "--interval"):  # count
            interval = get_interval(arg.strip())

    draw_sr(ticker, interval, cnt)

if __name__ == "__main__":
    main(sys.argv)
