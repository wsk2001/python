import sys
import sqlite3
import argparse
import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression
from prophet import Prophet

import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense


database_name = './dbms/virtual_asset.db'

def select_data(symbol, start_date, end_date='9999-12-31'):

    query = f"select date, open, high, low, close, volume from day_candle " \
            f"where symbol = '{symbol.upper()}' and " \
            f"date >= '{start_date}' and " \
            f"date <= '{end_date}' and " \
            f"rsi is not null order by Date;"

    con = sqlite3.connect(database_name)
    df = pd.read_sql_query(query, con)

    con.close()

    return df

def prediction(ticker, df):
    # 데이터 전처리
    df.drop(["date"], axis=1, inplace=True)
    df.drop(["volume"], axis=1, inplace=True)

    df.fillna(method="ffill", inplace=True)
    df["close"] = df["close"] / df["close"].iloc[0]

    # 모델 설계
    model = Sequential()
    model.add(Dense(128, activation="relu", input_shape=(df.shape[1] - 1,)))
    model.add(Dense(1))

    # 모델 학습
    model.compile(loss="mse", optimizer="adam")
    model.fit(df.drop("close", axis=1).astype("float32"), df["close"], epochs=300)

    # 모델 평가
    score = model.evaluate(df.drop("close", axis=1), df["close"])
    print("MSE:", score)

    # 주가 예측
    predictions = model.predict(df.drop("close", axis=1).astype("float32"))
    mean = np.mean(predictions)
    variance = np.var(predictions, ddof=1)

    print("평균:", mean)
    print("분산:", variance)


# 전혀 예측 않됨.
def main(argv):
    parser = argparse.ArgumentParser(description='옵션 지정 방법')
    parser.add_argument('-t', '--ticker', required=False, default='BTC', help='ticker')
    parser.add_argument('-s', '--start', required=False, default='2000-01-01', help='start date (yyyy-mm-dd)')
    parser.add_argument('-e', '--end', required=False, default='9999-12-31', help='end date (yyyy-mm-dd)')

    args = parser.parse_args()
    ticker = args.ticker
    start = args.start
    end = args.end

    df = select_data(ticker, start, end)

    prediction(ticker, df)

if __name__ == "__main__":
    main(sys.argv)

