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


##############################################################################
# 스토캐스틱 (Stochastic)지표로 매매하는 법
# 주로 횡보장이나 박스권에서 많이 씁니다.
# 5-3-3, 10-6-6, 20-12-12 숫자가 적어질수록 단기적인 움직임을 보기 용이하며
# 긴 흐름을 가져 가실 때는 20 12 12 로 보시면 됩니다.
##############################################################################
# 매수 신호 = %K선이 과매도 영역 에서 아래 에서 %D선을 교차 합니다.
# 매도 신호 = %K선이 과매수 영역 에서 위에서 %D선을 교차 합니다.
##############################################################################
def AddStochastic(priceData, period=9, screen_window=3, slow_window=3):
    ndayhigh = priceData['high'].rolling(window=period, min_periods=1).max()
    ndaylow = priceData['low'].rolling(window=period, min_periods=1).min()
    fast_k = (priceData['close'] - ndaylow) / (ndayhigh - ndaylow) * 100
    fast_d = fast_k.rolling(window=screen_window).mean()
    slow_k = fast_k.rolling(window=slow_window).mean()
    slow_d = fast_d.rolling(window=slow_window).mean()
    return priceData.assign(slow_k=slow_k, slow_d=slow_d).dropna().copy()


def stocastic_list(ticker, cnt, interval='day'):
    if not ticker.startswith('KRW-') and not ticker.startswith('BTC-') and not ticker.startswith('USDT-'):
        ticker = 'KRW-' + ticker

    df = pyupbit.get_ohlcv(ticker, count=cnt, period=1)
    df = AddStochastic(df, 9, 3, 3)

    vals = df.values.tolist()
    idxs = df.index.tolist()

    last = len(idxs) - 1

    print('stochastic, symbol:', ticker[4:])
    print('일자 , 종가, SLOW K%, SLOW D%')

    for indexs, v in zip(idxs, vals):
        print(str(indexs)[:10], f'{v[3]:.2f}, {v[6]:.2f}, {v[7]:.2f}')

    print()
    print(str(idxs[last])[:10], f'{vals[last][3]:.2f}, {vals[last][6]:.2f}, {vals[last][7]:.2f}')


def stocastic(ticker, cnt, interval='day'):
    if not ticker.startswith('KRW-') and not ticker.startswith('BTC-') and not ticker.startswith('USDT-'):
        ticker = 'KRW-' + ticker

    df = pyupbit.get_ohlcv(ticker, interval=interval, count=cnt, period=1)

    dft = df
    df10 = AddStochastic(dft, 9, 3, 3)
    vals = df10.values.tolist()
    idxs = df10.index.tolist()
    last = len(idxs) - 1
    k = vals[last][6]
    d = vals[last][7]

    return ticker[4:], k, d


def main(argv):
    ticker = None
    cnt = 60
    all_flag = None

    recommend_buy = []
    recommend_sell = []

    recommend_buy.clear()
    recommend_sell.clear()

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

    if ticker is None:
        all_flag = True

    if all_flag is None:
        v, k, d = stocastic(ticker, cnt)
        print(f'{v}, {k5:.2f}, {d5:.2f}, {k10:.2f}, {d10:.2f}')
    else:
        code_list, _, _ = market_code()
        print('Stochastic Oscillator')
        print('symbol, %K, %D')
        code_list.sort()
        for t in code_list:
            v, k, d = stocastic(t, cnt)

            # buy signal
            if d < 25 and d < k:
                recommend_buy.append(v)
                print(f'{v}, {k:.2f}, {d:.2f}, buy')

            # sell signal
            if 75 < d and k < d:
                recommend_sell.append(v)
                print(f'{v}, {k:.2f}, {d:.2f}, sell')

            time.sleep(0.3)

        print()

        if 0 < len(recommend_buy):
            print(f'recommend buy ({str(len(recommend_buy))}): ', end=' ')
            ts = ''
            for ticker in recommend_buy:
                if 0 < len(ts):
                    ts += ',' + ticker
                else:
                    ts += ticker
            print(ts)

        if 0 < len(recommend_sell):
            print(f'recommend sell ({str(len(recommend_sell))}): ', end=' ')
            ts = ''
            for ticker in recommend_sell:
                if 0 < len(ts):
                    ts += ',' + ticker
                else:
                    ts += ticker
            print(ts)


if __name__ == "__main__":
    main(sys.argv)

# run: python get_ohlcv.py -c 7 -t kava -i d
# 일단위 data 수집시, 최고가 일자 _data, 최저가 일자 _data print 하도록 수정 필요.
# BTC market 가격 반영
