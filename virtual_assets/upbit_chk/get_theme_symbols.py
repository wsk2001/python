# -*- coding: utf-8 -*-

"""
코인 포지션이 전환되는 일자와 등락%의 평균값을 구하는 App
업비트 원화마켓 의 모든 코인이 기준입니다.
"""

import time, sys, getopt
import pyupbit
from datetime import datetime
from common.themes import get_theme_symbols


def main(argv):
    theme = 'did'
    try:
        opts, etc_args = getopt.getopt(argv[1:], "ht:"
                                       , ["help", "theme"])

    except getopt.GetoptError:
        print(argv[0], '-t <theme>')
        print('ex) python', f'{argv[0]}', '-t web3')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(argv[0], '-t <theme>')
            print('ex) python', f'{argv[0]}', '-t web3')
            sys.exit(2)

        elif opt in ("-t", "--theme"):
            theme = arg

    symbols = get_theme_symbols(theme)

    for key, val in symbols.items():
        print(f'{key}, {val}')


if __name__ == "__main__":
    main(sys.argv)
