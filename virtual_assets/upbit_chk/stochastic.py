import sys, time
import pyupbit
from common.utils import market_code, get_interval
from datetime import datetime, date
import argparse
import sqlite3
import pandas as pd


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
def AddStochastic(priceData, period=5, screen_window=3, slow_window=3):
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


def buy(index, total_amt, close_amt):
    count = total_amt / close_amt

    # print(f'{index}, buy, {close_amt:.2f}, {count:.2f}, {total_amt:.2f}')
    return count


def sell(index, count, close_amt):
    end_amt = count * close_amt

    # print(f'{index}, sell, {close_amt:.2f}, {count:.2f}, {end_amt:.2f}')
    return end_amt


# 스토캐스트 %K 가 %D 를 돌파 할때
def stocastic_backtesting_kd_cross(ticker, cnt, interval='day'):
    start_cash = 10000000
    end_cash = 10000000
    buy_flag = False
    count = 0

    if not ticker.startswith('KRW-') and not ticker.startswith('BTC-') and not ticker.startswith('USDT-'):
        ticker = 'KRW-' + ticker

    df = pyupbit.get_ohlcv(ticker, interval=interval, count=cnt, period=1)

    dft = df
    df10 = AddStochastic(dft, 14, 3, 3)
    vals = df10.values.tolist()
    idxs = df10.index.tolist()

    # print('스토캐스틱 백테스트 심볼:', ticker[4:], ', 범위:',  str(idxs[0])[:10],'~', str(idxs[-1])[:10])
    # print('일자, 구분, 단가, 수량, 금액')

    i = 0
    lower_limit = 20
    upper_limit = 80
    lower_rate = -5.0
    upper_rate = 5.0
    for indexs, v in zip(idxs, vals):
        index = str(indexs)[:10]
        close_amt = v[3]
        k = v[6]
        d = v[7]
        i += 1

        if i < 9:
            continue

        if buy_flag is False:
            if d < k and d <= lower_limit:
                buy_flag = True
                count = buy(index, end_cash, close_amt)
        elif buy_flag is True:
            if k < d and upper_limit <= d:
                buy_flag = False
                end_cash = sell(index, count, close_amt)
            else:
                cur_cash = count * close_amt
                cur_rate = ((cur_cash / end_cash) - 1.0) * 100.0
                if cur_rate <= lower_rate or upper_rate < cur_rate:
                    buy_flag = False
                    end_cash = sell(index, count, close_amt)

    last_rate = ((end_cash / start_cash) - 1.0) * 100.0

    return ticker, start_cash, end_cash, last_rate


# 스토캐스트 %K 가 lower limit, upper limit 를 돌파 할때
def stocastic_backtesting_limit_cross(ticker, cnt, periodn=5, periodk=3, periodd=3, lower_limit=20, upper_limit=80,
                                      lower_rate=-5, upper_rate=5):
    start_cash = 10000000
    end_cash = 10000000
    buy_flag = False

    # if not ticker.startswith('KRW-') and not ticker.startswith('BTC-') and not ticker.startswith('USDT-'):
    #     ticker = 'KRW-' + ticker
    #
    # df = pyupbit.get_ohlcv(ticker, interval='day', count=cnt, period=1)

    query = "select date, open, high, low, close, volume from day_candle " \
            "where symbol = '" + ticker[4:] + "' " \
            "order by date;"
    #            "and date >= '2022-01-01' " \

    con = sqlite3.connect('./dbms/virtual_asset.db')
    df = pd.read_sql_query(query, con)

    dft = df
    df10 = AddStochastic(dft, periodn, periodk, periodd)
    vals = df10.values.tolist()
    idxs = df10.index.tolist()

    # print('스토캐스틱 백테스트 심볼:', ticker[4:], ', 범위:',  str(idxs[0])[:10],'~', str(idxs[-1])[:10])
    # print('일자, 구분, 단가, 수량, 금액')

    for i in range(len(vals)):
        if i < 9:
            continue

        # db 에 있는 data 는 date column 이 index 가 아니라서 위치가 하나 더 늘어 난다.
        old_k = vals[i - 1][7]
        new_k = vals[i][7]
        index = vals[i][0]
        close_amt = vals[i][4]

        if buy_flag is False:
            if old_k <= lower_limit < new_k:
                buy_flag = True
                count = buy(index, end_cash, close_amt)
        elif buy_flag is True:
            if old_k >= upper_limit > new_k:
                buy_flag = False
                end_cash = sell(index, count, close_amt)
            else:
                cur_cash = count * close_amt
                cur_rate = ((cur_cash / end_cash) - 1.0) * 100.0
                if cur_rate <= lower_rate or upper_rate < cur_rate:
                    buy_flag = False
                    end_cash = sell(index, count, close_amt)

    last_rate = ((end_cash / start_cash) - 1.0) * 100.0

    con.close()

    return ticker, start_cash, end_cash, last_rate


def backtest_main(symbol='ALL', count=0, period=5, periodk=3, periodd=3, lower=20, upper=80, earnlow=-5, earnhigh=5):
    if symbol.startswith('ALL'):
        code_list, _, _ = market_code()
        code_list.sort()
    else:
        code_list = [symbol]
    if count == 0:
        # Current date
        count = datetime.now().timetuple().tm_yday - 1
        # Specific date
        # day_of_year = date(2021, 1, 7).timetuple().tm_yday

    plus_count = 0
    minus_count = 0
    for v in code_list:
        # v, start_cash, end_cash, rate = stocastic_backtesting_kd_cross(v, day_of_year-1)
        v, start_cash, end_cash, rate = stocastic_backtesting_limit_cross(v, count, period, periodk, periodd, lower,
                                                                          upper, earnlow, earnhigh)

        if rate < 0:
            minus_count += 1
        elif 0 < rate:
            plus_count += 1

        # print(f'{v[4:]}, 시작: {start_cash:.2f}, 종료: {end_cash:.2f}, 실적: {rate:.2f}%')
        print(f'{v[4:]},{rate:.2f}')
        # time.sleep(0.2)

    print(plus_count, minus_count, f'{plus_count / (plus_count + minus_count) * 100:.2f}%')
    print(
        f'count={count}, n={period}, k={periodk}, d={periodd}, low={lower}, high={upper}, elow={earnlow}, ehigh={earnhigh}')


def main(argv):
    parser = argparse.ArgumentParser(description='옵션 지정 방법')
    parser.add_argument('--count', required=False, default=None, help='days (default=None, day_of_year)')
    parser.add_argument('--symbol', required=False, default='ALL', help='symbol (default=ALL)')
    parser.add_argument('--backtest', required=False, default='NO', help='BackTesting YES/NO (default=NO)')
    parser.add_argument('--period', required=False, default=20, help='period nday (default=5)')
    parser.add_argument('--periodk', required=False, default=20, help='period K (default=3)')
    parser.add_argument('--periodd', required=False, default=20, help='period D (default=3)')
    parser.add_argument('--lower', required=False, default=20, help='Lower limit percent (default=20)')
    parser.add_argument('--upper', required=False, default=80, help='Upper limit percent (default=80)')
    parser.add_argument('--earnlow', required=False, default=-5, help='earning low (default=-5)')
    parser.add_argument('--earnhigh', required=False, default=5, help='earning high (default=5)')

    args = parser.parse_args()
    count = args.count
    symbol = args.symbol
    backtest = args.backtest
    period = int(args.period)
    periodk = int(args.periodk)
    periodd = int(args.periodd)
    lower = int(args.lower)
    upper = int(args.upper)
    earnlow = int(args.earnlow)
    earnhigh = int(args.earnhigh)

    if count is None:
        count = datetime.now().timetuple().tm_yday

    if backtest.upper().startswith('YES'):
        backtest_main(symbol, count, period, periodk, periodd, lower, upper, earnlow, earnhigh)


if __name__ == "__main__":
    main(sys.argv)

# run: python get_ohlcv.py -c 7 -t kava -i d
# 일단위 data 수집시, 최고가 일자 _data, 최저가 일자 _data print 하도록 수정 필요.
# BTC market 가격 반영
