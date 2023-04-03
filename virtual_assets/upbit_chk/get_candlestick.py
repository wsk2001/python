from huobi.client.market import MarketClient
from huobi.constant import *
from huobi.utils import *
import time
import sys, getopt, signal

market_client = MarketClient(init_log=True)

def exit_gracefully(signal, frame):
    sys.exit(0)

def get_stick(t):
    # interval = CandlestickInterval.MIN5
    interval = CandlestickInterval.DAY1
    # symbol = "ethusdt"
    symbol = t + "usdt"
    list_obj = market_client.get_candlestick(symbol, interval, 5)

    o = list_obj[0].open
    h = list_obj[0].high
    l = list_obj[0].low
    c = list_obj[0].close
    r = ((list_obj[0].close / list_obj[0].open) - 1.0) * 100.0
    print(f'{t}, {o}, {h}, {l}, {c}, {r:3.3f}')


def main(argv):
    while True:
        print('pvt - 0.000337 (count-847,821.48)')
        get_stick('rndr')
        get_stick('pvt')
        get_stick('btc')
        print('')
        time.sleep(10)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit_gracefully)
    main(sys.argv)
