# -*- coding: utf-8 -*-

import requests
from ast import literal_eval


# 마켓코드조회 krw
from pytz import unicode


def market_code(classify):
    url = "https://api.upbit.com/v1/market/all"
    querystring = {"isDetails": "false"}
    response = requests.request("GET", url, params=querystring)

    # 코인이름 - 마켓코드 매핑
    r_str = response.text
    r_str = r_str.lstrip('[')  # 첫 문자 제거
    r_str = r_str.rstrip(']')  # 마지막 문자 제거
    r_list = r_str.split("}")  # str를 }기준으로 쪼개어 리스트로 변환

    name_to_symbol = {}
    symbol_to_name = {}
    symbol_list = []

    for i in range(len(r_list) - 1):
        r_list[i] += "}"

        if i != 0:
            r_list[i] = r_list[i].lstrip(',')

        r_dict = literal_eval(r_list[i])  # element to dict

        if r_dict["market"].startswith(classify.upper()):  # 원하는 마켓 상품만 추출
            name_dict = {r_dict["market"]: r_dict["korean_name"]}
            code_dict = {r_dict["korean_name"]: r_dict["market"]}
            symbol_list.append(r_dict["market"])  # 코드 리스트
            name_to_symbol.update(name_dict)  # 코인이름 - 코드 매핑(딕셔너리)
            symbol_to_name.update(code_dict)  # 코드 - 코인이름 매핑(딕셔너리)

    return symbol_list, name_to_symbol, symbol_to_name


# 미완 테스트중
def get_name_to_symbol(kor, name_to_symbol):
    rtn_value = None
    try:
        rtn_value = name_to_symbol[kor]
    except:
        rtn_value = None
        print(kor, 'get_name_to_symbol')
        return rtn_value
    else:
        return rtn_value


# 미완 테스트중
def get_symbol_to_name(symbol, symbol_to_name):
    rtn_value = None
    try:
        rtn_value = symbol_to_name[symbol]
    except:
        rtn_value = None
        return rtn_value
    else:
        return rtn_value


if __name__ == "__main__":
    krw_symbol_list, krw_name_to_symbol, krw_symbol_to_name = market_code('KRW')
    btc_symbol_list, btc_name_to_symbol, btc_symbol_to_name = market_code('BTC')
    usdt_symbol_list, usdt_name_to_symbol, usdt_symbol_to_name = market_code('USDT')

    # print('symbol_list', btc_symbol_list)
    # print('')
    #
    # for key, value in btc_name_to_symbol.items():
    #     print(key, value)
    # print('')
    #
    # for key, value in btc_symbol_to_name.items():
    #     print(key, value)
    # print('--------------------')

    file = open('market_value.txt', "r",  encoding='euc-kr')
    lines = file.readlines()
    # lines = lines.encode('utf-8')


    con_str = ''
    j = 0
    for l in lines:
        line = l.strip()
        if not line:
            continue

        if line.startswith("#") or line.startswith("//"):
            continue

        if len(line) <= 0:
            continue

        strings = line.strip()
        strs = strings.split()
        if 1 < len(strs):
            i = 0
            for s in strs:
                if i < 1:
                    if i != 2 :
                        con_str = con_str + ', ' + s
                i += 1
        else:
            if j != 1:
                if j == 0 :
                    con_str = con_str + ' ' + strings
                else:
                    con_str = con_str + ', ' + strings

        j += 1

        if 4 <= j:
            print(con_str.strip())
            j = 0
            con_str = ''
