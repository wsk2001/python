from datetime import datetime as dt

import ta.volume
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.trend import MACD, IchimokuIndicator
import pyupbit
from common.utils import market_code
import time, sys


def buy_check_org(coin_name, rsi_val, MACD_diff_val, MACD_signal_val, stochast_k, stochast_d, ichimoku_cloud, df):
    # entry signal
    if rsi_val.iloc[-1] >= 50:
        print('')
        print('CASE 1: RSI OVER 50')
        if MACD_diff_val.iloc[-1] >= MACD_signal_val.iloc[-1]:
            print('CASE 2: MACD_D > MACD_S')
            if 20 <= stochast_k.iloc[-1] <= 80 and 20 <= stochast_d.iloc[-1] <= 80:
                print('CASE 3: STOCHASTIC < 80')
                if ichimoku_cloud:
                    print('CASE 4: ICHIMOKU GREEN')
                    return True


def buy_check(coin_name, rsi_val, MACD_diff_val, MACD_signal_val, stochast_k, stochast_d, ichimoku_cloud, df):
    # entry signal
    score = 0

    if rsi_val.iloc[-1] >= 50:
        # print('')
        # print('CASE 1: RSI OVER 50')
        score += 1

    if MACD_diff_val.iloc[-1] >= MACD_signal_val.iloc[-1]:
        # print('CASE 2: MACD_D > MACD_S')
        score += 1

    if 20 <= stochast_k.iloc[-1] <= 80 and 20 <= stochast_d.iloc[-1] <= 80:
        # print('CASE 3: STOCHASTIC < 80')
        score += 1

    if ichimoku_cloud:
        # print('CASE 4: ICHIMOKU GREEN')
        score += 1

    if 3 <= score:
        return True, score
    else:
        return False, score


def main(argv):

    code_list, _, _ = market_code()
    code_list.sort()
    recommand_list = []
    recommand_list.clear()
    for t in code_list:
        df = pyupbit.get_ohlcv(t, count=200, interval='day', period=1)

        rsi_indicator = RSIIndicator(df['close'])
        rsi_val = rsi_indicator.rsi()

        MACD_indicator = MACD(
            df['close'], window_slow=21, window_fast=8, window_sign=5)
        MACD_signal_val = MACD_indicator.macd_signal()
        MACD_diff_val = MACD_indicator.macd_diff()

        stochast_indicator = StochasticOscillator(
            df['high'], df['low'], df['close'])
        stochast_k = stochast_indicator.stoch()
        stochast_d = stochast_indicator.stoch_signal()

        Ichimoku_indicator = IchimokuIndicator(df['high'], df['low'])
        Ichimoku_a = Ichimoku_indicator.ichimoku_a()
        Ichimoku_b = Ichimoku_indicator.ichimoku_b()
        ichimoku_cloud = False

        count = 0
        for j in range(5):
            if Ichimoku_a.iloc[j - 26] > Ichimoku_b.iloc[j - 26]:
                count = count + 1
        if count == 5:
            ichimoku_cloud = True

        bought, score = buy_check(t, rsi_val, MACD_diff_val,
                           MACD_signal_val, stochast_k, stochast_d, ichimoku_cloud, df)
        if bought:
            print(t[4:] + f', score={score}, score max=4,', dt.now().strftime('%Y-%m-%d %H:%M:%S'))
            print('Stochast_K : ' + str(round(stochast_k.iloc[-1],2)))
            print('Stochast_D : ' + str(round(stochast_d.iloc[-1],2)))
            print('RSI        : ' + str(round(rsi_val.iloc[-1],2)))
            print('MACD_Diff  : ' + str(round(MACD_diff_val.iloc[-1],2)))
            print('MACD_Signal: ' + str(round(MACD_signal_val.iloc[-1],2)))
            print('Ichimoku   : ' + str(ichimoku_cloud) + f', count={count}')
            print('')
            recommand_list.append(t[4:])

        time.sleep(0.3)

    print('Summary (' + dt.now().strftime('%Y-%m-%d %H:%M:%S') + ')')
    for ticker in recommand_list:
        dfi = pyupbit.get_ohlcv('KRW-' + ticker, count=2, interval='day', period=1)
        open_price = dfi['open'][-1]
        close_price = dfi['close'][-1]
        earning = ((close_price / open_price) - 1.0) * 100.0
        print(ticker, round(earning, 2), '%')
        time.sleep(0.3)



if __name__ == "__main__":
    main(sys.argv)
