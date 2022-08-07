#-*- coding:utf-8 -*-

import time, sys, signal
import requests
import json
from common.utils import get_binance_btc
from common.dominance import get_dominance, aoa_position
import ccxt, cbpro, datetime
from tradingview_ta import TA_Handler, Interval, Exchange
import io
from bs4 import BeautifulSoup

url = "https://api.alternative.me/fng/?limit="


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


def fear_day(bef):
    _bef = str(bef+1)
    _url = url + _bef
    res = requests.request("GET", _url)

    parsed = json.loads(res.text)
    data = parsed["data"]

    return data[bef]["value"]


def fear_yester():
    _url = url + "2"
    res = requests.request("GET", _url)

    parsed = json.loads(res.text)
    data = parsed["data"]

    return data[1]["value"]


def fear_twodaysago():
    _url = url + "3"
    res = requests.request("GET", _url)

    parsed = json.loads(res.text)
    data = parsed["data"]

    return data[2]["value"]


def fear_week():
    _url = url + "7"
    res = requests.request("GET", _url)

    parsed = json.loads(res.text)
    data = parsed["data"]

    sum = 0
    for index, value in enumerate(data):
        sum += int(value["value"])

    return sum / 7


def fear_month():
    _url = url + "30"
    res = requests.request("GET", _url)

    parsed = json.loads(res.text)
    data = parsed["data"]

    sum = 0
    for index, value in enumerate(data):
        sum += int(value["value"])

    return sum / 30


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


def main(argv):
    fng_today = fear_day(0)
    fng_yesterday = fear_day(1)
    fng_twodayago = fear_day(2)
    fng_threedayago = fear_day(3)
    fng_fourdayago = fear_day(4)
    fng_fivedayago = fear_day(5)
    fng_sixdayago = fear_day(6)

    fng_week = fear_week()
    fng_month = fear_month()
    print('공포/탐욕 지수', '(' + datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + ')')
    print('일간:', fng_sixdayago, '->', fng_fivedayago, '->', fng_fourdayago, '->',
          fng_threedayago, '->', fng_twodayago, '->', fng_yesterday, '->', fng_today)
    print('주간:', f'{fng_week:.2f}')
    print('월간:', f'{fng_month:.2f}')
    print('')

    _, _, _, domi = get_dominance()
    _, price = get_binance_btc('BTC')
    cb_p, bn_p, cb_idx, ti = cb_index(price)

    print(f'바낸 비트 가격: $' + format(price, ',.2f'))
    print(f'바낸 비트 도미: {domi:.3f}')
    print(aoa_position() + ' (bitsignal)')

    # print(f'코베 비트 가격: $' + format(cb_p, ',.2f'))
    # print(f'테더 가격     : ' + format(ti, ',.5f'))
    # print('')
    print('코인베이스 프리미엄 지수:', f'{cb_idx:.2f}')
    # print('  산출 방법: 코베 - (바낸 * 테더)')
    # print('')
    #
    # while True:
    #     _, price = get_binance_btc('BTC')
    #     cb_p, bn_p, cb_idx, ti = cb_index(price)
    #     print('Coinbase Premium Index:', f'{cb_idx:.2f}')
    #     time.sleep(5)


def exit_gracefully(signal, frame):
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit_gracefully)
    main(sys.argv)
