# -*- coding: utf-8 -*-

import datetime
import ccxt
import pandas as pd
import argparse

# 한글 폰트 사용을 위해서 세팅 (아래 4줄)
from matplotlib import font_manager, rc
font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

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

    parser = argparse.ArgumentParser(description='옵션 지정 방법')
    parser.add_argument('--count', required=False, default=1000, help='수집 data 갯수 (default=1000, max=1000)')
    parser.add_argument('--symbol', required=False, default='btc', help='심볼 (BTC, ETH, ADA, ..., default=btc)')
    parser.add_argument('--interval', required=False, default='1d',
                        help='candle 종류 (1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M)')
    parser.add_argument('--startdate', required=False, default=None, help='시작 일자(yyyy-mm-dd, default=현재 일자)')
    parser.add_argument('--starttime', required=False, default='00:00:00', help='시작 시각(hh:mm:ss, default=현재 시각)')

    args = parser.parse_args()
    count = int(args.count)
    symbol = args.symbol
    timeframe = args.interval
    startdate = args.startdate
    starttime = args.starttime

    # if starttime is None:
    #     starttime = datetime.datetime.now().strftime('%H:%M:%S')

    if startdate is None:
        startdate = datetime.datetime.now().strftime('%Y-%m-%d')
        one_day_sec = 86400
        str_since = startdate + ' ' + starttime
        since = int(((pd.to_datetime(str_since).timestamp()-one_day_sec)*1000))
    else:
        since = int((pd.to_datetime(startdate).timestamp()*1000))

    df = get_binance_ohlcv(symbol.upper(), count, timeframe, since)
    # df = get_binance_ohlcv(symbol.upper(),count,timeframe )

    vals = df.values.tolist()
    idxs = df.index.tolist()

    for indexs, values in zip(idxs, vals):
        print(indexs, values[3])


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
