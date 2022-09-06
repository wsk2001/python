# -*- coding: utf-8 -*-

import time, sys, getopt
import pyupbit
from common.themes import get_themes, get_all_themes, get_theme_symbols_count


def calc_earn(v):
    try:
        df = pyupbit.get_ohlcv(v, count=1)
        o = df['open'][0]
        c = df['close'][0]
        p = ((c / o) - 1.0) * 100.0

        return v[4:], o, c, p
    except:
        return None, None, None, None


def usage(app):
    print(app, 'options -c <count>')
    print('options')
    print('\t-c, --count\t\tranking count')
    print('\t-d         \t\tdown ranking')
    print('\t-u         \t\tup ranking')
    print('ex) python', app, '-u -c 20')
    print('    python', app, '-d -c 30')
    sys.exit(2)


def main(argv):
    lst = pyupbit.get_tickers(fiat="KRW")
    earns = [[]]
    theme_dict = {}
    theme_dict.clear()
    count = 30

    # option: Up
    reverse_flag = True

    try:
        opts, etc_args = getopt.getopt(argv[1:], "hc:ud"
                                       , ["help", "count=", "up", "down"])

    except getopt.GetoptError:
        usage(argv[0])

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage(argv[0])
        elif opt in ("-c", "--count"):
            count = int(arg.strip())
        elif opt in ("-d", "--down"):
            reverse_flag = False
        elif opt in ("-u", "--up"):
            reverse_flag = True

    themes = get_all_themes()
    for t in themes:
        theme_dict[t] = 0

    earns.clear()

    for v in lst:
        time.sleep(0.2)
        arr = calc_earn(v)
        if arr is not None:
            earns.append(list(arr))

    earns = sorted(earns, key=lambda x: x[3], reverse=reverse_flag)

    if reverse_flag:
        print(f'업비트 금일 상승률 상위 {count} 개 종목이 속한 테마 ')
    else:
        print(f'업비트 금일 하락률 하위 {count} 개 종목이 속한 테마 ')

    print(time.strftime('%Y-%m-%d %H:%M:%S'))
    print()
    print('순위, 심볼, open, close, 실적, [테마]')

    i = 0
    for e in earns:
        _, tms = get_themes(e[0])
        for t in tms:
            if not t.lower().startswith('unclassified'):
                theme_dict[t] += 1
        i += 1
        tms_u = [x.upper() for x in tms]
        print(str(i)+',', f'{e[0]},', f'{e[1]},', f'{e[2]},', f'{e[3]:.2f}%, ',tms_u)
        if count <= i:
            break

    print()
    for key, val in theme_dict.items():
        if 0 < val :
            per = val/get_theme_symbols_count(key) * 100
            print(f'{key.upper():<10}: {val}/{get_theme_symbols_count(key)} ({per:.2f}%)')


if __name__ == "__main__":
    main(sys.argv)
