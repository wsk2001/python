# -*- coding: utf-8 -*-

"""
저항선/지지선  구하는 알고리즘 App
.
"""

import time, sys
import argparse
import ccxt

def get_binance_ohlcv(ticker, count=1):
    binance = ccxt.binance()
    ohlcv = binance.fetch_ohlcv(ticker.upper() + '/USDT', timeframe='1d', limit=count)
    o = 0
    h = 0
    l = 0
    c = 0

    start_flag = True

    for v in ohlcv:
        if start_flag == True:
            o = v[1]
            h = v[2]
            l = v[3]
            c = v[4]
            start_flag = False
        else :
            if h < v[2]:
                h = v[2]
            if l > v[3]:
                l = v[3]

        c = v[4]

    return o, h, l, c

def pp_traditional(high, low, close):
    PP = (high + low + close) / 3
    R1 = PP * 2 - low
    S1 = PP * 2 - high
    R2 = PP + (high - low)
    S2 = PP - (high - low)
    R3 = PP * 2 + (high - 2 * low)
    S3 = PP * 2 - (2 * high - low)
    R4 = PP * 3 + (high - 3 * low)
    S4 = PP * 3 - (3 * high - low)
    R5 = PP * 4 + (high - 4 * low)
    S5 = PP * 4 - (4 * high - low)

    #return round(PP,2), round(R1,2), round(R2,2), round(R3,2), round(R4,2), round(R5,2), round(S1,2), round(S2,2), round(S3,2), round(S4,2), round(S5,2)
    return round(PP,2), round(S1,2), round(R1,2)

def pp_fibonacci(high, low, close):
    PP = (high + low + close) / 3
    R1 = PP + 0.382 * (high - low)
    S1 = PP - 0.382 * (high - low)
    R2 = PP + 0.618 * (high - low)
    S2 = PP - 0.618 * (high - low)
    R3 = PP + (high - low)
    S3 = PP - (high - low)

    #return round(PP,2), round(R1,2), round(R2,2), round(R3,2), round(S1,2), round(S2,2), round(S3,2)
    return round(PP,2), round(S1,2), round(R1,2)


def pp_woodie(high, low, close):
    PP = (high + low + 2 * close) / 4
    R1 = 2 * PP - low
    S1 = 2 * PP - high
    R2 = PP + (high - low)
    S2 = PP - (high - low)
    R3 = high + 2 * (PP - low)
    S3 = low - 2 * (high - PP)
    R4 = R3 + (high - low)
    S4 = S3 - (high - low)

    return round(PP, 2), round(S1, 2), round(R1, 2)


def pp_classic(high, low, close):
    PP = (high + low + close) / 3
    R1 = 2 * PP - low
    S1 = 2 * PP - high
    R2 = PP + (high - low)
    S2 = PP - (high - low)
    R3 = PP + 2 * (high - low)
    S3 = PP - 2 * (high - low)
    R4 = PP + 3 * (high - low)
    S4 = PP - 3 * (high - low)

    return round(PP, 2), round(S1, 2), round(R1, 2)


def pp_demark(open, high, low, close):
    if open == close:
        X = high + low + 2 * close
    else:
        if close > open:
            X = 2 * high + low + close
        else:
            X = 2 * low + high + close

    PP = X / 4
    R1 = X / 2 - low
    S1 = X / 2 - high

    return round(PP, 2), round(S1, 2), round(R1, 2)


def pp_camarilla(high, low, close):
    PP = (high + low + close) / 3
    R1 = close + 1.1 * (high - low) / 12
    S1 = close - 1.1 * (high - low) / 12
    R2 = close + 1.1 * (high - low) / 6
    S2 = close - 1.1 * (high - low) / 6
    R3 = close + 1.1 * (high - low) / 4
    S3 = close - 1.1 * (high - low) / 4
    R4 = close + 1.1 * (high - low) / 2
    S4 = close - 1.1 * (high - low) / 2
    R5 = (high / low) * close
    S5 = close - (R5 - close)

    return round(PP, 2), round(S1, 2), round(R1, 2)

def main(argv):
    parser = argparse.ArgumentParser(description='옵션 지정 방법')
    parser.add_argument('--high', required=False, default=518, help='high price')
    parser.add_argument('--low', required=False, default=453, help='low price')
    parser.add_argument('--close', required=False, default=468, help='close price')

    args = parser.parse_args()
    h = float(args.high)
    l = float(args.low)
    c = float(args.close)

    o, h, l, c = get_binance_ohlcv('btc', 2)

    print('yesterday ohlcv:', get_binance_ohlcv('btc', 2))
    print()
    print('traditional  sr:', pp_traditional(h, l, c))
    print('fibonacci    sr:', pp_fibonacci(h, l, c))
    print('woodie       sr:', pp_woodie(h, l, c))
    print('classic      sr:', pp_classic(h, l, c))
    print('demark       sr:', pp_demark(o, h, l, c))
    print('camarilla    sr:', pp_camarilla(h, l, c))
    print()


if __name__ == "__main__":
    main(sys.argv)

# command line 에서 sqlite3 script 호출 하는 방법
# $ sqlite3.exe auction.db < work_script.sql

# py association_analysis.py --symbol=PUNDIX --earning=20 --range=3 --pick=20
