import time
import datetime
import sys, getopt
import pyupbit
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
import pandas as pd

def view(v, cnt, itv, to_time=None, disp='yes', save='no'):
    plt.cla()
    plt.clf()
    plt.close()

    if isinstance(to_time, str):
        to_time = pd.to_datetime(to_time).to_pydatetime()
    else:
        to_time = datetime.datetime.now()

    if v.capitalize().startswith('KRW-'):
        df = pyupbit.get_ohlcv(v, interval=itv, count=cnt, to=to_time, period=1)
        dfbtc = pyupbit.get_ohlcv('KRW-BTC', interval=itv, count=cnt, to=to_time, period=1)
    else:
        df = pyupbit.get_ohlcv('KRW-' + v, interval=itv, count=cnt, to=to_time, period=1)
        dfbtc = pyupbit.get_ohlcv('KRW-BTC', interval=itv, count=cnt, to=to_time, period=1)

    ###################################################
    fig = plt.figure(v + '_' + str(to_time)[0:10])
    ax1 = fig.add_subplot(312)
    c_series = df['close']
    ax1.plot(c_series)
    plt.title(v + ' close')

    ax2 = fig.add_subplot(313)
    v_series = df['volume']
    ax2.plot(v_series, color='green')
    plt.title(v + ' volume')

    ax3 = fig.add_subplot(311)
    v_series = dfbtc['close']
    ax3.plot(v_series, color='blue')
    plt.title('BTC (' + itv + ')')

    if save.lower().startswith('yes'):
        manager = plt.get_current_fig_manager()
        manager.full_screen_toggle()

        plt.title(v + ' (' + itv + ')' + ' volume')
        plt.savefig('J:/charts/' + v + '_' + str(to_time)[0:10] + '.png')

    if disp.lower().startswith('yes'):
        plt.show()

    ###################################################

    # c_series = df['close']
    # c_ax = plt.gca()
    # c_series.plot(kind='line', x='name', y='currency', ax=c_ax)
    # c_ax.legend()
    #
    # plt.title(v + ' (' + itv + ')')
    # plt.show()
    # plt.savefig('J:/kilchi/' + v + '.png')

    # v_series = df['volume']
    # v_ax = plt.gca()
    # v_series.plot.subplot(kind='line', x='name', y='volume', ax=c_ax, color='green')


    # o_series = df['open']
    # o_ax = plt.gca()
    # o_series.plot(kind='line', x='name', y='currency', ax=c_ax, color='black')

    # df['sma5c'] = df['close'].rolling(5).mean()
    # df['sma5h'] = df['high'].rolling(5).mean()
    # df['sma5l'] = df['low'].rolling(5).mean()
    #
    # # h_series = df['high']
    # h_series = df['sma5h']
    # h_ax = plt.gca()
    # # h_series.plot(kind='line', x='name', y='currency', ax=h_ax, color='green')
    # h_series.plot(kind='line', label='high', ax=h_ax, color='green')
    # h_ax.legend()
    #
    # l_series = df['sma5l']
    # l_ax = plt.gca()
    # l_series.plot(kind='line', label='low' , ax=l_ax, color='blue')
    # l_ax.legend()
    #
    # ma5_series = df['sma5c']
    # ma5_ax = plt.gca()
    # ma5_series.plot(kind='line', label='sma5', ax=ma5_ax, color='magenta')
    # ma5_ax.legend()

    # manager = plt.get_current_fig_manager()
    # manager.full_screen_toggle()

    # plt.title(v + ' (' + itv + ')')
    # plt.savefig('J:/kilchi/' + v + '.png')
    # plt.show()

def main(argv):
    ticker = None
    itv = 'minute5'
    count = 288
    lasttime = " 09:00:00"
    lastdate = datetime.datetime.now().strftime('%Y%m%d')
    pd.set_option('display.max_rows', 16000)
    try:
        opts, etc_args = getopt.getopt(argv[1:], "ht:c:i:l:"
                                       , ["help", "ticker=", "count=", "interval=", "lastdate="])

    except getopt.GetoptError:
        print(argv[0], '-t <ticker symbol>')
        print('ex) python', f'{argv[0]}', '-t iost -c 48 -i minute30 -l', f'{lastdate}')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(argv[0], '-t <ticker symbol> -c <count> -i <interval> -l <lasttime>')
            print('\t<interval>')
            print('\t\tday / minute1 / minute3 / minute5 / minute10 / minute15 /')
            print('\t\tminute30 / minute60 / minute240 / week / month')
            print('')
            print('\t<lastdate>')
            print('\t\t(ex: "20210928"')
            print('')
            print('ex) python', f'{argv[0]}', '-t iost -c 48 -i minute30 -l', f'{lastdate}')
            print('')
            sys.exit()

        elif opt in ("-t", "--ticker"):  # ticker symbol
            ticker = arg

        elif opt in ("-c", "--count"):  # count
            count = int(arg.strip())

        elif opt in ("-i", "--interval"):  # interval
            itv = arg.strip()

        elif opt in ("-l", "--lastdate"):  # lastdate
            lastdate = arg.strip()

    if lastdate is not None:
        lastdate = lastdate + lasttime

    ko_lst = ["ICX", "WAXP", "MED", "PLA", "BORA", "META", "UPP", "CRE", "MLK",
              "HUNT", "AERGO", "HUM", "RFR", "AQT", "FCT2", "MOC", "MBL", "AHT", "TON", "CBK"]

    # view(v, cnt, itv, to_time=None, no_disp=None, save=None)
    if ticker is None:
        for l in ko_lst:
            view(l, count, itv, lastdate)
    else:
        view(ticker, count, itv, lastdate)


if __name__ == "__main__":
    main(sys.argv)

# python view_one_day.py -t iost -c 1440
# python .\view_one_day.py -t iost -c 288 -i minute5 -l "20210929"

