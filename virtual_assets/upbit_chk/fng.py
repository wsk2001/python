#-*- coding:utf-8 -*-

import sys
import requests
import json
from common.utils import get_binance_btc
from common.dominance import get_dominance
import ccxt


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

def main(argv):
    fng_today = fear_day(0)
    fng_yesterday = fear_day(1)
    fng_twodayago = fear_day(2)
    fng_threedayday = fear_day(3)
    fng_fourdayday = fear_day(4)

    fng_week = fear_week()
    fng_month = fear_month()
    print('공포/탐욕 지수')
    print('일간:', fng_fourdayday, '->', fng_threedayday, '->', fng_twodayago, '->', fng_yesterday, '->', fng_today)
    print('주간:', f'{fng_week:.2f}')
    print('월간:', f'{fng_month:.2f}')
    print('')

    _, _, _, domi = get_dominance()
    _, price = get_binance_btc('BTC')

    print(f'비트코인 가격: $' + format(price, ',.2f'))
    print(f'비트코인 도미: {domi:.3f}')
    print('')

    # fr_binanc = funding_rate_binance()
    # print('바이낸스 펀딩비:', fr_binanc)
    # fr_bybit = funding_rate_bybit()
    # fr_bitmax = funding_rate_bitmex()
    # print('바이비트 펀딩비:', fr_bybit)
    # print('비트맥스 펀딩비:', fr_bitmax)


if __name__ == "__main__":
    main(sys.argv)
