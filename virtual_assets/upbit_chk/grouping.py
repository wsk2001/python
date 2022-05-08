#-*- coding:utf-8 -*-

import time
from datetime import date, datetime, timedelta
import sys, getopt
import pyupbit
import traceback
from common.utils import market_code

def earning(lst, name_to_code, start_date, end_date, title, detail=None, ko=True):
    try:
        print()
        print(title, '코인 수익률')
        print()
        avg = 0.0
        i = 0
        total = 0.0
        for k in lst:
            if ko:
                t = name_to_code[k[0]]
            else:
                t = 'KRW-' + k[0]

            dfo = pyupbit.get_ohlcv(t, count=1, to=start_date, period=0.1)
            dfc = pyupbit.get_ohlcv(t, count=1, to=end_date, period=0.1)
            # df = pyupbit.get_ohlcv(t, count=1, period=0.1)

            if dfo is None:
                continue

            so = dfo['open'][0]
            ec = dfc['close'][0]
            rate = ((ec / so) - 1.0) * 100.0
            total += rate
            i += 1
            # print(t, f'earning: ', f'{rate:.2f}%', f'{so:.2f}', f'{ec:.2f}')
            if detail is not None:
                if ko:
                    print(t, ',', f'{rate:.2f}%,', f'{so},', f'{ec}')
                else:
                    print(t[4:], ',', f'{rate:.2f}%,', f'{so},', f'{ec}')

            time.sleep(0.5)

        avg = total / i
        print(title, 'earning: ', f'{avg:.2f}')

    except Exception as e:
        print(traceback.format_exc())
        pass

    print()

def make_lst(fname):
    path = './indexs/'
    lst = []

    file = open(path + fname, "r")
    lines = file.readlines()

    idx_name = None
    for l in lines:
        line = l.strip()
        if not line:
            continue

        if line.startswith("#") or line.startswith("//"):
            continue

        if len(line) <= 0:
            continue

        strings = line.split()

        if idx_name is None:
            idx_name = strings
            continue

        lst.append(strings)

    return idx_name, lst

def main(argv):
    detail = 'detail'
    all_flag = False

    tmp_day = date.today() - timedelta(days=9)
    start_date = tmp_day.strftime('%Y%m%d')
    tmp_day = date.today() + timedelta(days=1)
    end_date = tmp_day.strftime('%Y%m%d')
    code_list, name_to_code, code_to_name = market_code()

    try:
        opts, etc_args = getopt.getopt(argv[1:], "hs:e:i:a", ["help", "start=", "end=", "index="])

    except getopt.GetoptError:
        print(argv[0], '-s <start date (yyyymmdd)> -e <end date(yyyymmdd)>')
        print('ex: ', argv[0], '-s 20211001 -e 20211012 -i kimchi.txt')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(argv[0], '-s <start date (yyyymmdd)> -e <end date(yyyymmdd)>')
            print('ex: ', argv[0], '-s 20211001 -e 20211012 -i kimchi.txt')
            sys.exit()

        elif opt in ("-s", "--start"):
            start_date = arg

        elif opt in ("-e", "--end"):
            end_date = arg

        elif opt in ("-i", "--index"):
            file_name = arg

        elif opt in ("-a", "-all"):
            all_flag = True

    if not all_flag:
        title, ticker_list = make_lst(file_name)
        earning(ticker_list, name_to_code, start_date, end_date, title, detail,ko=True)
    else:
        title = "all"
        earning(code_list, name_to_code, start_date, end_date, title, detail, ko=False)

if __name__ == "__main__":
    main(sys.argv)
