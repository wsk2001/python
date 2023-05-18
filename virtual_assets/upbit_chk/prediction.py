import sys
import sqlite3
import argparse
import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression

database_name = './dbms/virtual_asset.db'

def select_data(symbol, start_date):

    query = f"select date, open, high, low, close, volume from day_candle " \
            f"where symbol = '{symbol.upper()}' and " \
            f"date >= '{start_date}' order by Date;"

    con = sqlite3.connect(database_name)
    df = pd.read_sql_query(query, con)

    con.close()

    print(query)

    return df

def updown_prediction(df):
    # Dependent variable selection
    # 종가를 종속 변수로, 기타 모든 변수를 독립 변수로 하는 선형 회귀 모델을 만듭니다.
    model = LinearRegression()
    model.fit(df[['open', 'high', 'low', 'volume']], df['close'])

    # 모델을 저장합니다.
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)

    # 모델을 로드합니다.
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)

    # 모델을 사용하여 다음 5일의 가격을 예측합니다.
    predictions = model.predict(df[['open', 'high', 'low', 'volume']].tail(5))

    # 예측을 실제 가격과 비교합니다.
    # print(df[['close']].tail(5))

    print('Next 5 days')
    for p in predictions:
        print(round(p, 2))

    # 예측을 시각화합니다.
    # plt.plot(df['close'])
    # plt.plot(predictions)
    # plt.show()


def main(argv):
    parser = argparse.ArgumentParser(description='옵션 지정 방법')
    parser.add_argument('--symbol', required=False, default='BTC', help='수집 data 갯수 (default=10000)')
    parser.add_argument('--start', required=False, default='2023-01-01', help='시작 일자 (yyyy-mm-dd)')

    args = parser.parse_args()
    symbol = args.symbol
    start = args.start

    df = select_data(symbol, start)

    updown_prediction(df)


if __name__ == "__main__":
    main(sys.argv)

