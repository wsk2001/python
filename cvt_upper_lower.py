import time
import datetime
import sys, getopt
import argparse


def main(argv):
    parser = argparse.ArgumentParser(description='옵션 지정 방법')
    parser.add_argument('--upper_case', required=False, default=None, help='대 문자로 변경')
    parser.add_argument('--lower_case', required=False, default=None, help='소 문자로 변경')

    args = parser.parse_args()
    upper_case = args.upper_case
    lower_case = args.lower_case

    if upper_case is not None:
        print(f'Upper case: {upper_case} -> {upper_case.upper()}')

    if lower_case is not None:
        print(f'Lower case: {lower_case} -> {lower_case.lower()}')


if __name__ == "__main__":
    main(sys.argv)

# 대 소문자 변경
# py cvt_upper_lower.py -h
