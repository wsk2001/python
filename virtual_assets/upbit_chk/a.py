from huobi.client.market import MarketClient
from huobi.constant import *
from huobi.utils import *
import time
import sys, getopt, signal

market_client = MarketClient(init_log=True)

def exit_gracefully(signal, frame):
    sys.exit(0)

def get_stick(t):
    interval = CandlestickInterval.DAY1
    symbol = t + "usdt"
    list_obj = market_client.get_candlestick(symbol, interval, 180)
    print(len(list_obj))
    print(list_obj[179].close)

get_stick('btc')
