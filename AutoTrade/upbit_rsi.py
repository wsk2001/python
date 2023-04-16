import pyupbit
import pandas as pd
import numpy as np

# 가격 데이터 가져오기
df = pyupbit.get_ohlcv("KRW-BTC", count=30, interval="minute60")

# RSI 계산을 위한 기간 설정
window_length = 14

# 종가와 종가의 변화량을 계산
close = df["close"]
delta = close.diff()

# 상승분과 하락분으로 나누어서 계산
gain = delta.where(delta > 0, 0)
loss = -delta.where(delta < 0, 0)

# 이동평균을 이용한 RSI 계산
avg_gain = gain.rolling(window_length).mean()
avg_loss = loss.rolling(window_length).mean().abs()
rs = avg_gain / avg_loss
rsi = 100.0 - (100.0 / (1.0 + rs))

print(rsi)
