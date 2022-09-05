# -*- coding: utf-8 -*-

import pyupbit
import pandas as pd
import matplotlib.pyplot as plt
import time


def draw_graph(list1, list_buy, list_sell, data):
    fig = plt.figure(figsize=(20, 5))
    for i in range(len(list1)):
        fig = plt.plot(list1[i])
    for i in range(len(list_buy)):
        fig = plt.axvspan(list_buy[i][0], list_buy[i][0], color='blue', alpha=0.1)
    for i in range(len(list_sell)):
        fig = plt.axvspan(list_sell[i][0], list_sell[i][0], color='red', alpha=0.1)
    fig = plt.legend()
    fig = plt.show()
    fig2 = plt.figure(figsize=(20, 2))
    fig2 = plt.plot(data['volume'])


def set_envelop(data, gap):
    ma20 = data['close'].rolling(window=20).mean()
    idx = ma20.index
    en_high, en_low = [], []
    for i in range(len(ma20)):
        en_high.append(ma20[i] + ((ma20[i] * gap) / 100))
        en_low.append(ma20[i] - ((ma20[i] * gap) / 100))
    en_high = pd.Series(en_high, index=idx)
    en_low = pd.Series(en_low, index=idx)
    return en_high, en_low


# 벡테스팅 함수
def buy(price, cash, finance, Average_price, div_count):
    div_count = div_count + 1
    buy_cash = cash / 3
    Average_price = ((Average_price * finance) + (price * buy_cash / price)) / (finance + buy_cash / price)
    finance = finance + buy_cash / price
    cash = cash - buy_cash
    return cash, finance, Average_price, div_count


def sell(price, cash, finance, Average_price, div_count):
    cash = finance * price + cash
    finance = 0
    Average_price = 0
    div_count = 0
    return cash, finance, Average_price, div_count

# 3 분할 매수, 매도는 한번에
# 분할 매수가 끝나지 않았으면 매도 못함 (로직 수정 필요)
def backtesting(name, data):
    start_cash = 10000000
    cash, finance, Average_price = start_cash, 0, 0
    div_count = 0
    list_buy, list_sell = [], []
    en_high, en_low = set_envelop(data, 3)

    for i in range(1, len(data)):
        if div_count < 3:
            if data['close'][i - 1] > en_low[i - 1] and data['close'][i] <= en_low[i]:
                print('buy', data.index[i], data['close'][i])
                cash, finance, Average_price, div_count = buy(en_low[i], cash, finance, Average_price, div_count)
                line = []
                line.append(data.index[i])
                line.append(i)
                list_buy.append(line)
        else:
            if data['close'][i - 1] < en_high[i - 1] and data['close'][i] >= en_high[i]:
                print('sell-1', data.index[i], data['close'][i])
                cash, finance, Average_price, div_count = sell(en_high[i], cash, finance, Average_price, div_count)
                line = []
                line.append(data.index[i])
                line.append(i)
                list_sell.append(line)
            elif data['close'][i] + Average_price * 5 / 100 >= Average_price:
                print('sell-2', data.index[i], data['close'][i])
                cash, finance, Average_price, div_count = sell(en_high[i], cash, finance, Average_price, div_count)
                line = []
                line.append(data.index[i])
                line.append(i)
                list_sell.append(line)
            elif data['close'][i] + Average_price * 5 / 100 <= Average_price:
                print('sell-3', data.index[i], data['close'][i])
                cash, finance, Average_price, div_count = sell(en_high[i], cash, finance, Average_price, div_count)
                line = []
                line.append(data.index[i])
                line.append(i)
                list_sell.append(line)
    """
    list1 = []
    list1.append(en_high)
    list1.append(en_low)
    list1.append(data['close'])
    draw_graph(list1,list_buy,list_sell,data)
    """
    print(name, '백테스팅 총 수익률:',
          round(((cash - start_cash + (finance * data['close'][len(data) - 1])) / start_cash) * 100, 2), '%')
    return round(((cash - start_cash + (finance * data['close'][len(data) - 1])) / start_cash) * 100, 2)


def main():
    code_name = ['KRW-BTC', 'KRW-ETH', 'KRW-SOL', 'KRW-GRS', 'KRW-HBAR']
    result = []

    for i in range(len(code_name)):
        line = []
        name = code_name[i]
        data = pyupbit.get_ohlcv(name, interval="minute60", count=1000)
        backtesting_result = backtesting(name, data)
        line.append(name)
        line.append(backtesting_result)
        result.append(line)
        time.sleep(0.3)

    print(result)

if __name__ == "__main__":
    main()
