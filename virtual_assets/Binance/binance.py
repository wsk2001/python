# -*- coding: utf-8 -*-

import ccxt
import pandas as pd

# https://wikidocs.net/31065
# max 1,000 rows

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

    # for ticker in usdt_tickers:
    #     print(ticker)


#  timeframes: '1m','3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M'
def get_binance_ohlcv(symbol, limit=1000, timeframe='1d', since=None):
    binance = ccxt.binance()
    tickers = binance.fetch_ohlcv(symbol=symbol+'/USDT', timeframe=timeframe, since=since, limit=limit)

    df = pd.DataFrame(tickers, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
    df.set_index('datetime', inplace=True)

    return df


def main():
    get_binance_usdt_tickers()

    t = 'BTC'
    limit = 1000
    timeframe = '1d'
    since = '2017-08-17'
    since = int(pd.to_datetime(since).timestamp() * 1000)
    df = get_binance_ohlcv(t, limit, timeframe)
    print(df)


if __name__ == "__main__":
    main()


# date='2017-08-17'
# date = int(pd.to_datetime(date).timestamp()*1000)
#
# btc = binance.fetch_ohlcv(
#     symbol="BTC/USDT",
#     timeframe='1d',
#     since=date,
#     limit=5000)
#
# df = pd.DataFrame(btc, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
# df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
# df.set_index('datetime', inplace=True)
#
# vals = df.values.tolist()
# idxs = df.index.tolist()
#
# i = 0
# for indexs, values in zip(idxs, vals):
#     print(indexs, values)
#     i += 1
#
# print(i)
