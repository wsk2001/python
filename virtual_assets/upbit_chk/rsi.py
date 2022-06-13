import requests
from ast import literal_eval
import numpy as np
import pandas as pd
import operator
from common.utils import market_code

import time, datetime, sys, getopt
import json

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

def RSI_analysis(code_list, code_to_name, time_unit, unit, target_up=70, target_down=30, option="multi"):

    start = time.time()

    if time_unit.upper().startswith('MINUTES'):
        url = "https://api.upbit.com/v1/candles/" + time_unit + "/" + str(unit)  # 1, 3, 5, 10, 15, 30, 60, 240
    elif time_unit.upper().startswith('DAYS'):
        url = "https://api.upbit.com/v1/candles/days"
    elif time_unit.upper().startswith('WEEKS'):
        url = "https://api.upbit.com/v1/candles/weeks"
    elif time_unit.upper().startswith('MONTHS'):
        url = "https://api.upbit.com/v1/candles/months"
    else:
        url = "https://api.upbit.com/v1/candles/days"

    coin_to_price = {}
    rsi_list = []
    rsi_number = 14
    sample = 200
    request_limit_per_second = -10
    request_count = 0
    request_time_list = np.array([])

    # 코인별 시간별 가격
    for i in range(len(code_list)):
        querystring = {"market": code_list[i], "count": str(sample)}  # 캔들 갯수
        if request_count < request_limit_per_second:  # max api 요청수, 분당 600, 초당 10회
            request_count += 1  # 요청수 1회 증가
        else:
            request_time_sum = np.sum(request_time_list[request_limit_per_second:])
            if request_time_sum >= 1:
                pass
            else:
                time.sleep(1 - request_time_sum)

        times = time.time()  # 요청 시작 시간
        response = requests.request("GET", url, params=querystring)
        request_time_list = np.append(request_time_list, time.time() - times)  # 요청 끝 시간
        r_str = response.text
        r_str = r_str.lstrip('[')  # 첫 문자 제거
        r_str = r_str.rstrip(']')  # 마지막 문 제거
        r_list = r_str.split("}")  # str를 }기준으로 쪼개어 리스트로 변환

        date_to_price = {}
        price_list = []

        for j in range(len(r_list) - 1):
            r_list[j] += "}"
            if j != 0:
                r_list[j] = r_list[j].lstrip(',')
            # r_dict = literal_eval(r_list[j])  # stinrg to dict
            r_dict = json.loads(r_list[j])  # stinrg to dict
            temp_dict = {r_dict["candle_date_time_kst"]: r_dict["trade_price"]}
            date_to_price.update(temp_dict)  # 시간-가격 매핑
            price_list.append(r_dict["trade_price"])  # 가격 리스트

        price_list.reverse()  # order : past -> now
        temp_dict = {code_list[i]: date_to_price}
        coin_to_price.update(temp_dict)  # 코인-시간-가격 매핑

        rsi_list.append(rsi_calculate(price_list, rsi_number, sample))  # RSI 계산

    target_dict = {}

    if option == "multi":

        for i in range(len(rsi_list)):
            if (target_down > rsi_list[i] >= 0) or i == 0:  # 비트코인 포함, rsi가 음수인 빈리스트 제외
                target_dict.update({code_to_name[code_list[i]]: rsi_list[i]})
                # target_dict.update({name_to_code[code_list[i]]: rsi_list[i]})
        if len(target_dict) <= 1:
            pass
        else:
            print("\n## RSI " + str(target_down) + "미만 " + time_unit + " " + str(unit))
            target_dict = sorted(target_dict.items(), key=operator.itemgetter(1))

            for i in target_dict:
                print(i[0], f'{i[1]:.2f}')

        target_dict = {}

        for i in range(len(rsi_list)):
            if (rsi_list[i] > target_up) or i == 0:
                target_dict.update({code_to_name[code_list[i]]: rsi_list[i]})
                # target_dict.update({name_to_code[code_list[i]]: rsi_list[i]})
        if len(target_dict) <= 1:
            pass
        else:
            print("\n## RSI " + str(target_up) + "이상 " + time_unit + " " + str(unit))

            target_dict = sorted(target_dict.items(), key=operator.itemgetter(1))
            for i in target_dict:
                print(i[0], f'{i[1]:.2f}')
            end = time.time()
            print("\nRunning time : ", end - start)
            print("현재시간 : " + time.strftime('%c', time.localtime(time.time())) + "\n")

    elif option == "up":

        for i in range(len(rsi_list)):
            if (rsi_list[i] > target_up) or i == 0:
                target_dict.update({code_to_name[code_list[i]]: rsi_list[i]})
                # target_dict.update({name_to_code[code_list[i]]: rsi_list[i]})
        if len(target_dict) <= 1:
            pass
        else:
            print("\n## RSI " + str(target_up) + "이상 " + time_unit + " " + str(unit))

            target_dict = sorted(target_dict.items(), key=operator.itemgetter(1))
            for i in target_dict:
                print(i[0], f'{i[1]:.2f}')
            end = time.time()
            print("\nRunning time : ", end - start)
            print("현재시간 : " + time.strftime('%c', time.localtime(time.time())) + "\n")
    else:
        for i in range(len(rsi_list)):
            if (target_down > rsi_list[i] >= 0) or i == 0:
                target_dict.update({code_to_name[code_list[i]]: rsi_list[i]})
                # target_dict.update({name_to_code[code_list[i]]: rsi_list[i]})
        if len(target_dict) <= 1:
            pass
        else:
            print("\n## RSI " + str(target_down) + "미만 " + time_unit + " " + str(unit))

            target_dict = sorted(target_dict.items(), key=operator.itemgetter(1))

            for i in target_dict:
                print(i[0], f'{i[1]:.3f}')
            end = time.time()
            print("\nRunning time : ", end - start)
            print("현재시간 : " + time.strftime('%c', time.localtime(time.time())) + "\n")


# Main function
def main(argv):

    rsi_up = 70
    rsi_bottom = 30
    unit = 1
    time_unit = "DAYS"

    try:
        opts, etc_args = getopt.getopt(argv[1:], "hdwm:u:b:"
                                       , ["help", "days", "weeks", "minutes=", "up=", "down="])

    except getopt.GetoptError:
        print(argv[0], '-m <minute> -u <rsi up level>  -b <rsi bottom level>')
        print('\t\t-d \t\t일자 기준 RSI')
        print('\t\t-w \t\t주 기준 RSI')
        print('ex) python', f'{argv[0]}', '-m 240 -u 70  -d 30')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(argv[0], '-m <minute> -u <rsi up level>  -b <rsi bottom level>')
            print('\t\t-d \t\t일자 기준 RSI')
            print('\t\t-w \t\t주 기준 RSI')
            print('ex) python', f'{argv[0]}', '-m 240 -u 70  -d 30')
            sys.exit()

        elif opt in ("-d", "--days"):  # ticker symbol
            time_unit = "DAYS"

        elif opt in ("-w", "--weeks"):  # ticker symbol
            time_unit = "WEEKS"

        elif opt in ("-m", "--minutes"):  # ticker symbol
            unit = int(arg.strip())
            time_unit = "MINUTES"

        elif opt in ("-u", "--up"):  # count
            rsi_up = int(arg.strip())

        elif opt in ("-b", "--bottom"):  # count
            rsi_bottom = int(arg.strip())

    print("Start\n")
    code_list, name_to_code, code_to_name = market_code()
    while 1:
        # 1, 3, 5, 10, 15, 30, 60, 240
        try:
            RSI_analysis(code_list, code_to_name, time_unit, unit, rsi_up, rsi_bottom)
        except Exception as e:
            print(e)
            exit(0)


if __name__ == "__main__":
    main(sys.argv)
