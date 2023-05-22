#-*- coding:utf-8 -*-

import time, sys, signal
import requests
import json
from common.utils import get_binance_btc
from common.dominance import get_dominance
import ccxt, cbpro, datetime
from tradingview_ta import TA_Handler, Interval, Exchange
import pyupbit
import requests
from datetime import timedelta

def funding_rate_binance():
    binance = ccxt.binance({'options': {
        'defaultType': 'future',
    }})

    fund = binance.fetch_funding_rate(symbol='BTC/USDT')
    return fund['interestRate']


def funding_rate_bybit():
    bybit = ccxt.bybit()
    tick = bybit.fetch_ticker(symbol='BTC/USDT')
    tick_info = tick['info']
    return tick_info['funding_rate']


def funding_rate_bitmex():
    bitmex = ccxt.bitmex()
    tick = bitmex.fetch_ticker(symbol='BTC/USD')
    tick_info = tick['info']
    return tick_info['fundingRate']


def get_fng():
    url = "https://api.alternative.me/fng/?limit="
    _url = url + "30"
    res = requests.request("GET", _url)

    parsed = json.loads(res.text)
    data = parsed["data"]

    ma = 0
    wa = 0
    sum = 0
    i = 0
    l = []
    l.clear()

    for d in data:
        sum += int(d["value"])
    ma = sum / 30

    sum = 0
    i = 0
    for d in data:
        sum += int(d["value"])
        i += 1
        l.append(int(d["value"]))
        if 7 <= i:
            break
    wa = sum / 7

    return l[0], l[1],  l[2],  l[3],  l[4],  l[5],  l[6],  wa, ma


# Coinbase Index
def cb_index(bn_p):
    public_client = cbpro.PublicClient()
    res = public_client.get_product_order_book('BTC-USD')
    cb_p = float(res["bids"][0][0])
    handler = TA_Handler(
        symbol="USDTUSD",
        exchange="KRAKEN",
        screener="crypto",
        interval=Interval.INTERVAL_1_MINUTE
    )
    ti = float(handler.get_analysis().indicators['close'])
    return cb_p, bn_p, cb_p - bn_p * ti, ti
    # return cb_p, bn_p, cb_p - bn_p, ((cb_p - bn_p) / bn_p) * 100

def calc_earn(v):
    try:
        df = pyupbit.get_ohlcv(v, count=2)
        o = df['open'][0]
        c = df['close'][0]
        p = ((c / o) - 1.0) * 100.0

        return v[4:], o, c, p
    except:
        return None, None, None, None


def upbit_top10():
    lst = pyupbit.get_tickers(fiat="KRW")
    earns = [[]]
    theme_dict = {}
    theme_dict.clear()
    count = 10

    # option: Up
    reverse_flag = True

    earns.clear()

    for v in lst:
        time.sleep(0.2)
        arr = calc_earn(v)
        if arr is not None:
            earns.append(list(arr))

    earns = sorted(earns, key=lambda x: x[3], reverse=reverse_flag)

    i = 0

    print()
    print('전일 상승률 top 10')
    for e in earns:
        print(f'{e[0]}, {e[3]:.2f}%')
        i += 1
        if count <= i:
            break
    print()


def get_coingecko_dominance():
    tmp_url = 'https://api.coingecko.com/api/v3/global'
    response = requests.get(tmp_url)
    data = json.loads(response.text)
    bitcoin_dominance = data['data']['market_cap_percentage']['btc']
    return bitcoin_dominance

def get_alternative_btc_dominance():
    tmp_url = 'https://api.alternative.me/v2/global'
    response = requests.get(tmp_url)
    data = json.loads(response.text)
    bitcoin_dominance = data['data']['bitcoin_percentage_of_market_cap']
    return bitcoin_dominance * 100.0



def main(argv):
    fng_b0, fng_b1, fng_b2, fng_b3, fng_b4, fng_b5, fng_b6, fng_week, fng_month = get_fng()

    print()
    print('공포/탐욕 지수', '(' + datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + ')')
    print('일간:', fng_b6, '->', fng_b5, '->', fng_b4, '->',
          fng_b3, '->', fng_b2, '->', fng_b1, '->', fng_b0)
    print('주간:', f'{fng_week:.2f}')
    print('월간:', f'{fng_month:.2f}')
    print('')

    domi = get_coingecko_dominance()
    domi_alternative = get_alternative_btc_dominance()
    _, price = get_binance_btc('BTC')

    print(f'바낸 비트 가격: $' + format(price, ',.2f'))
    print(f'비트  도미넌스: {domi:.2f} (coingecko)')
    print(f'비트  도미넌스: {domi_alternative:.2f} (alternative)')



def exit_gracefully(signal, frame):
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit_gracefully)
    main(sys.argv)
