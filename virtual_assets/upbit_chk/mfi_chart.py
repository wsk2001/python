# -*- coding: utf-8 -*-

from common.utils import market_code
import time, datetime, sys, getopt
import talib as ta
import pyupbit
import matplotlib.pyplot as plt
import argparse

# 한글 폰트 사용을 위해서 세팅 (아래 4줄)
from matplotlib import font_manager, rc

font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)


def mfi(symbol, count):
    if not symbol.startswith('KRW-') and not symbol.startswith('BTC-') and not symbol.startswith('USDT-'):
        symbol = 'KRW-' + symbol

    df = pyupbit.get_ohlcv(symbol, count=count, period=1)
    rl = ta.MFI(high=df['high'], low=df['low'], close=df['close'], volume=df['volume'], timeperiod=14)
    return rl


# Main function
def main(argv):
    parser = argparse.ArgumentParser(description='옵션 지정 방법')
    parser.add_argument('--symbol', required=False, default='BTC', help='symbol (default=BTC)')
    parser.add_argument('--count', required=False, default=90, help='data gettering size (default=90)')

    args = parser.parse_args()
    count = int(args.count)
    symbol = args.symbol

    lst = mfi(symbol, count)
    cur_value = lst[-1]

    ax = plt.gca()
    plt.title(f'MFI(Money Flow Index): {symbol.upper()}')
    lst.plot(kind='line', x='name', y='currency', color='blue', label='현재값: ' + str(round(cur_value, 2)), ax=ax)
    plt.grid(True)
    plt.legend()

    plt.show()


if __name__ == "__main__":
    main(sys.argv)

# py rsi.py --up=60 --down=35
