import time
import pyupbit
import datetime
import pandas as pd
import requests
import webbrowser
import numpy as np

a = 1

f = open("upbit.txt")
lines = f.readlines()
access = lines[0].strip()
secret = lines[1].strip()
f.close()

upbit = pyupbit.Upbit(access, secret)


def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=20)
    k = 1 - abs(df.iloc[0]['open'] - df.iloc[0]['close']) / (df.iloc[0]['high'] - df.iloc[0]['low'])
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    print(target_price)
    return target_price


def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute1", count=1)
    start_time = df.index[0]
    return start_time


def get_ma20(ticker):
    """20일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=20)
    ma20 = df['close'].rolling(window=20, min_periods=1).mean().iloc[-1]
    print(ma20)
    return ma20


def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0


def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]


if a == 1:
    url = "https://www.bybit.com/?affiliate_id=17490&language=en-US&group_id=0&group_type=2"
    webbrowser.open(url)
    a = 2

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    def goldencross(symbol):
        url = "https://api.upbit.com/v1/candles/minutes/240"

        querystring = {"market": symbol, "count": "100"}

        response = requests.request("GET", url, params=querystring)

        data = response.json()

        df = pd.DataFrame(data)

        df = df['trade_price'].iloc[::-1]

        ma20 = df.rolling(window=20, min_periods=1).mean()
        ma60 = df.rolling(window=60, min_periods=1).mean()

        test1 = ma20.iloc[-2] - ma60.iloc[-2]
        test2 = ma20.iloc[-1] - ma60.iloc[-1]

        call = '해당없음'

        if test1 > 0 and test2 < 0:
            call = '데드크로스'

        if test1 < 0 and test2 > 0:
            call = '골든크로스'

        print(symbol)
        print('이동평균선 20: ', round(ma20.iloc[-1], 2))
        print('이동평균선 60: ', round(ma60.iloc[-1], 2))
        print('골든크로스/데드크로스: ', call)
        print('')
        time.sleep(1)


    goldencross('KRW-CBK')

    print("Try")
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-CBK")
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-CBK", 0.5)
            ma20 = get_ma20("KRW-CBK")
            current_price = get_current_price("KRW-CBK")
            if target_price < current_price and ma20 < current_price:
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order("KRW-CBK", krw * 0.9995)
        else:
            CBK = get_balance("CBK")
            if CBK > 0.44:
                upbit.sell_market_order("KRW-CBK", CBK * 0.9995)
        time.sleep(1)

    except Exception as e:
        print(e)
        time.sleep(1)
