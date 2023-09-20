# -*- coding: utf-8 -*-

import requests
from ast import literal_eval
import numpy as np
import pandas as pd
import operator
from common.utils import market_code
import time, datetime, sys, getopt
import json
import argparse
import talib as ta
import pyupbit
# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


def get_ohlcv(ticker, interval='day'):
    if not ticker.startswith('KRW-') and not ticker.startswith('BTC-') and not ticker.startswith('USDT-'):
        ticker = 'KRW-' + ticker

    df = pyupbit.get_ohlcv(ticker, interval=interval)

    return df


def predict_direction(symbol, df):
  """
  ohlcv 값을 이용해 상승/하락을 예상합니다.

  Args:
    ohlcv: OHLCV 데이터프레임

  Returns:
    상승: 1, 하락: 0
  """

  # 이동평균선 계산
  close = df['close']
  ma_5 = close.rolling(5).mean()
  ma_20 = close.rolling(20).mean()

  # 현재가가 이동평균선 5를 상향 돌파했는지 확인
  if close[-1] > ma_5[-1] and ma_5[-1] > ma_20[-1]:
    return 1

  # 현재가가 이동평균선 5를 하향 돌파했는지 확인
  elif close[-1] < ma_5[-1] and ma_5[-1] < ma_20[-1]:
    return -1

  # 그 외의 경우
  else:
    return 0


def predict_dir_sk(symbol, df):
    # Load your OHLCV data into a DataFrame (replace 'data.csv' with your dataset)
    # data = pd.read_csv('data.csv')

    # Feature engineering - create additional features if needed
    # For example, you can calculate moving averages, RSI, MACD, etc.

    # Define your target variable, e.g., 1 for rise and 0 for fall
    df['Target'] = (df['close'] > df['open']).astype(int)

    # Split the data into training and testing sets
    X = df[['open', 'high', 'low', 'volume']]  # Features
    y = df['Target']  # Target variable
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a machine learning model (Random Forest in this example)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Make predictions
    predictions = model.predict(X_test)
    res = predict_direction(symbol, df)

    # Evaluate the model
    accuracy = accuracy_score(y_test, predictions)
    if 0 < predictions[0] and 65.0 <= accuracy * 100 and 0 < res:
        print(f'{symbol}\t{accuracy * 100:.2f}% {predictions[0]} {predictions[1]} {predictions[2]} {predictions[3]}')
    # Print the prediction
    # print(f'Tomorrow's prediction: {prediction[0]}')

def main(argv):
    parser = argparse.ArgumentParser(description='옵션 지정 방법')
    parser.add_argument('-i', '--interval', required=False, default='day',
                        help='candle 종류 (day, week, month, minute1, ...)')
    parser.add_argument('-s', '--symbol', required=False, default='all',
                        help='symbol (default:all)')

    args = parser.parse_args()
    interval = args.interval
    symbol = args.symbol

    if not symbol.lower().startswith('all'):
        df = get_ohlcv(symbol, interval)
        predict_direction(symbol, df)
    else:
        try:
            lst = pyupbit.get_tickers(fiat="KRW")
            lst.sort()

            ptn_score_list = []
            ptn_score_list.clear()

            for v in lst:
                time.sleep(0.1)
                df = get_ohlcv(v[4:], interval)
                predict_dir_sk(v[4:], df)
        except Exception as e:
            print(e)

        print('interval=', interval)

if __name__ == "__main__":
    main(sys.argv)

# py rsi.py --up=60 --down=35
