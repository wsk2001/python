import sys
from autots import AutoTS
import sqlite3
import pandas as pd
import argparse
import datetime


database_name = './dbms/virtual_asset.db'

def price_prediction(symbol, start_date):

    query = f"select date, open, high, low, close, volume from day_candle " \
            f"where symbol = '{symbol.upper()}' and " \
            f"date >= '{start_date}' order by Date;"

    con = sqlite3.connect(database_name)
    data = pd.read_sql_query(query, con)
    data["Date"] = pd.to_datetime(data.date)

    model = AutoTS(forecast_length=30, frequency='infer', ensemble='simple')
    model = model.fit(data, date_col='Date', value_col='close', id_col=None)
    prediction = model.predict()
    forecast = prediction.forecast

    con.close()

    return forecast


def main(argv):
    parser = argparse.ArgumentParser(description='옵션 지정 방법')
    parser.add_argument('--symbol', required=False, default=21, help='수집 data 갯수 (default=10000)')
    parser.add_argument('--start', required=False, default='2022-01-01', help='시작 일자 (yyyy-mm-dd)')

    args = parser.parse_args()
    symbol = args.symbol
    start = args.start

    start_dt = datetime.datetime.now()
    forecast = price_prediction(symbol, start)
    end_dt = datetime.datetime.now()
    print(forecast)
    print('symbol: ', symbol, ' start: ', start_dt, ' end: ', end_dt)



if __name__ == "__main__":
    main(sys.argv)

