import sys
from autots import AutoTS
import sqlite3
import pandas as pd
import argparse
import datetime
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import LSTM, Dense

database_name = './dbms/virtual_asset.db'

def price_prediction(symbol, start_date):

    query = f"select date, open, high, low, close, volume from day_candle " \
            f"where symbol = '{symbol.upper()}' and " \
            f"date >= '{start_date}' order by Date;"

    con = sqlite3.connect(database_name)
    df = pd.read_sql_query(query, con)

    con.close()

    return df

def main(argv):
    parser = argparse.ArgumentParser(description='옵션 지정 방법')
    parser.add_argument('--symbol', required=False, default=21, help='수집 data 갯수 (default=10000)')
    parser.add_argument('--start', required=False, default='2022-01-01', help='시작 일자 (yyyy-mm-dd)')

    args = parser.parse_args()
    symbol = args.symbol
    start = args.start

    start_dt = datetime.datetime.now()
    df = price_prediction(symbol, start)

    # 데이터 전처리
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(df['close'].values.reshape(-1, 1)) # 종가(Close) 데이터 스케일링
    window_size = 20  # 윈도우 사이즈 설정
    X = []
    y = []
    for i in range(len(scaled_data) - window_size):
        X.append(scaled_data[i : i + window_size, 0])
        y.append(scaled_data[i + window_size, 0])
    X, y = np.array(X), np.array(y)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))

    # 훈련 데이터와 테스트 데이터로 분할
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    # LSTM 모델 생성
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
    model.add(LSTM(units=50))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')

    # 모델 학습
    model.fit(X_train, y_train, epochs=100, batch_size=32)

    # 모델 평가
    train_loss = model.evaluate(X_train, y_train, batch_size=32)
    test_loss = model.evaluate(X_test, y_test, batch_size=32)
    print('Train Loss:', train_loss)
    print('Test Loss:', test_loss)

    # 모델을 활용한 예측
    predicted = model.predict(X_test)
    predicted = scaler.inverse_transform(predicted) # 스케일링된 데이터를 원본 스케일로 변환

    print(predicted)


if __name__ == "__main__":
    main(sys.argv)

