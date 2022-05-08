'''
Created on 14. nov. 2017

@author: michal
link: https://github.com/mfolusiak/kMeansSupportResistance
@see 지지선, 저항선 그리는 알고리즘
'''
import time, datetime, sys, getopt
import matplotlib.patches as mpatches
import pyupbit
import pandas as pd
from common.utils import market_code, get_interval, upbit_get_usd_krw

# 한글 폰트 사용을 위해서 세팅
from matplotlib import font_manager, rc
font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

def save_ticker(v, cnt=60, interval='day'):
    to_time = datetime.datetime.now()
    # kimchi_premium = 1.05
    kimchi_premium = 1.0
    usd = upbit_get_usd_krw() * kimchi_premium

    if v.capitalize().startswith('KRW-'):
        df = pyupbit.get_ohlcv(v, interval=interval, count=cnt, to=to_time, period=1)
    else:
        df = pyupbit.get_ohlcv('KRW-' + v, interval=interval, count=cnt, to=to_time, period=1)

    tickers = df.values.tolist()

    f = open('data/' + v + '.mst', 'w')
    print('<TICKER>,<DTYYYYMMDD>,<OPEN>,<HIGH>,<LOW>,<CLOSE>,<VOL>', file=f)

    i = 0

    for t in tickers:
        if v.upper().endswith('BTC') :
            print(f'{v},{i},{t[0]/1200},{t[1]/1200},{t[2]/1200},{t[3]/1200},{t[4]}', file=f)
        else:
            print(f'{v},{i},{t[0]},{t[1]},{t[2]},{t[3]},{t[4]}', file=f)

        i += 1

    f.close()

    return to_time

def load_quotes(t):
    try:
        q = pd.read_csv("data/" + t + ".mst", sep=',', header=0,
                        names=['Ticker', 'Date', 'o', 'h', 'l', 'c', 'v']) #Load the dataframe with headers
        # q.index = pd.to_datetime(q['Date'], format='%Y%m%d')
        # q.index = q['Date']
        q['ch'] = q['c'] / q['c'].shift(1) - 1
        q.fillna(method='ffill', inplace=True)
        q.fillna(method="bfill", inplace=True)
        return q
    except OSError as e:
        print("Not found %s"%(t))

def plot_candlestick(tckr, v, last, interval) -> object:
    from mplfinance.original_flavor import candlestick_ohlc, candlestick2_ohlc
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    from common.utils import market_code

    fig, ax = plt.subplots()
    _, _, code_to_name = market_code()
    kor_name = code_to_name['KRW-' + v.upper()]

    plt.title(kor_name + ' 지지/저항선-' + interval + ' (' + str(last)[:16] + ') 까지')

    candlestick2_ohlc(ax, tckr['o'], tckr['h'], tckr['l'], tckr['c'],
                      colorup='red', colordown='blue', width=0.6)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(12))
    fig.autofmt_xdate()
    fig.tight_layout()
    return plt

def main(argv):
    import pandas as pd
    import numpy as np
    from sklearn import cluster

    # input
    ticker = 'LINK'
    cnt = 60
    interval = 'day'

    try:
        opts, etc_args = getopt.getopt(argv[1:], "ht:c:i:"
                                       , ["help", "ticker=", "count=", "interval"])

    except getopt.GetoptError:
        print(argv[0], '-c <days> -t <ticker symbol>')
        print('ex) python', f'{argv[0]}', '-c 365 -t xtz')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('ex) python', f'{argv[0]}', '-c 365 -t xtz')
            print('')
            sys.exit()

        elif opt in ("-t", "--ticker"):  # ticker symbol
            ticker = arg

        elif opt in ("-c", "--count"):  # count
            cnt = int(arg.strip())

        elif opt in ("-i", "--interval"):  # count
            interval = get_interval(arg.strip())

    last_date = save_ticker(ticker, cnt, interval)
    tckr = load_quotes(ticker)
    rlen = len(tckr)
    tckr = tckr.iloc[-rlen:]

    #
    # clustering just by number of days
    kmeans = cluster.KMeans(n_clusters=5).fit(tckr[['c']])

    mean_vol = tckr['v'].sum()/cnt
    vol_bin = mean_vol/10.
    
    # create new DataFrame
    # for each price at a date, create that many instances as many bins 
    tckr['n_bins'] = tckr['v']/vol_bin
    tckr['n_bins'] = tckr['n_bins'].astype(int)
    
    binned_close = np.array([])
    # for i in range(days):
    for i in range(rlen):
        # repeat closing price n_bins times
        binned_close = np.append(binned_close, values=np.repeat(tckr['c'].iloc[i], tckr['n_bins'].iloc[i]), axis=0 )

    #
    # clustering by volume
    kmeans_vol = cluster.KMeans(n_clusters=5).fit(binned_close.reshape(-1,1))

    #
    # plot
    my_plot = plot_candlestick(tckr, ticker, last_date, interval)
    # my_plot.title(ticker + '(Support Resistance) ' + str(last_date) )

    # ax = my_plot.gca()
    # ax.set_facecolor('black')

    # red cluster centers by days
    for cc in kmeans.cluster_centers_:
        horiz_line_data = np.array([cc for i in range(2)])
        lb = str(horiz_line_data[0])
        my_plot.plot([0, tckr.index.size-1], horiz_line_data, 'r--', label=lb)
        print(horiz_line_data[0])

    # blue cluster centers by volume
    # for cc in kmeans_vol.cluster_centers_:
    #     horiz_line_data = np.array([cc for i in range(2)])
    #     my_plot.plot([0, tckr.index.size-1], horiz_line_data, 'g--')

    price_patch = mpatches.Patch(color='r', label='지지/저항선')
    # volume_patch = mpatches.Patch(color='g', label='지지/저항선(volume)')
    count_patch = mpatches.Patch(color='black', label='count: ' + str(rlen))

    my_plot.legend(loc='upper left', handles=[price_patch, count_patch])
    # my_plot.legend(loc='upper left', handles=[price_patch, volume_patch, count_patch])
    my_plot.show()


if __name__ == "__main__":
    main(sys.argv)
