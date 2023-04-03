#-*- coding:utf-8 -*-

import requests
from ast import literal_eval
import requests
import json
import pyupbit


# 마켓코드조회
def market_code():
    url = "https://api.upbit.com/v1/market/all"
    querystring = {"isDetails": "false"}
    response = requests.request("GET", url, params=querystring)

    # 코인이름 - 마켓코드 매핑
    r_str = response.text
    r_str = r_str.lstrip('[')  # 첫 문자 제거
    r_str = r_str.rstrip(']')  # 마지막 문자 제거
    r_list = r_str.split("}")  # str를 }기준으로 쪼개어 리스트로 변환

    # name to code
    ntc = {}
    # code to name
    ctn = {}
    # code list
    cl = []

    for i in range(len(r_list) - 1):
        r_list[i] += "}"
        if i != 0:
            r_list[i] = r_list[i].lstrip(',')
        r_dict = literal_eval(r_list[i])  # element to dict
        if r_dict["market"][0] == 'K':  # 원화거래 상품만 추출
            temp_dict = {r_dict["market"]: r_dict["korean_name"]}
            ctn.update(temp_dict)  # 코드 - 코인이름 매핑
            temp_dict = {r_dict["korean_name"]: r_dict["market"]}
            ntc.update(temp_dict)  # 코인이름 - 코드 매핑
            cl.append(r_dict["market"])  # 코드 리스트
    return cl, ntc, ctn

# 마켓코드조회
def market_code_all():
    url = "https://api.upbit.com/v1/market/all"
    querystring = {"isDetails": "false"}
    response = requests.request("GET", url, params=querystring)

    # 코인이름 - 마켓코드 매핑
    r_str = response.text
    r_str = r_str.lstrip('[')  # 첫 문자 제거
    r_str = r_str.rstrip(']')  # 마지막 문자 제거
    r_list = r_str.split("}")  # str를 }기준으로 쪼개어 리스트로 변환

    # name to code
    ntc = {}
    # code to name
    ctn = {}
    # code list
    cl = []

    for i in range(len(r_list) - 1):
        r_list[i] += "}"
        if i != 0:
            r_list[i] = r_list[i].lstrip(',')
        r_dict = literal_eval(r_list[i])  # element to dict
        temp_dict = {r_dict["market"]: r_dict["korean_name"]}
        ctn.update(temp_dict)  # 코드 - 코인이름 매핑

    return ctn


def get_binance_btc(t):
    ep = 'https://api.binance.com'
    ping = '/api/v1/ping'
    ticker24h = '/api/v1/ticker/24hr'

    params = {'symbol': t + 'USDT'}
    # r1 = requests.get(ep + ping)
    r2 = requests.get(ep + ticker24h, params=params)

    return float(r2.json()['openPrice']), float(r2.json()['lastPrice'])


def get_fng():
    url = 'https://api.alternative.me/fng/'
    r1 = requests.get(url)
    return int(r1.json()['data'][0]['value'])


# 환률 정보 조회
def upbit_get_usd_krw():
    url = 'https://quotation-api-cdn.dunamu.com/v1/forex/recent?codes=FRX.KRWUSD'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    exchange = requests.get(url, headers=headers).json()
    return exchange[0]['basePrice']


def get_interval(k):
    interval_dic = {'d': 'day',
                    'w': 'week',
                    'm': 'month',
                    'm1': 'minute1',
                    'm3': 'minute3',
                    'm5': 'minute5',
                    'm10': 'minute10',
                    'm15': 'minute15',
                    'm30': 'minute30',
                    'm60': 'minute60',
                    'm240': 'minute240'}
    return interval_dic[k]


def get_profit(open_price, close_price):
    return ((close_price / open_price) - 1.0) * 100.0


# 지정된 심볼의 ohlcv 를 가져 온다.
# dfs 는 기존에 취득 했던 data 를 다시 분석 할때 재 사용 한다.
def get_idx_values(symbol, cnt=10000, interval='day', dfs=None):
    if dfs is None:
        ticker = symbol
        if not ticker.upper().startswith('KRW-'):
            ticker = 'KRW-' + symbol.upper()

        df = pyupbit.get_ohlcv(ticker, count=cnt, interval=interval, period=1)
    else:
        df = dfs

    values = df.values.tolist()
    idx = df.index.tolist()

    return idx, values, df

# 명목화폐 (KRW, BTC, USDT) 기준 모든 종목명을 리스트로 돌려준다.
def get_tickers(fiat='KRW'):
    lst = pyupbit.get_tickers(fiat=fiat)
    lst.sort()

    return lst


if __name__ == "__main__":
    code_list, name_to_code, code_to_name = market_code()

    for code in code_list:
        print(code)

    for key in name_to_code:
        print(key, name_to_code[key])

    for key in code_to_name:
        print(key, code_to_name[key])

    fng = get_fng()
    print('Fear and Greed Index: ', fng)

