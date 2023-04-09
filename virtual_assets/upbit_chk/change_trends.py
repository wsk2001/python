import calendar
import getopt
import sys, time
import pyupbit
from common.utils import market_code
from datetime import datetime
from common.utils import get_idx_values, get_tickers
import argparse

def change_trends(ticker, cnt, interval='minute5', view=None):
    if not ticker.startswith('KRW-') and not ticker.startswith('BTC-') and not ticker.startswith('USDT-'):
        ticker = 'KRW-' + ticker
    result = 0
    df = pyupbit.get_ohlcv(ticker, interval=interval, count=cnt+1, period=1)

    # 종가를 이용하여 수익률을 계산합니다.
    returns = df['close'].pct_change()

    # cnt 개 봉 기준으로 수익률의 평균값을 계산합니다.
    average_returns = returns.rolling(window=cnt).mean()

    # 평균 수익률이 0보다 크면 상승 추세, 작으면 하락 추세로 분류합니다.
    if average_returns.iloc[-1] > 0:
        if view is not None:
            print(ticker[4:].upper() + ' 상승 추세')
        result = 1
    else:
        if view is not None:
            print(ticker[4:].upper() + ' 하락 추세')
        result = -1
    return result

def main(argv):
    parser = argparse.ArgumentParser(description='옵션 지정 방법')
    parser.add_argument('--count', required=False, default=60, help='수집 data 갯수 (default=10000)')
    parser.add_argument('--interval', required=False, default='minute5', help='candle 종류 (day, week, month, minute1, ...)')
    parser.add_argument('--view', required=False, default='No', help='종목별 Display (Yes/No)')

    args = parser.parse_args()
    count = int(args.count)
    interval = args.interval
    view = args.view
    view = 'yes' if str(view).upper().startswith("YES") else None

    lst = get_tickers('KRW')
    up = 0
    down = 0
    for v in lst:
        res = change_trends(v.upper(), count, interval, view)
        if res == 1:
            up += 1
        elif res == -1:
            down += 1
        if view is None:
            print('.', end='')
            sys.stdout.flush()
        time.sleep(0.2)

    print()
    print("상승 추세: " + str(up) + ", 하락 추세: " + str(down))
    print()

if __name__ == "__main__":
    main(sys.argv)
