import pyupbit
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Upbit API Key 및 Secret Key 입력
access_key = 'Input your access key here'
secret_key = 'Input your secret key here'

# Upbit 객체 생성
# upbit = pyupbit.Upbit(access_key, secret_key)

# 데이터 불러오기
df = pyupbit.get_ohlcv(ticker='KRW-BTC', interval='day', count=50)

# True Range(TR) 계산
df['TR'] = df[['high', 'low', 'close']].apply(lambda x: max(x) - min(x), axis=1)

# Average True Range(ATR) 계산
df['ATR'] = df['TR'].rolling(window=14).mean()

# 매매 기준값 계산
df['buy_signal'] = df['close'] > (df['close'].shift(1) + df['ATR'].shift(1))
df['sell_signal'] = df['close'] < (df['close'].shift(1) - df['ATR'].shift(1))

# 차트 그리기
fig = make_subplots(rows=2, cols=1, shared_xaxes=True)

fig.add_trace(
    go.Candlestick(x=df.index,
                   open=df['open'],
                   high=df['high'],
                   low=df['low'],
                   close=df['close'],
                   name='candlestick'),
    row=1, col=1
)

fig.add_trace(
    go.Scatter(x=df.index,
               y=df['ATR'],
               name='ATR'),
    row=2, col=1
)

fig.add_trace(
    go.Scatter(x=df[df['buy_signal']].index,
               y=df['close'][df['buy_signal']],
               mode='markers',
               marker=dict(color='green', size=10),
               name='Buy Signal'),
    row=1, col=1
)

fig.add_trace(
    go.Scatter(x=df[df['sell_signal']].index,
               y=df['close'][df['sell_signal']],
               mode='markers',
               marker=dict(color='red', size=10),
               name='Sell Signal'),
    row=1, col=1
)

fig.update_layout(title='업비트 비트코인 변동성 매매',
                  xaxis_rangeslider_visible=False,
                  height=600)

fig.show()
