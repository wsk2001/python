# -*- coding:utf-8 -*-

import time, sys, getopt, signal
import requests
import json
from common.utils import get_binance_btc
from common.dominance import get_dominance
import ccxt, cbpro, datetime

from tradingview_ta import TA_Handler, Interval, Exchange
import pyupbit


def get_ta(symbol, screener, exchange, interval):
    return TA_Handler(
        symbol=symbol,
        screener=screener,
        exchange=exchange,
        interval=interval,
    ).get_analysis().summary


def buy_sell_binance(ticker, interval):
    dt = get_ta(ticker + "USDT", "CRYPTO", "Binance", interval)
    print(type(dt))
    print(dt)
    cur = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    op_btc, price = get_binance_btc(ticker)
    earn = ((price / op_btc) - 1.0) * 100.0
    p = price
    recmd = dt['RECOMMENDATION']
    pr = "{:0,.3f}".format(p)
    print(cur + ': ' f'{ticker:<6}', f'{recmd:<10}', f'{str(dt["BUY"]):>4}',
          f'{str(dt["SELL"]):>4}', f'{str(dt["NEUTRAL"]):>4}', f'  {pr:>14}', f'{earn:6.2f}%')

    # dt1 = TA_Handler(ticker + "USDT", "CRYPTO", "Binance", interval).get_analysis().
    # print(type(dt1))
    # print(dt1)


if __name__ == "__main__":
    buy_sell_binance('BTC', '1d')