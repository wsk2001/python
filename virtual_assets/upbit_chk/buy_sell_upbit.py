#-*- coding:utf-8 -*-

import time, sys, getopt
import requests
import json
from common.utils import get_binance_btc
from common.dominance import get_dominance
import ccxt, cbpro, datetime

from tradingview_ta import TA_Handler, Interval, Exchange
import pyupbit


# Coinbase Index
def get_usdt_price():
    handler = TA_Handler(
        symbol="USDTUSD",
        exchange="KRAKEN",
        screener="crypto",
        interval=Interval.INTERVAL_1_MINUTE
    )
    usdt = float(handler.get_analysis().indicators['close'])
    return usdt


def earning(v):
    df = pyupbit.get_ohlcv('KRW-'+ v, count=1)
    open_price = df['open'][0]
    close_price = df['close'][0]
    res = ((close_price / open_price) - 1.0) * 100.0
    return res, close_price


# INTERVAL_1_MINUTE = "1m"
# INTERVAL_5_MINUTES = "5m"
# INTERVAL_15_MINUTES = "15m"
# INTERVAL_30_MINUTES = "30m"
# INTERVAL_1_HOUR = "1h"
# INTERVAL_2_HOURS = "2h"
# INTERVAL_4_HOURS = "4h"
# INTERVAL_1_DAY = "1d"
# INTERVAL_1_WEEK = "1W"
# INTERVAL_1_MONTH = "1M"

Recommendation = {'STRONG_BUY': '강한 매수', 'BUY': '매수', 'SELL': '매도', 'STRONG_SELL': '강한 매도', 'NEUTRAL': '중립'}


def buy_sell_upbit(ticker, interval):
    handler = TA_Handler(
        symbol=ticker+"KRW",
        exchange="UPBIT",
        screener="crypto",
        interval=interval
    )
    dt = handler.get_analysis().summary
    cur = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    earn, p = earning(ticker)
    print(cur + ':',  ticker + ',', Recommendation[str(dt['RECOMMENDATION'])]+',', str(dt['BUY'])+',',
          str(dt['SELL'])+',', str(dt['NEUTRAL'])+',',  f'{p:8.3f},', f'{earn:6.2f}%')


def main(argv):
    sleep_sec = 10.0
    interval = "5m"
    lst = pyupbit.get_tickers(fiat="KRW")
    earns = [[]]
    earns.clear()

    try:
        opts, etc_args = getopt.getopt(argv[1:], "hs:i:f:", ["sleep=", "interval=", "filename="])

    except getopt.GetoptError:
        print(argv[0], '-s <sleep seconds> -i <interval> -f <filename>')
        print('')
        print('interval')
        print('\t1m  \tInterval 1 minute')
        print('\t5m  \tInterval 5 minutes')
        print('\t15m \tInterval 15 minutes')
        print('\t30m \tInterval 30 minutes')
        print('\t1h  \tInterval 1 hour')
        print('\t2h  \tInterval 2 hours')
        print('\t4h  \tInterval 4 hours')
        print('\t1d  \tInterval 1 day')
        print('\t1W  \tInterval 1 week')
        print('\t1M  \tInterval 1 month(X)')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(argv[0], '-s <sleep seconds> -i <interval> -f <filename>')
            print('interval')
            print('\t1m  \tInterval 1 minute')
            print('\t5m  \tInterval 5 minutes')
            print('\t15m \tInterval 15 minutes')
            print('\t30m \tInterval 30 minutes')
            print('\t1h  \tInterval 1 hour')
            print('\t2h  \tInterval 2 hours')
            print('\t4h  \tInterval 4 hours')
            print('\t1d  \tInterval 1 day')
            print('\t1W  \tInterval 1 week')
            print('\t1M  \tInterval 1 month(X)')

            sys.exit()

        elif opt in ("-s", "--sleep"):
            sleep_sec = int(arg.strip())

        elif opt in("-i", "--interval"):
            interval = arg.strip()

        elif opt in("-f", "--filename"):
            filename = arg.strip()

    print('Interval: '+interval)
    print('시각, 심볼, 추천, 매수, 매도, 중립(지수), 가격, 등/락')
    while True:
        # buy_sell_upbit('ALGO', Interval.INTERVAL_30_MINUTES)
        # time.sleep(10)

        lst_mon = ['KRW-WAVES', 'KRW-BTC', 'KRW-ETH']
        for v in lst_mon:
            buy_sell_upbit(v[4:], interval)
            time.sleep(0.1)

        print('')
        time.sleep(sleep_sec)
        # break

if __name__ == "__main__":
    main(sys.argv)
