import schedule
import pandas as pd
import warnings
import sys, getopt
from datetime import datetime
import time
import pyupbit

# https://github.com/hackingthemarkets/supertrend-crypto-bot

pd.set_option('display.max_rows', None)
warnings.filterwarnings('ignore')

ticker = 'KRW-MANA'

def tr(data):
    data['previous_close'] = data['close'].shift(1)
    data['high-low'] = abs(data['high'] - data['low'])
    data['high-pc'] = abs(data['high'] - data['previous_close'])
    data['low-pc'] = abs(data['low'] - data['previous_close'])

    tr = data[['high-low', 'high-pc', 'low-pc']].max(axis=1)

    return tr


def atr(data, period):
    data['tr'] = tr(data)
    atr = data['tr'].rolling(period).mean()

    return atr


def supertrend(df, period=7, atr_multiplier=3):
    hl2 = (df['high'] + df['low']) / 2
    df['atr'] = atr(df, period)
    df['upperband'] = hl2 + (atr_multiplier * df['atr'])
    df['lowerband'] = hl2 - (atr_multiplier * df['atr'])
    df['in_uptrend'] = True

    for current in range(1, len(df.index)):
        previous = current - 1

        if df['close'][current] > df['upperband'][previous]:
            df['in_uptrend'][current] = True
        elif df['close'][current] < df['lowerband'][previous]:
            df['in_uptrend'][current] = False
        else:
            df['in_uptrend'][current] = df['in_uptrend'][previous]

            if df['in_uptrend'][current] and df['lowerband'][current] < df['lowerband'][previous]:
                df['lowerband'][current] = df['lowerband'][previous]

            if not df['in_uptrend'][current] and df['upperband'][current] > df['upperband'][previous]:
                df['upperband'][current] = df['upperband'][previous]

    return df


in_position = False


def check_buy_sell_signals(df):
    global in_position

    print("checking for buy and sell signals", ticker.upper())
    print(df.tail(5))
    last_row_index = len(df.index) - 1
    previous_row_index = last_row_index - 1

    if not df['in_uptrend'][previous_row_index] and df['in_uptrend'][last_row_index]:
        print("changed to uptrend, buy")
        if not in_position:
            # order = exchange.create_market_buy_order('ETH/USD', 0.05)
            # print(order)
            in_position = True
        else:
            print("already in position, nothing to do")

    if df['in_uptrend'][previous_row_index] and not df['in_uptrend'][last_row_index]:
        if in_position:
            print("changed to downtrend, sell")
            # order = exchange.create_market_sell_order('ETH/USD', 0.05)
            # print(order)
            in_position = False
        else:
            print("You aren't in position, nothing to sell")


def run_bot():
    global ticker
    print(f"Fetching new bars for {datetime.now().isoformat()}")
    bars = pyupbit.get_ohlcv(ticker, interval='minute1', count=100, period=1)
    df = pd.DataFrame(bars[:-1], columns=['open', 'high', 'low', 'close', 'volume'])

    supertrend_data = supertrend(df)

    check_buy_sell_signals(supertrend_data)


schedule.every(10).seconds.do(run_bot)

def main(argv):
    global ticker
    try:
        opts, etc_args = getopt.getopt(argv[1:], "ht:", ["help", "ticker="])

    except getopt.GetoptError:
        print(argv[0], '-t <ticker symbol>')
        print('ex) python', f'{argv[0]}', '-t mana')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(argv[0], '-t <ticker symbol>')
            print('ex) python', f'{argv[0]}', '-t mana')
            sys.exit()

        elif opt in ("-t", "--ticker"):  # ticker symbol
            ticker = 'KRW-' + arg

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main(sys.argv)