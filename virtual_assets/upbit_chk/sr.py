'''
Created on 14. nov. 2017

@author: michal
link: https://github.com/mfolusiak/kMeansSupportResistance
@see 지지선, 저항선 그리는 알고리즘
'''
import os, datetime, sys, getopt
import matplotlib.patches as mpatches
import pyupbit
import pandas as pd
from common.utils import market_code, get_interval, upbit_get_usd_krw
import argparse

# 한글 폰트 사용을 위해서 세팅
from matplotlib import font_manager, rc
font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

def save_ticker(v, cnt=60, interval='day'):
    to_time = datetime.datetime.now()

    if v.upper().startswith('KRW-'):
        df = pyupbit.get_ohlcv(v, interval=interval, count=cnt, to=to_time, period=1)
    else:
        df = pyupbit.get_ohlcv('KRW-' + v, interval=interval, count=cnt, to=to_time, period=1)

    tickers = df.values.tolist()
    indexs = df.index.tolist()

    f = open('data/' + v + '.mst', 'w')
    print('<TICKER>,<DTYYYYMMDD>,<OPEN>,<HIGH>,<LOW>,<CLOSE>,<VOL>', file=f)

    i = 0

    for t in tickers:
        print(f'{v},{str(indexs[i])[:10]},{t[0]},{t[1]},{t[2]},{t[3]},{t[4]}', file=f)
        i += 1

    f.close()

    return to_time

def load_quotes(t):
    try:
        q = pd.read_csv("data/" + t + ".mst", sep=',', header=0,
                        names=['Ticker', 'Date', 'o', 'h', 'l', 'c', 'v'])
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

    parser = argparse.ArgumentParser(description='옵션 지정 방법')
    parser.add_argument('--symbol', required=False, default='BTC', help='심볼 (default:BTC)')
    parser.add_argument('--interval', required=False, default='day', help='interval(day,minute60, ..., default=day)')
    parser.add_argument('--count', required=False, default=365, help='count of candle')
    parser.add_argument('--view', required=False, default="yes", help='view plot (yes/no)')

    args = parser.parse_args()
    symbol = args.symbol
    interval = args.interval
    count = int(args.count)
    view = args.view

    last_date = save_ticker(symbol, count, interval)
    tckr = load_quotes(symbol)
    rlen = len(tckr)
    tckr = tckr.iloc[-rlen:]

    kmeans = cluster.KMeans(n_clusters=5).fit(tckr[['c']])

    mean_vol = tckr['v'].sum()/count
    vol_bin = mean_vol/10.
    
    tckr['n_bins'] = tckr['v']/vol_bin
    tckr['n_bins'] = tckr['n_bins'].astype(int)
    
    binned_close = np.array([])
    for i in range(rlen):
        binned_close = np.append(binned_close, values=np.repeat(tckr['c'].iloc[i], tckr['n_bins'].iloc[i]), axis=0 )

    kmeans_vol = cluster.KMeans(n_clusters=5).fit(binned_close.reshape(-1,1))

    # plot
    my_plot = plot_candlestick(tckr, symbol, last_date, interval)

    # red cluster centers by days
    sr_val_list = []
    sr_val_list.clear()
    for cc in kmeans.cluster_centers_:
        horiz_line_data = np.array([cc for i in range(2)])
        lb = str(horiz_line_data[0])
        my_plot.plot([0, tckr.index.size-1], horiz_line_data, 'r--', label=lb)
        # print(horiz_line_data[0])
        sr_val_list.append(horiz_line_data[0])

    sr_val_list = sorted(sr_val_list)
    sr_val_list = reversed(sr_val_list)
    if interval.lower().startswith('minute'):
        minute = interval.replace('minute', '')
        print(f'{symbol.upper()} 지지/저항선, {minute}분봉:{rlen} 기준')
    else:
        print(f'{symbol.upper()} 지지/저항선, 일봉:{rlen} 기준')

    print(f'분석 시점: {datetime.datetime.today()} ')
    print()
    for ele in sr_val_list:
        print(f'{ele[0]:.2f}')
    print()

    os.remove("data/" + symbol + ".mst")

    if view.upper().startswith('YES'):
        price_patch = mpatches.Patch(color='r', label='지지/저항선')
        count_patch = mpatches.Patch(color='black', label='count: ' + str(rlen))

        my_plot.legend(loc='upper left', handles=[price_patch, count_patch])
        my_plot.show()


if __name__ == "__main__":
    main(sys.argv)
