import time
import datetime
import sys, getopt
import pyupbit
from time import sleep

'''
출처: https://superhky.tistory.com/282
'''
def rising_market(ticker) :
    df = pyupbit.get_ohlcv(ticker)
    new_df = df['close']

    open_price = df['open'][-1]
    close_price = df['close'][-1]
    earning = ((close_price / open_price) - 1.0) * 100.0

    MOV      = df['close'].rolling(window=20, min_periods=1).mean()
    ShortEMA = df.close.ewm(span=12, adjust=False).mean()
    LongEMA  = df.close.ewm(span=26, adjust=False).mean()
    MACD     = ShortEMA-LongEMA
    Signal   = MACD.ewm(span=9, adjust=False).mean()
    EMA      = df['close'].ewm(span=100, adjust=False).mean()
    price    = pyupbit.get_current_price(ticker)

    if (MACD[-1] > Signal[-1]) \
        and (MACD[-1] > MACD[-2]) \
        and (price > EMA[-1]) \
        and (price > MOV[-1]) \
        and (price > new_df[-2]):
        return True, earning, close_price

    return False, 0.0, close_price

def main(argv):
    tickers = pyupbit.get_tickers(fiat="KRW")
    cur = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:')
    print(cur, "checking...")

    for ticker in tickers:
        res, earn, close_price = rising_market(ticker)
        if res is True:
            print( ticker, close_price, f'{earn:6.2f}%' )
        time.sleep(0.2)

    cur = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:')
    print(cur, "end of check.")

if __name__ == "__main__":
    main(sys.argv)
