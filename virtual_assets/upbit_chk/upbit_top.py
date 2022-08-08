# -*- coding: utf-8 -*-

import time, sys, getopt
import pyupbit
from common.themes import get_themes, get_all_themes


def calc_earn(v):
    try:
        df = pyupbit.get_ohlcv(v, count=1)
        o = df['open'][0]
        c = df['close'][0]
        p = ((c / o) - 1.0) * 100.0

        return v[4:], o, c, p
    except:
        return None, None, None, None


def main(argv):
    lst = pyupbit.get_tickers(fiat="KRW")
    earns = [[]]
    theme_dict = {}
    theme_dict.clear()
    count = 50

    try:
        opts, etc_args = getopt.getopt(argv[1:], "hc:"
                                       , ["help", "count="])

    except getopt.GetoptError:
        print(argv[0], '-c <count>')
        print('ex) python', f'{argv[0]}', '-c 20  (default)')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('ex) python', f'{argv[0]}', '-c 20  (default)')
            sys.exit(2)
        elif opt in ("-c", "--count"):
            count = int(arg.strip())

    themes = get_all_themes()
    for t in themes:
        theme_dict[t] = 0

    earns.clear()

    for v in lst:
        time.sleep(0.1)
        arr = calc_earn(v)
        if arr is not None:
            earns.append(list(arr))

    earns = sorted(earns, key=lambda x : x[3], reverse=True)

    print(f'업비트 상위 {count} 개 종목이 속한 테마 ', time.strftime('%Y-%m-%d %H:%M:%S'))
    print()
    print('번호, 심볼, open, close, 실적, 테마')

    i = 0
    for e in earns:
        _, tms = get_themes(e[0])
        for t in tms:
            if not t.lower().startswith('unclassified'):
                theme_dict[t] += 1
        i += 1
        print(str(i)+',', f'{e[0]},', f'{e[1]},', f'{e[2]},', f'{e[3]:.2f}%, ', tms)
        if count <= i:
            break

    print()
    for key, val in theme_dict.items():
        if 0 < val :
            print( key+':', val)


if __name__ == "__main__":
    main(sys.argv)
