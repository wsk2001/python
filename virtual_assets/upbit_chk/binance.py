import json
from datetime import datetime, timedelta

import pandas as pd
import requests

timeframes = {
    "1m": ['1m', "1 mins", 300],
    "3m": ['1m', "3 mins", 300],
    "5m": ['5m', "5 mins", 300],
    "15m": ['15m', "15 mins", 300],
    "30m": ['30m', "30 mins", 300],
    "1h": ['1h', "1h", 3600],
    "2h": ['1h', "2h", 3600],
    "4h": ['1h', "4h", 3600],
    "6h": ['6h', "6h", 3600],
    "8h": ['1h', "8h", 3600],
    "12h": ['12h', "12h", 3600],
    "1d": ['1d', "1D", 1],
    "3d": ['1d', "3D", 3],
    "1w": ['1w', "7D", 7],
    "1M": ['1M', "30D", 30],
}

class Binance():
    def __init__(self, apiUrl="https://api.binance.com"):
        self.apiUrl = apiUrl

    @property
    def symbols(self) -> []:
        response = requests.get(f"{self.apiUrl}/api/v3/ticker/price", headers={"content-type": "application/json"})
        symbols = []
        for pair in response.json():
            symbols.append(pair["symbol"])
        return symbols

    def fetch_ohlcv(self, symbol, timeframe="2h", limit=300, from_date='2021-12-01 02:00:00.000000'):
        barSize = timeframes.get(timeframe)
        timeEnd = datetime.now()
        delta = timedelta(seconds=int(barSize[2]))
        if limit > 1000:
            # print("Overridden limit: Sorry maximum limit is 300")
            limit = 1000
        elif limit < 5:
            # print("Overridden limit: Sorry minimum limit is 1")
            limit = 5
        date_time_obj = datetime.strptime(from_date, '%Y-%m-%d %H:%M:%S.%f')
        frames = []
        while True:
            timeStart = timeEnd - (limit * delta)
            timeStart = timeStart

            parameters = {
                "symbol": symbol,
                "startTime": str(timeStart.timestamp()).replace(".", "")[:13],
                "interval": barSize[0],
                "limit": limit
            }

            data = requests.get(f"{self.apiUrl}/api/v3/klines", params=parameters)
            data_array = []
            for row in json.loads(data.content):
                data_array.append([row[0], float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5])])
            df = pd.DataFrame(data_array, columns=["time", "open", "high", "low", "close", "volume"])
            if limit < 5:
                frames.append(df.tail(1))
            else:
                frames.append(df)
            if date_time_obj.timestamp() > timeStart.timestamp() or limit < 50:
                break
            else:
                timeEnd = timeStart

        df = pd.concat(frames)
        df.drop_duplicates()
        df.reset_index(inplace=True)
        df["date"] = pd.to_datetime(df["time"], unit="ms")
        df.set_index("date", inplace=True)

        df = df.resample(barSize[1]).agg({
            "open": "first",
            "high": "max",
            "low": "min",
            "close": "last",
            "volume": "mean"
        })

        df.reset_index(inplace=True)

        df.dropna()
        df = df.loc[(df['date'] >= from_date)]
        df.reset_index(inplace=True)

        df = df.iloc[-limit:]
        df.reset_index(inplace=True)
        rows = []
        for index, row in df[["date", "low", "high", "open", "close", "volume"]].iterrows():
            rows.append([
                row["date"],
                row["open"],
                row["high"],
                row["low"],
                row["close"],
                row["volume"],
            ])
        return rows

    def fetch_ohlc(self, symbol, timeframe="2h", limit=300, from_date='2021-12-01 02:00:00.000000'):
        barSize = timeframes.get(timeframe)
        timeEnd = datetime.now()
        delta = timedelta(seconds=int(barSize[2]))
        if limit > 1000:
            # print("Overridden limit: Sorry maximum limit is 300")
            limit = 1000
        elif limit < 5:
            # print("Overridden limit: Sorry minimum limit is 1")
            limit = 5
        date_time_obj = datetime.strptime(from_date, '%Y-%m-%d %H:%M:%S.%f')
        frames = []
        while True:
            timeStart = timeEnd - (limit * delta)
            timeStart = timeStart

            parameters = {
                "symbol": symbol,
                "startTime": str(timeStart.timestamp()).replace(".", "")[:13],
                "interval": barSize[0],
                "limit": limit
            }

            data = requests.get(f"{self.apiUrl}/api/v3/klines", params=parameters)
            data_array = []
            for row in json.loads(data.content):
                data_array.append([row[0], float(row[1]), float(row[2]), float(row[3]), float(row[4])])
            df = pd.DataFrame(data_array, columns=["time", "open", "high", "low", "close"])
            if limit < 5:
                frames.append(df.tail(1))
            else:
                frames.append(df)
            if date_time_obj.timestamp() > timeStart.timestamp() or limit < 50:
                break
            else:
                timeEnd = timeStart

        df = pd.concat(frames)
        df.drop_duplicates()
        df.reset_index(inplace=True)
        df["date"] = pd.to_datetime(df["time"], unit="ms")
        df.set_index("date", inplace=True)

        df = df.resample(barSize[1]).agg({
            "open": "first",
            "high": "max",
            "low": "min",
            "close": "last"
        })

        df.reset_index(inplace=True)

        df.dropna()
        df = df.loc[(df['date'] >= from_date)]
        df.reset_index(inplace=True)

        df = df.iloc[-limit:]
        df.reset_index(inplace=True)
        rows = []
        for index, row in df[["date", "low", "high", "open", "close"]].iterrows():
            rows.append([
                row["date"],
                row["open"],
                row["high"],
                row["low"],
                row["close"],
            ])
        return rows

    def fetch_ticker(self, symbol) -> str:
        data = requests.get(f"{self.apiUrl}/api/v3/ticker/24hr?symbol={symbol}",
                            headers={"content-type": "application/json"})
        return data.json()



if __name__ == '__main__':
    binance = Binance()
    # print(binance.symbols)
    # print(binance.fetch_ticker("BTCUSDT"))
    # print(binance.fetch_ohlcv("BTCUSDT", limit=500))
    # print(binance.fetch_ohlc("BTCUSDT", timeframe="4h", limit=500))
    print(binance.fetch_ohlc("BTCUSDT", timeframe="4h", limit=30))
