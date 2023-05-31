import time
import datetime
import sys, getopt
import pyupbit
from time import sleep
import pandas as pd

def trend(ticker):
    df = pyupbit.get_ohlcv(ticker)

    macd = pd.DataFrame()
    macd["MACD"] = df["close"].ewm(span=12, min_periods=12).mean() - df["close"].ewm(span=26, min_periods=26).mean()
    macd["Signal"] = macd["MACD"].ewm(span=9, min_periods=9).mean()
    golden_cross = macd["MACD"] >= macd["Signal"]

    if macd["MACD"].iloc[-1] > 0:
        return ticker, True, golden_cross
    return ticker, False, golden_cross

def main(argv):
    tickers = pyupbit.get_tickers(fiat="KRW")

    up_count = 0
    down_count = 0

    rising_list = []
    golden_cross = []

    rising_list.clear()
    golden_cross.clear()

    for ticker in tickers:
        symbol, res, gc = trend(ticker)
        print('.', end='')
        sys.stdout.flush()
        if res is True:
            up_count += 1
            rising_list.append(symbol)
        else:
            down_count += 1
        
        if gc is True:
            print(symbol)
            golden_cross.append(symbol)

        time.sleep(0.2)
    
    print()
    print('uptrend:', up_count, ',downtrend:', down_count)
    for s in rising_list:
        print(s)
    print()

    if 0 < len(golden_cross):
        print('golden closs ticker')
        for s in golden_cross:
            print(s)
        print()


if __name__ == "__main__":
    main(sys.argv)
