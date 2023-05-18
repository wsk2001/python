import sys
import sqlite3
import argparse
import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression
from prophet import Prophet

database_name = './dbms/virtual_asset.db'

def select_data(symbol, start_date, end_date='9999-12-31'):

    query = f"select date, open, high, low, close, volume from day_candle " \
            f"where symbol = '{symbol.upper()}' and " \
            f"date >= '{start_date}' and " \
            f"date <= '{end_date}' order by Date;"

    con = sqlite3.connect(database_name)
    df = pd.read_sql_query(query, con)

    con.close()

    return df

def updown_prediction(ticker, df):
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

    print(f"{ticker.upper()} Next 5 days price prediction (Doesn't fit at all.)")
    for p in predictions:
        print(round(p, 2))

    # 예측을 시각화합니다.
    # plt.plot(df['close'])
    # plt.plot(predictions)
    # plt.show()


def ph_predict(df):
    df_train = df[['date', 'close']]
    df_train = df_train.rename(columns={"date": "ds", "close": "y"})
    m = Prophet()
    m.fit(df_train)

    future = m.make_future_dataframe(periods=7)
    forecast = m.predict(future)

    for f in forecast.tail(7):
        print(f)


# 전혀 예측 않됨.
def main(argv):
    parser = argparse.ArgumentParser(description='옵션 지정 방법')
    parser.add_argument('-t', '--ticker', required=False, default='BTC', help='ticker')
    parser.add_argument('-s', '--start', required=False, default='2023-01-01', help='start date (yyyy-mm-dd)')
    parser.add_argument('-e', '--end', required=False, default='9999-12-31', help='end date (yyyy-mm-dd)')

    args = parser.parse_args()
    ticker = args.ticker
    start = args.start
    end = args.end

    df = select_data(ticker, start, end)

    updown_prediction(ticker, df)

    ph_predict(df)

if __name__ == "__main__":
    main(sys.argv)

