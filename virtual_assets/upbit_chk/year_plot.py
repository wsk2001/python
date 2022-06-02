# importing package
import matplotlib.pyplot as plt
import numpy as np
import time, sys, getopt
import pyupbit
import datetime

open_p = 0
high_p = 1
low_p = 2
close_p = 3

# create data
# x = np.arange(5)
# y1_earn = [5, -3, -7, 7, 19]
# y2_earn = [-2, -3, 6, 15, 23]
# y3_earn = np.full(5, 0)

# plot lines
# plt.plot(x, y1_earn, label="2020")
# plt.plot(x, y2_earn, label="2021")
# plt.plot(x, y3_earn, label="2022")
# plt.legend()
# plt.show()


def make_data(t, year, period):
    earnings = np.full(365, 0)
    if period == 365:
        to = datetime.datetime.strptime(year + "-12-31", "%Y-%m-%d")
        df = pyupbit.get_ohlcv(t, to=to, count=period)
    else:
        df = pyupbit.get_ohlcv(t, count=period)

    values = df.values.tolist()
    start_price = 0.0

    for i in range(len(values)):
        if i == 0:
            start_price = values[i][open_p]
        earnings[i] = ((values[i][close_p] / start_price) - 1) * 100.0

    return year, earnings


def main(argv):
    ticker = 'KRW-BTC'

    try:
        opts, etc_args = getopt.getopt(argv[1:], "ht:"
                                       , ["help", "ticker="])

    except getopt.GetoptError:
        print(argv[0], '-t <ticker symbol>')
        print('ex) python', f'{argv[0]}', '-t ada')
        print('ex) python', f'{argv[0]}', '-t btc')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(argv[0], '-t <ticker symbol>')
            print('ex) python', f'{argv[0]}', '-t ada')
            print('ex) python', f'{argv[0]}', '-t btc')
            sys.exit()

        elif opt in ("-t", "--ticker"):  # ticker symbol
            if arg.upper().startswith("KRW-"):
                ticker = arg
            else:
                ticker = 'KRW-' + arg.upper()

    day_of_year = datetime.datetime.now().timetuple().tm_yday
    y2, data2 = make_data(ticker, '2020', 365)
    y1, data1 = make_data(ticker, '2021', 365)
    y0, data0 = make_data(ticker, '2022', day_of_year)
    x = np.arange(365)

    plt.title('UPBIT ' + ticker)
    plt.plot(x, data2, label=y2)
    plt.plot(x, data1, label=y1)
    plt.plot(x, data0, label=y0)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main(sys.argv)
