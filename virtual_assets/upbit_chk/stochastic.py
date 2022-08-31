import calendar
import getopt
import sys, time
import pyupbit
from common.utils import market_code, get_interval
from datetime import datetime


class ohlc:
    def __init__(self):
        self.day = ''
        self.o = 0.0
        self.h = 0.0
        self.l = 0.0
        self.c = 0.0


start_date = ''
hv = ohlc()
lv = ohlc()

open_p = 0
high_p = 1
low_p = 2
close_p = 3
vol_p = 4


def get_earning(start, end):
    return ((end / start) - 1) * 100.0


def what_day_is_it(date):
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    day = date.weekday()
    return days[day]


def krw_btc_price():
    df = pyupbit.get_ohlcv('KRW-BTC', count=1)
    return df['close'][0]


#def AddStochastic(priceData, period=15, screen_window=5, slow_window=3):
def AddStochastic(priceData, period=14, screen_window=3, slow_window=3):
    ndayhigh = priceData['high'].rolling(window=period, min_periods=1).max()
    ndaylow = priceData['low'].rolling(window=period, min_periods=1).min()
    fast_k = (priceData['close'] - ndaylow) / (ndayhigh - ndaylow) * 100
    fast_d = fast_k.rolling(window=screen_window).mean()
    slow_k = fast_k.rolling(window=slow_window).mean()
    slow_d = fast_d.rolling(window=slow_window).mean()
    return priceData.assign(slow_d=slow_d).dropna().copy()
    # return priceData.assign(slow_k=slow_k, slow_d=slow_d).dropna().copy()


def analyze(ticker, cnt, interval='day'):
    if not ticker.startswith('KRW-') and not ticker.startswith('BTC-') and not ticker.startswith('USDT-'):
        ticker = 'KRW-' + ticker

    if not ticker.startswith('KRW-'):
        r = krw_btc_price()
    else:
        r = 1

    df = pyupbit.get_ohlcv(ticker, count=cnt, period=1)
    #df = AddStochastic(df, 15, 5, 3)
    #df = AddStochastic(df, 5, 3, 3)
    df = AddStochastic(df, 10, 6, 6)
    #df = AddStochastic(df, 20, 12, 12)

    vals = df.values.tolist()
    idxs = df.index.tolist()

    st_o = 0.0
    en_c = 0.0
    print('stochastic, symbol:', ticker[4:])
    print('일자 , 종가, SLOW D%')

    for indexs, v in zip(idxs, vals):
        print(str(indexs)[:10], f'{v[3]:.2f}, {v[6]:.2f}')


def main(argv):
    ticker = None
    cnt = 100
    all_flag = None

    try:
        opts, etc_args = getopt.getopt(argv[1:], "hc:t:a"
                                       , ["help", "count=", "ticker=", "all"])

    except getopt.GetoptError:
        print(argv[0], '-c <count> -t <ticker symbol>')
        print('ex) python', f'{argv[0]}', '-c 100 -t bat')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(argv[0], '-c <count> -t <ticker symbol>')
            print('ex) python', f'{argv[0]}', '-c 100 -t bat')
            sys.exit()

        elif opt in ("-t", "--ticker"):  # ticker symbol
            ticker = arg

        elif opt in ("-c", "--count"):  # count
            cnt = int(arg.strip())

        elif opt in ("-a", "--all"):  # count
            all_flag = True

    if all_flag is None:
        analyze(ticker, cnt)
    else:
        code_list, _, _ = market_code()
        for t in code_list:
            analyze(t, cnt)
            print('')
            time.sleep(0.3)


if __name__ == "__main__":
    main(sys.argv)

# run: python get_ohlcv.py -c 7 -t kava -i d
# 일단위 data 수집시, 최고가 일자 _data, 최저가 일자 _data print 하도록 수정 필요.
# BTC market 가격 반영
