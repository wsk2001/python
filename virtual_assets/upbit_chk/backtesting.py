import sys, time
import pyupbit
import talib

from common.utils import market_code, get_interval
from datetime import datetime, date
import argparse
import sqlite3
import pandas as pd


# 2 가 최적임
min_plus = 2

def buy(index, total_amt, close_amt):
    count = total_amt / close_amt

    # print(f'{index}, buy, {close_amt:.2f}, {count:.2f}, {total_amt:.2f}')
    return count


def sell(index, count, close_amt):
    end_amt = count * close_amt

    # print(f'{index}, sell, {close_amt:.2f}, {count:.2f}, {end_amt:.2f}')
    return end_amt


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


# 스토캐스트 %K 가 %D 를 돌파 할때
def stocastic_backtesting_kd_cross_(ticker, cnt, interval='day'):
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



# 스토캐스트 %K 가 %D 를 돌파 할때
def stocastic_backtesting_kd_cross(ticker, cnt, periodn=5, periodk=3, periodd=3, lower_limit=20, upper_limit=80,
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

    # "and date >= '2022-01-01' " \
    # "and date <= '2022-09-07' " \

    con = sqlite3.connect('./dbms/virtual_asset.db')
    df = pd.read_sql_query(query, con)
    if len(df) < 1:
        con.close()
        return ticker, 1, 1, 0

    dft = df
    df10 = AddStochastic(dft, periodn, periodk, periodd)
    vals = df10.values.tolist()
    idxs = df10.index.tolist()

    # print('스토캐스틱 백테스트 심볼:', ticker[4:], ', 범위:',  str(idxs[0])[:10],'~', str(idxs[-1])[:10])
    # print('일자, 구분, 단가, 수량, 금액')

    # 0: date,  1: open,   2: high, 3: low
    # 4: close, 5: volume, 6: K,    7: D

    plus_count = 0
    for i in range(len(vals)):
        if i < 9:
            continue

        # db 에 있는 data 는 date column 이 index 가 아니라서 위치가 하나 더 늘어 난다.
        k = vals[i][6]
        d = vals[i][7]
        index = vals[i][0]
        close_amt = vals[i][4]

        # 양봉
        if vals[i][1] < vals[i][4]:
            plus_count += 1
        elif vals[i][4] < vals[i][1]:
            plus_count = 0

        if buy_flag is False:
            if d < k and d <= lower_limit and min_plus <= plus_count:
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

    con.close()

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

    # "and date >= '2022-01-01' " \
    # "and date <= '2021-09-07' " \

    con = sqlite3.connect('./dbms/virtual_asset.db')
    df = pd.read_sql_query(query, con)
    if len(df) < 1:
        con.close()
        return ticker, 1, 1, 0

    dft = df
    df10 = AddStochastic(dft, periodn, periodk, periodd)
    vals = df10.values.tolist()
    idxs = df10.index.tolist()

    # print('스토캐스틱 백테스트 심볼:', ticker[4:], ', 범위:',  str(idxs[0])[:10],'~', str(idxs[-1])[:10])
    # print('일자, 구분, 단가, 수량, 금액')

    # 0: date,  1: open,   2: high, 3: low
    # 4: close, 5: volume, 6: K,    7: D

    plus_count = 0
    for i in range(len(vals)):
        # db 에 있는 data 는 date column 이 index 가 아니라서 위치가 하나 더 늘어 난다.
        old_d = vals[i - 1][7]
        new_d = vals[i][7]
        index = vals[i][0]
        close_amt = vals[i][4]

        # 양봉
        if vals[i][1] < vals[i][4]:
            plus_count += 1
        elif vals[i][4] < vals[i][1]:
            plus_count = 0

        if buy_flag is False:
            if old_d <= lower_limit < new_d and min_plus <= plus_count:
                buy_flag = True
                count = buy(index, end_cash, close_amt)
        elif buy_flag is True:
            # if upper_limit <= new_d:
            #     buy_flag = False
            #     end_cash = sell(index, count, close_amt)

            if old_d >= upper_limit > new_d:
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


def backtest_stocastic(symbol='ALL', count=0, period=5, periodk=3, periodd=3, lower=20, upper=80, earnlow=-20, earnhigh=20):
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
        # v, start_cash, end_cash, rate = stocastic_backtesting_limit_cross(v, count, period, periodk, periodd, lower,
        #                                                                   upper, earnlow, earnhigh)
        v, start_cash, end_cash, rate = stocastic_backtesting_kd_cross(v, count, period, periodk, periodd, lower,
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


# 스토캐스트 %K 가 %D 를 돌파 할때
def stocastic_backtesting_kd_cross(ticker, cnt, periodn=5, periodk=3, periodd=3, lower_limit=20, upper_limit=80,
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

    # "and date >= '2022-01-01' " \
    # "and date <= '2022-09-07' " \
    con = sqlite3.connect('./dbms/virtual_asset.db')
    df = pd.read_sql_query(query, con)
    if len(df) < 1:
        con.close()
        return ticker, 1, 1, 0

    dft = df
    df10 = AddStochastic(dft, periodn, periodk, periodd)
    vals = df10.values.tolist()
    idxs = df10.index.tolist()

    # print('스토캐스틱 백테스트 심볼:', ticker[4:], ', 범위:',  str(idxs[0])[:10],'~', str(idxs[-1])[:10])
    # print('일자, 구분, 단가, 수량, 금액')

    # 0: date,  1: open,   2: high, 3: low
    # 4: close, 5: volume, 6: K,    7: D

    for i in range(len(vals)):
        if i < 9:
            continue

        # db 에 있는 data 는 date column 이 index 가 아니라서 위치가 하나 더 늘어 난다.
        k = vals[i][6]
        d = vals[i][7]
        index = vals[i][0]
        close_amt = vals[i][4]

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

    con.close()

    return ticker, start_cash, end_cash, last_rate
##############################################################################

##############################################################################
# 볼린져 밴드
##############################################################################
def AddBBANDS(priceData, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0):
    upperband, middleband, lowerband = talib.BBANDS(priceData['close'], timeperiod=20, nbdevup=2, nbdevdn=2)
    return priceData.assign(upperband=upperband, middleband=middleband, lowerband=lowerband).dropna().copy()


# 스토캐스트 %K 가 %D 를 돌파 할때
def bband_backtesting(ticker, start_date=None):
    start_cash = 10000000
    end_cash = 10000000
    buy_flag = False

    query = "select date, open, high, low, close, volume from day_candle " \
            "where symbol = '" + ticker[4:] + "' " \
            "order by date;"

    # "and date >= '2022-01-01' " \
    # "and date <= '2022-09-07' " \
    con = sqlite3.connect('./dbms/virtual_asset.db')
    df = pd.read_sql_query(query, con)
    if len(df) < 1:
        con.close()
        return ticker, 1, 1, 0

    dft = AddBBANDS(df)
    vals = dft.values.tolist()
    idxs = dft.index.tolist()
    lower_rate = -5.0
    upper_rate = 5.0

    # 0: date,  1: open,   2: high,      3: low
    # 4: close, 5: volume, 6: upperband, 7: middleband, 8: lowerband

    plus_count = 0

    for i in range(len(vals)):
        # db 에 있는 data 는 date column 이 index 가 아니라서 위치가 하나 더 늘어 난다.
        u_price = vals[i][6]
        l_price = vals[i][8]
        index = vals[i][0]
        close_amt = vals[i][4]

        if u_price is None or l_price is None  or index is None or close_amt is None:
            continue

        # 양봉
        if vals[i][1] < vals[i][4]:
            plus_count += 1
        elif vals[i][4] < vals[i][1]:
            plus_count = 0

        if buy_flag is False:
            if close_amt <= l_price + ((l_price/100)*2) and min_plus <= plus_count:
                buy_flag = True
                count = buy(index, end_cash, close_amt)
        elif buy_flag is True:
            if u_price <= close_amt:
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


def backtest_bbands(symbol='ALL'):
    if symbol.startswith('ALL'):
        code_list, _, _ = market_code()
        code_list.sort()
    else:
        code_list = [symbol]

    plus_count = 0
    minus_count = 0
    for v in code_list:
        v, start_cash, end_cash, rate = bband_backtesting(v)
        if rate < 0:
            minus_count += 1
        elif 0 < rate:
            plus_count += 1

        # print(f'{v[4:]}, 시작: {start_cash:.2f}, 종료: {end_cash:.2f}, 실적: {rate:.2f}%')
        print(f'{v[4:]},{rate:.2f}')
        # time.sleep(0.2)

    print(plus_count, minus_count, f'{plus_count / (plus_count + minus_count) * 100:.2f}%')
##############################################################################


##############################################################################
# RSI, timeperiod=14 가 최적의 값임.
##############################################################################
def AddRSI(priceData, timeperiod=14):
    rsi = talib.RSI(priceData['close'], timeperiod=timeperiod)
    return priceData.assign(rsi=rsi).dropna().copy()


# buy: RSI < 30, sell: 70 < RSI
def rsi_backtesting(ticker, from_date='2022-01-01', to_date='2022-09-07'):
    start_cash = 10000000
    end_cash = 10000000
    buy_flag = False

    query = "select date, open, high, low, close, volume from day_candle " \
            "where symbol = '" + ticker[4:] + "' " \
            "and date >= '" + from_date + "' " \
            "and date <= '" + to_date + "' " \
            "order by date;"

    con = sqlite3.connect('./dbms/virtual_asset.db')
    df = pd.read_sql_query(query, con)
    if len(df) < 1:
        con.close()
        return ticker, 1, 1, 0

    dft = AddRSI(df, 14)
    vals = dft.values.tolist()
    lower_index = 30
    upper_index = 70.0
    # -9 가 최적임
    lower_rate = -5.0
    # 5 가 적당함
    upper_rate = 5.0


    # 0: date,  1: open,   2: high,      3: low
    # 4: close, 5: volume, 6: rsi

    plus_count = 0

    # vals[0][1] 의 위치는 14일 이후 의 data 부터 시작 한다.
    # rsi 의 timeperiod 의 값이 14로 설정되어 그 이전 값은 AddRSI(df, 14) 에서 NaN 이므로 제거됨.
    open_price = vals[0][1]
    close_price = vals[-1][4]

    for i in range(len(vals)):
        # db 에 있는 data 는 date column 이 index 가 아니라서 위치가 하나 더 늘어 난다.
        cur_rsi = vals[i][6]
        close_amt = vals[i][4]
        index = vals[i][0]

        # 양봉
        if vals[i][1] < vals[i][4]:
            plus_count += 1
        elif vals[i][4] < vals[i][1]:
            plus_count = 0

        if buy_flag is False:
            if cur_rsi <= lower_index and min_plus <= plus_count:
                buy_flag = True
                count = buy(index, end_cash, close_amt)
        elif buy_flag is True:
            if upper_index <= close_amt:
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

    return ticker, start_cash, end_cash, last_rate, open_price, close_price


def backtest_rsi(symbol='ALL'):
    if symbol.startswith('ALL'):
        code_list, _, _ = market_code()
        code_list.sort()
    else:
        code_list = [symbol]

    plus_count = 0
    minus_count = 0
    str_from = '2022-01-01'
    str_to = '2022-09-07'
    print(f'RSI 백테스팅: {str_from} ~ {str_to}')
    for v in code_list:
        v, start_cash, end_cash, rate, open_price, close_price = rsi_backtesting(v, from_date=str_from, to_date=str_to)
        if rate < 0:
            minus_count += 1
        elif 0 < rate:
            plus_count += 1

        earn = ((close_price / open_price) - 1.0) * 100.0
        # print(f'{v[4:]}, 시작: {start_cash:.2f}, 종료: {end_cash:.2f}, 실적: {rate:.2f}%')
        print(f'{v[4:]}, 실적:{rate:.2f}%, 시가:{open_price:.2f}, 종가:{close_price:.2f}, 등락:{earn:.2f}%')
        # time.sleep(0.2)

    print(f'수익종목수:{plus_count}, 손실종목수:{minus_count},  승률:{plus_count / (plus_count + minus_count) * 100:.2f}%')
##############################################################################

def main(argv):
    parser = argparse.ArgumentParser(description='옵션 지정 방법')
    parser.add_argument('--type', required=False, default='rsi', help='worktype rsi, bband, stocastic, default=rsi')
    parser.add_argument('--symbol', required=False, default='ALL', help='symbol (default=ALL)')
    parser.add_argument('--count', required=False, default=None, help='days (default=None, day_of_year)')
    parser.add_argument('--backtest', required=False, default='NO', help='BackTesting YES/NO (default=NO)')
    parser.add_argument('--period', required=False, default=20, help='period nday (default=5)')
    parser.add_argument('--periodk', required=False, default=20, help='period K (default=3)')
    parser.add_argument('--periodd', required=False, default=20, help='period D (default=3)')
    parser.add_argument('--lower', required=False, default=20, help='Lower limit percent (default=20)')
    parser.add_argument('--upper', required=False, default=70, help='Upper limit percent (default=70)')
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
    work_type = args.type

    if count is None:
        count = datetime.now().timetuple().tm_yday

    if backtest.upper().startswith('YES'):
        if  work_type.lower().startswith('rsi'):
            backtest_rsi(symbol)
        elif work_type.lower().startswith('bband'):
            backtest_bbands(symbol)
        elif  work_type.lower().startswith('stocastic'):
            backtest_stocastic(symbol, count, period, periodk, periodd, lower, upper, earnlow, earnhigh)

if __name__ == "__main__":
    main(sys.argv)

# run: python get_ohlcv.py -c 7 -t kava -i d
# 일단위 data 수집시, 최고가 일자 _data, 최저가 일자 _data print 하도록 수정 필요.
# BTC market 가격 반영
