from numpy.core.numeric import False_
import pandas as pd
import os.path
import ccxt
import time
import requests
import ta

from pprint import pprint
from os import path
from datetime import datetime as dt
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.trend import MACD, IchimokuIndicator
from datetime import datetime


def buy_check(coin_name, rsi_val, MACD_diff_val, MACD_signal_val, stochast_k, stochast_d, ichimoku_cloud, df):
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
                    swing_low_price = min(
                        df.iloc[-2]['close'], df.iloc[-2]['open'])
                    for j in range(30):
                        if swing_low_price >= min(df.iloc[(j + 2) * -1]['close'], df.iloc[(j + 2) * -1]['open']):
                            swing_low_price = min(
                                df.iloc[(j + 2) * -1]['close'], df.iloc[(j + 2) * -1]['open'])
                        else:
                            break
                    swing_low = open('swing_low.txt', 'w')
                    swing_low.write(str(swing_low_price))
                    swing_low.close()

                    last_bought = open('last_bought.txt', 'r')
                    last_bought_coin = str(last_bought.readline())
                    last_bought.close()

                    if last_bought_coin != coin_name:
                        return True


def sell_check(coin_name):
    swing_low = open('swing_low.txt', 'rt')
    stop_lose = float(swing_low.readline())
    swing_low.close()
    profit_sell_val = stop_lose * 1.5

    balance = binance.fetch_balance()

    while balance['free']['USDT'] <= 10:
        sell_book = binance.fetch_order_book(coin_name)
        bars = binance.fetch_ohlcv(i, interval, limit=200)
        df = pd.DataFrame(
            bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

        rsi_indicator = RSIIndicator(df['close'])
        rsi_val = rsi_indicator.rsi()

        stochast_indicator = StochasticOscillator(
            df['high'], df['low'], df['close'])
        stochast_k = stochast_indicator.stoch()
        stochast_d = stochast_indicator.stoch_signal()

        balance = binance.fetch_balance()
        print('---------------------------------------')
        print(dt.now().strftime('%Y-%m-%d %H:%M:%S'))
        print('%s__TRADING' % coin_name)
        print('')
        print('Balance     : $' +
              str(round(bars[-1][4] * balance['free'][coin_name[:-5]], 2)))
        print('')
        print('Current ask : $' + str(sell_book['asks'][0][0]))
        print('')
        print('Stop lose   : $' + str(stop_lose))
        print('RSI_Val     : ' + str(rsi_val.iloc[-1]))
        print('Stochast_k  : ' + str(stochast_k.iloc[-1]))
        print('Stochast_b  : ' + str(stochast_d.iloc[-1]))
        print('Volume      : ' + str(bars[-1][5]))
        print('')
        print('Profit_sell : $' + str(profit_sell_val))
        print('---------------------------------------')

        if rsi_val.iloc[-1] >= 70:
            sell(coin_name)
        elif stochast_k.iloc[-1] >= 80 or stochast_d.iloc[-1] >= 80:
            sell(coin_name)
        elif sell_book['asks'][0][0] >= profit_sell_val:
            sell(coin_name)
        elif sell_book['asks'][0][0] <= stop_lose:
            sell(coin_name)
        balance = binance.fetch_balance()


def possible_pump():
    all_binance_market = binance.fetch_markets()
    usdt_volume_checker = []

    for i in all_binance_market:
        if i['symbol'][-4:] == 'USDT':
            usd_checker = i['symbol'][:-4]
            if 'USD' not in usd_checker:
                temp = binance.fetch_ohlcv(i['symbol'], '1d')
                print('Checking ' + str(i['symbol']))
                if len(temp) >= 2:
                    if temp[-1][1] <= temp[-1][4]:
                        symbol_volume = (
                            i['symbol'], 100 / temp[-1][1] * temp[-1][4], temp[-1][5])
                        if 'MARKET' in i['info']['orderTypes']:
                            usdt_volume_checker.append(symbol_volume)

    usdt_volume_checker.sort(key=lambda x: -x[2])
    if len(usdt_volume_checker) >= 100:
        usdt_volume_checker = usdt_volume_checker[0:100]
    usdt_volume_checker.sort(key=lambda x: -x[1])

    return usdt_volume_checker


def buy(coin_name):
    # 잔고를 보고 매수 할 수 있으면 호가 매수
    balance = binance.fetch_balance()
    if balance['free']['USDT'] >= 10:
        bal = balance['free']['USDT']

        orderbook = binance.fetch_order_book(coin_name)

        checker = True
        amount = bal/orderbook['bids'][0][0]
        drop_decimal = -1
        while checker:
            try:
                binance.create_market_buy_order(
                    coin_name, amount)
            except:
                amount = str(amount)
                amount = amount[:drop_decimal]
                amount = float(amount)
                drop_decimal = drop_decimal - 1
            else:
                checker = False
            time.sleep(2)

        time.sleep(2)

        if len(binance.fetch_open_orders(coin_name)) != 0:
            buy_cancel(coin_name)

        text = coin_name + '\n매수: $' + \
            str(round(bal, 2)) + '\n매수 가격: $' + str(orderbook['bids'][0][0])
        post_message(slack_token, "#bitcoin", text)

        last_bought = open('last_bought.txt', 'w')
        last_bought.write(str(coin_name))
        last_bought.close()

        sell_check(coin_name)


def buy_cancel(coin_name):
    order_id = binance.fetch_open_orders(coin_name)
    order_id = order_id[0]['info']['orderId']
    binance.cancel_order(int(order_id), coin_name)
    buy(coin_name)


def sell(coin_name):
    sell_coin = coin_name[:-5]

    all_binance_market = binance.fetch_markets()
    for i in all_binance_market:
        if i['symbol'] == coin_name:
            amount = i['limits']['amount']['min']

    # 발랜스 보고 코인으로 잔고가 있으면 호가 매도
    balance = binance.fetch_balance()

    if balance['free'][sell_coin] >= amount:
        binance.create_market_sell_order(
            coin_name, balance['free'][sell_coin])

        time.sleep(5)

        if len(binance.fetch_open_orders(coin_name)) != 0:
            sell_cancel(coin_name)

        bal = binance.fetch_balance()
        bal = bal['free']['USDT']
        text = coin_name + '\n매도: $' + str(round(bal, 2))
        post_message(slack_token, "#bitcoin", text)


def sell_cancel(coin_name):
    order_id = binance.fetch_open_orders(coin_name)
    order_id = order_id[0]['info']['orderId']
    binance.cancel_order(int(order_id), coin_name)
    sell(coin_name)


def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
                             headers={"Authorization": "Bearer " + token},
                             data={"channel": channel, "text": text}
                             )


if __name__ == '__main__':
    # key file read (binance token, secret token, slack token, timeframe)
    f = open('key.txt', 'r')
    data = f.read()
    f.close()

    # first & second line of key.txt = binance key, secret token
    binance = ccxt.binance(config={'apiKey': data.split('\n')[
        0], 'secret': data.split('\n')[1]})

    # third line of key.txt = slack token
    slack_token = data.split('\n')[2]

    # interval check
    interval = data.split('\n')[3]

    # when error occured and restarted program use this to go to sell_check
    balance = binance.fetch_balance()
    for i in balance['free']:
        if balance['free'][i] > 0 and i != 'USDT':
            price_data = binance.fetch_ohlcv(i + '/USDT', interval, limit=1)
            if price_data[0][4] * balance['free'][i] > 10:
                i = i + '/USDT'
                sell_check(i)

    while True:
        # find coins that might pump
        coin_to_trade = possible_pump()
        coin_length = 0
        if len(coin_to_trade) != 0:
            bought = False
            while bought is False:
                i = coin_to_trade[coin_length]

                bars = binance.fetch_ohlcv(i[0], interval, limit=200)
                df = pd.DataFrame(
                    bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

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
                Ichimoku_cloud = False
                count = 0
                for j in range(5):
                    if Ichimoku_a.iloc[j - 26] > Ichimoku_b.iloc[j - 26]:
                        count = count + 1
                if count == 5:
                    Ichimoku_cloud = True

                print('---------------------------------------')
                print(dt.now().strftime('%Y-%m-%d %H:%M:%S'))
                print(str(i[0]) + '__TRADING')
                print('')
                print('Stochast_K : ' + str(stochast_k.iloc[-1]))
                print('Stochast_D : ' + str(stochast_d.iloc[-1]))
                print('RSI        : ' + str(rsi_val.iloc[-1]))
                print('MACD_Diff  : ' + str(MACD_diff_val.iloc[-1]))
                print('MACD_Signal: ' + str(MACD_signal_val.iloc[-1]))
                print('Ichimoku   : ' + str(Ichimoku_cloud))
                print('')
                bought = buy_check(i[0], rsi_val, MACD_diff_val,
                                   MACD_signal_val, stochast_k, stochast_d, Ichimoku_cloud, df)

                if bought:
                    buy(i[0])
                print('---------------------------------------')
                print('')

                coin_length = coin_length + 1
                if coin_length >= len(coin_to_trade):
                    bought = True
        else:
            print('NO COIN PUMP YET')
