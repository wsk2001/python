# -*- coding: utf-8 -*-

"""
코인 포지션이 전환되는 일자와 등락%의 평균값을 구하는 App
업비트 원화마켓 의 모든 코인이 기준입니다.
"""

import time, sys, getopt
import pyupbit
from datetime import datetime
from common.themes import get_theme_symbols, get_all_themes


def main(argv):
    themes = get_all_themes()

    for t in themes:
        symbols = get_theme_symbols(t)

        print(f'[{t.upper()}]')
        for key, val in symbols.items():
            print(f'{key}, {val}')

        print()


if __name__ == "__main__":
    main(sys.argv)
