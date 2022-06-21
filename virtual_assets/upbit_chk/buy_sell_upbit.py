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


def buy_sell_upbit(ticker):
    handler = TA_Handler(
        symbol=ticker+"KRW",
        exchange="UPBIT",
        screener="crypto",
        interval=Interval.INTERVAL_1_HOUR
    )
    dt = handler.get_analysis().summary
    print(ticker + ':', dt['RECOMMENDATION'], dt['BUY'], dt['SELL'], dt['NEUTRAL'] )


def main(argv):
    lst = pyupbit.get_tickers(fiat="KRW")
    earns = [[]]

    earns.clear()

    for v in lst:
        buy_sell_upbit(v[4:])
        time.sleep(0.1)


if __name__ == "__main__":
    main(sys.argv)
