import time
import datetime
import sys, getopt
import pyupbit
from time import sleep

'''
출처: https://superhky.tistory.com/282
'''

def rising_market(ticker):
    df = pyupbit.get_ohlcv(ticker)
    new_df = df['close']

    chk_mov = df['close'].rolling(window=20, min_periods=1).mean()

    short_ema = df.close.ewm(span=12, adjust=False).mean()

    long_ema = df.close.ewm(span=26, adjust=False).mean()

    chk_macd = short_ema - long_ema

    rising_signal = chk_macd.ewm(span=9, adjust=False).mean()

    ema = df['close'].ewm(span=100, adjust=False).mean()

    price = pyupbit.get_current_price(ticker)

    if 2 < len(chk_macd):
        if (chk_macd[-1] > rising_signal[-1]) \
                and (chk_macd[-1] > chk_macd[-2]) \
                and (price > ema[-1]) \
                and (price > chk_mov[-1]) \
                and (price > new_df[-2]):

            df = pyupbit.get_ohlcv(ticker, count=1)
            open_price = df['open'][0]
            close_price = df['close'][0]
            earning = ((close_price / open_price) - 1.0) * 100.0

            cur_dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:')
            print(cur_dt, ticker, open_price, close_price, f'{earning:10.2f}%', "expected to rise")

            return True


def main(argv):
    while True:
        try:
            tickers = pyupbit.get_tickers(fiat="KRW")
            cur = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:')
            print(cur, "checking...")

            for ticker in tickers:
                rising_market(ticker)
                time.sleep(0.2)

            time.sleep(300)

        except Exception as e:

            print(e)
            time.sleep(1)

if __name__ == "__main__":
    main(sys.argv)
