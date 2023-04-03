#-*- coding:utf-8 -*-

import sys, time
import pandas as pd
from pycoingecko import CoinGeckoAPI
import datetime
from common.utils import market_code
import ccxt
import argparse

binance_tickers = []
bithumb_tickers = []
upbit_tickers = []


# get binance usdt tickers
def get_binance_usdt_tickers():
    binance = ccxt.binance()
    markets = binance.fetch_tickers()

    binance_tickers.clear()

    for ticker in markets.keys():
        if ticker.endswith('USDT'):
            binance_tickers.append(ticker[:-5])
        if ticker.endswith('BTC'):
            binance_tickers.append(ticker[:-4])
        if ticker.endswith('BNB'):
            binance_tickers.append(ticker[:-4])

    binance_tickers.sort()

def get_bithumb_tickers():
    bithumb = ccxt.bithumb()
    markets = bithumb.fetch_tickers()

    for ticker in markets.keys():
        if ticker.endswith('KRW'):
            bithumb_tickers.append(ticker[:-4])

    bithumb_tickers.sort()

    #ohlcv = bithumb.fetchOHLCV('ARW'+'/KRW', timeframe='1d', limit=1)
    #print(ohlcv)

def get_upbit_tickers():
    upbit = ccxt.upbit()
    markets = upbit.fetch_tickers()

    for ticker in markets.keys():
        if ticker.endswith('KRW'):
            upbit_tickers.append(ticker[:-4])

    upbit_tickers.sort()



def main(argv):
    get_binance_usdt_tickers()
    get_bithumb_tickers()
    get_upbit_tickers()

    for ticker in upbit_tickers:
        if ticker not in binance_tickers:
            print(ticker)


if __name__ == "__main__":
    main(sys.argv)
