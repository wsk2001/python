#-*- coding:utf-8 -*-

import sys, time
import pandas as pd
from pycoingecko import CoinGeckoAPI
import pyupbit
import datetime
from common.utils import market_code
import ccxt
import argparse

usdt_tickers = []


# get binance usdt tickers
def get_binance_usdt_tickers():
    binance = ccxt.binance()
    markets = binance.fetch_tickers()

    usdt_tickers.clear()

    for ticker in markets.keys():
        if ticker.endswith('USDT'):
            usdt_tickers.append(ticker[:-5])

    usdt_tickers.sort()


def get_bithumb_tickers():
    bithumb_tickers = []
    bithumb = ccxt.bithumb()
    markets = bithumb.fetch_tickers()

    for ticker in markets.keys():
        bithumb_tickers.append(ticker[:-4])

    bithumb_tickers.sort()

    #print(bithumb_tickers)
    ohlcv = bithumb.fetchOHLCV('ARW'+'/KRW', timeframe='1d', limit=1)
    print(ohlcv)


def binance_cap():
    get_binance_usdt_tickers()

    cg = CoinGeckoAPI()
    markets_page1 = cg.get_coins_markets(vs_currency="usd", per_page=250, page=1)
    markets_page2 = cg.get_coins_markets(vs_currency="usd", per_page=250, page=2)
    markets_page3 = cg.get_coins_markets(vs_currency="usd", per_page=250, page=3)

    df1 = pd.DataFrame(markets_page1)[['id', 'symbol', 'name', 'market_cap']].set_index('id')
    df2 = pd.DataFrame(markets_page2)[['id', 'symbol', 'name', 'market_cap']].set_index('id')
    df3 = pd.DataFrame(markets_page3)[['id', 'symbol', 'name', 'market_cap']].set_index('id')

    df = pd.concat([df1, df2, df3])

    vals = df.values.tolist()
    idxs = df.index.tolist()

    cnt = 0
    print('바이낸스 시총 순위 (' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ')')
    print()
    print('순위,id,symbol,금액 단위(1,000$)')
    for index, value in zip(idxs, vals):
        count = usdt_tickers.count(value[0].upper())
        if 0 < count:
            cnt += 1
            print(f'{cnt}, {index}, {value[0].upper()}, ' + format(int(value[2]/1000), ',d'))
            # if 200 <= cnt:
            #     break


def upbit_cap():
    code_list, _, _ = market_code()
    cg = CoinGeckoAPI()

    markets_page = cg.get_coins_markets(vs_currency="KRW", per_page=250, page=1)
    df = pd.DataFrame(markets_page)[['id', 'symbol', 'name', 'market_cap']].set_index('id')

    for i in range(2,50):
        mp = cg.get_coins_markets(vs_currency="KRW", per_page=250, page=i)
        dft = pd.DataFrame(mp)[['id', 'symbol', 'name', 'market_cap']].set_index('id')
        df = pd.concat([df, dft])
        time.sleep(0.3)

    # df = pd.concat([df1, df2, df3, df4, df5, df6, df7])

    vals = df.values.tolist()
    idxs = df.index.tolist()

    cnt = 0
    print('업비트 시총 순위 (' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ')')
    print()
    print('순위,symbol,금액 단위(억원)')
    for index, value in zip(idxs, vals):
        if index.startswith('tokamak-network'):
            continue
        count = code_list.count('KRW-'+value[0].upper())
        if 0 < count:
            cnt += 1
            # print(cnt, index, value[0].upper(), value[2])
            print(f'{cnt}, {value[0].upper()}, ' + format(int(value[2]/100000000.0), ',d'))


def main(argv):
    parser = argparse.ArgumentParser(description='옵션 지정 방법')
    parser.add_argument('--market', required=False, default='upbit', help='market: upbit or binance (default=upbit)')

    args = parser.parse_args()
    market = args.market

    if market.startswith('upbit'):
        upbit_cap()
    elif market.startswith('bithumb'):
        get_bithumb_tickers()
    else:
        binance_cap()


if __name__ == "__main__":
    main(sys.argv)
