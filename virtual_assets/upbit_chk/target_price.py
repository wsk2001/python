import calendar
import getopt
import sys, time
import pyupbit
from datetime import datetime
import argparse
import datetime
import numpy as np
import os

fee = 0.9995  # 거래 수수료 0.05%

# best_k 구하기_시작
def get_ror(ticker, k):
    df = pyupbit.get_ohlcv(ticker, "day", count=7)  # 7일간 일봉(count)
    df["range"] = (df["high"] - df["low"]) * k
    df["target"] = df["open"] + df["range"].shift(1)  # target = 매수가

    df["ror"] = np.where(
        df["high"] > df["target"], df["close"] / df["target"] - fee, 1
    )  # ror(수익율), np.where(조건문, 참일때 값, 거짓일때 값)

    ror = df["ror"].cumprod()[-2]
    return ror


# 변동성 돌파 전략 매수 목표가 추출_시작
def get_target_price(ticker, k):
    df = pyupbit.get_ohlcv(ticker, "day", count=2)
    target_price = df.iloc[0]["close"] + (df.iloc[0]["high"] - df.iloc[0]["low"]) * k
    return target_price


def get_best_k(ticker):
    ror1, next_ror, best_ror, best_k = 0.0, 0.0, 0.0, 0.1
    for k in np.arange(0.1, 1.0, 0.1):
        next_ror = get_ror(ticker, k)
        time.sleep(0.3)
        if ror1 < next_ror:  # k값중 최고 k 구하기
            if next_ror != 1:  # 수익률이 0% 가 아닐 때
                print(
                    "k : %.1f ror1 : %f  next_ror : %f"
                    % (k, ror1, next_ror),
                    "change",
                )
                ror1 = next_ror
                best_k = k
                best_ror = ror1
            else:
                print(
                    "k : %.1f ror1 : %f  next_ror : %f"
                    % (k, ror1, next_ror),
                    "No change_1",
                )
        else:
            print(
                "k : %.1f ror1 : %f  next_ror : %f" % (k, ror1, next_ror),
                "No change_2",
            )
    print("best_k : %.1f  best_ror : %f" % (best_k, best_ror))

    return best_k


def main(argv):
    parser = argparse.ArgumentParser(description='옵션 지정 방법')
    parser.add_argument('--symbol', required=False, default='btc', help='심볼 (BTC, ETH, ADA, ..., default=all)')

    args = parser.parse_args()
    symbol = args.symbol

    if not symbol.startswith('KRW-') and not symbol.startswith('BTC-') and not symbol.startswith('USDT-'):
        ticker = 'KRW-' + symbol
    else:
        ticker = symbol

    best_k = get_best_k(ticker)
    target_price = round(get_target_price(ticker, best_k), 0)
    print(ticker, 'Target price:', target_price)

if __name__ == "__main__":
    main(sys.argv)
