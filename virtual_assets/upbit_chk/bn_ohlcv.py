import ccxt
from datetime import datetime
import pandas as pd

timeframes = (
    "1m", "3m", "5m", "15m", "30m",
    "1h", "2h", "4h", "6h", "8h", "12h",
    "1d", "3d",
    "1w",
    "1M",
)

binance = ccxt.binance()
offset_ko = (9*60*60*1000)

to = datetime.now()
to = to.strftime("%Y-%m-%d %H:%M:%S")
print(to)

symbol = 'BTC'
since = "2022-06-28"
since = int(pd.to_datetime(since).timestamp() * 1000)
#since = int(pd.to_datetime(to[:10]).timestamp() * 1000)
ohlcvs = binance.fetch_ohlcv(symbol + 'USDT', since=since, timeframe='1h', limit=25)

for t in ohlcvs:
    print(pd.to_datetime(t[0]+offset_ko, unit='ms'), t[1], t[2], t[3], t[4], t[5])
