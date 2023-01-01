# -*- coding: utf-8 -*-
'''
시계열 유사패턴 분석 App
실행 방법 : py time_series_patterns.py --symbol=심볼명.
'''
import matplotlib.pyplot as plt
import sqlite3
import pandas as pd
# 1차월 배열간 코사인 유사도 계산
from scipy.spatial.distance import cosine
import sys

import argparse

database_name = './dbms/virtual_asset.db'

def get_df(symbol):
    query = \
        "select date, close from day_candle WHERE date >= '2018-01-01' and symbol" + "= '" + symbol.upper() + "';"

    con = sqlite3.connect(database_name)
    df = pd.read_sql_query(query, con)

    con.close()

    return df

def predict(symbol, base, next):
    upbit_df = get_df(symbol.upper())
    upbit_df.index.name = 'date'
    upbit_df_close = upbit_df['close']
    #upbit_df_close[-16:-1].plot();

    count = 0
    compare_base_r = upbit_df_close[(base+1)*-1:-1]

    # series에서 값만 추출
    compare_base = compare_base_r.values
    # 표준화
    compare_base_norm = (compare_base - compare_base.mean()) / compare_base.std()
    # array -> 1차원 리스트로 변환
    compare_base_norm = list(compare_base_norm)

    # 검색 기간
    window_size = len(compare_base_norm)
    # 검색 기간에 더해서 추가로 보여줄 기간
    next_date = next
    # 검색 횟수
    moving_cnt = len(upbit_df_close) - (window_size-1) - next_date

    # 유사도 저장 딕셔너리
    sim_dict = {}

    for i in range(moving_cnt):
        compare_target_r = upbit_df_close[i:i+window_size]
        # series에서 값만 추출
        compare_target = compare_target_r.values
        # 표준화
        compare_target_norm = (compare_target - compare_target.mean()) / compare_target.std()
        # array -> 1차원 리스트로 변환
        compare_target_norm = list(compare_target_norm)

        # 코사인 유사도 저장
        sim = cosine(compare_base_norm, compare_target_norm)
        # 코사인 유사도 <- i(인덱스), 시계열데이터 함께 저장
        sim_dict[sim] = [i,compare_target_r]

    # 최소 코사인 유사도
    min_sim = min(list(sim_dict.keys()))
    # 최소 코사인 유사도가 나온 인덱스, 기간 추출
    sim_dict[min_sim]

    plt.plot(compare_base_norm, label='base')
    plt.plot(compare_target_norm, label='target')
    plt.legend()
    plt.show()


    # 반복문 인덱스 복원
    idx = sim_dict[min_sim][0]
    # 반복문 타겟 구간 시계열 데이터 복원
    compare_target_r = sim_dict[min_sim][1]

    plt.figure(figsize=(12, 4))
    expanded_target_r = upbit_df_close[idx:idx+window_size+next_date]
    expanded_target_r.plot()
    plt.axvspan(compare_target_r.index[-1], expanded_target_r.index[-1], facecolor='gray', alpha=0.5)
    plt.axvline(x=compare_target_r.index[-1], c='r', linestyle='--')
    plt.xticks(rotation=90)
    plt.title(symbol)
    plt.grid()
    plt.show()



def main(argv):
    parser = argparse.ArgumentParser(description='옵션 지정 방법')
    parser.add_argument('--symbol', required=False, default='BTC', help='symbol')
    parser.add_argument('--base', required=False, default=21, help='compare data range')
    parser.add_argument('--next', required=False, default=7, help='predict date length')

    args = parser.parse_args()
    symbol = args.symbol
    base = int(args.base)
    next = int(args.next)

    predict(symbol, base, next)

if __name__ == "__main__":
    main(sys.argv)
