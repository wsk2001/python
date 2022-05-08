import requests
from ast import literal_eval
import time
import numpy as np
import pandas as pd
import operator
import threading


# RSI계산 함수
def rsi_calculate(l, n, sample_number):  # l = price_list, n = rsi_number

    diff = []
    au = []
    ad = []

    if len(l) != sample_number:  # url call error
        return -1
    for i in range(len(l) - 1):
        diff.append(l[i + 1] - l[i])  # price difference

    au = pd.Series(diff)  # list to series
    ad = pd.Series(diff)

    au[au < 0] = 0  # remove ad
    ad[ad > 0] = 0  # remove au

    _gain = au.ewm(com=n, min_periods=sample_number - 1).mean()  # Exponentially weighted average
    _loss = ad.abs().ewm(com=n, min_periods=sample_number - 1).mean()
    RS = _gain / _loss

    rsi = 100 - (100 / (1 + RS.iloc[-1]))

    return rsi


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

    name_to_code = {}
    code_to_name = {}
    code_list = []

    for i in range(len(r_list) - 1):
        r_list[i] += "}"

        if i != 0:
            r_list[i] = r_list[i].lstrip(',')

        r_dict = literal_eval(r_list[i])  # element to dict

        if r_dict["market"][0] == 'K':  # 원화거래 상품만 추출
            name_dict = {r_dict["market"]: r_dict["korean_name"]}
            code_dict = {r_dict["korean_name"]: r_dict["market"]}
            code_list.append(r_dict["market"])  # 코드 리스트
            name_to_code.update(name_dict)  # 코인이름 - 코드 매핑(딕셔너리)
            code_to_name.update(code_dict)  # 코드 - 코인이름 매핑(딕셔너리)

    return code_list, name_to_code, code_to_name


# Main function

if __name__ == "__main__":
    code_list, name_to_code, code_to_name = market_code()
    print('code_list', code_list)
    print('')
    # print('name_to_code', name_to_code)

    for key, value in name_to_code.items():
        print(key, value)
    print('')

    for key, value in code_to_name.items():
        print(key)
    print('')
