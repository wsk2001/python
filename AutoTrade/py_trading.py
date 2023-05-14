import pandas as pd
import numpy as np
import talib

def volatility_breakout_trading(df, symbol, window_size=14):
  """
  변동성 돌파 전략을 구현합니다.

  Args:
    df: 데이터 프레임.
    symbol: 기호.
    window_size: 변동성을 계산하기 위한 창 크기.

  Returns:
    매수 및 매도 신호의 리스트.
  """

  # 변동성을 계산합니다.
  volatility = talib.STDDEV(df['Close'], window_size)

  # 매수 및 매도 신호를 생성합니다.
  signals = []
  for i in range(len(df) - window_size):
    # 가격이 변동성 상단을 돌파하면 매수합니다.
    if df['Close'][i + window_size] > df['Close'][i] + volatility[i + window_size]:
      signals.append({
        'symbol': symbol,
        'type': 'buy',
        'price': df['Close'][i + window_size]
      })
    # 가격이 변동성 하단을 돌파하면 매도합니다.
    elif df['Close'][i + window_size] < df['Close'][i] - volatility[i + window_size]:
      signals.append({
        'symbol': symbol,
        'type': 'sell',
        'price': df['Close'][i + window_size]
      })

  return signals

def backtest_volatility_breakout_strategy(df, symbol, window_size=14):
  """
  변동성 돌파 전략의 백테스트를 수행합니다.

  Args:
    df: 데이터 프레임.
    symbol: 기호.
    window_size: 변동성을 계산하기 위한 창 크기.

  Returns:
    백테스트 결과.
  """

  # 매수 및 매도 신호를 생성합니다.
  signals = volatility_breakout_trading(df, symbol, window_size)

  # 백테스트 결과를 계산합니다.
  returns = []
  for signal in signals:
    if signal['type'] == 'buy':
      returns.append((df['Close'][signal['price']] - df['Close'][signal['price'] - 1]) / df['Close'][signal['price'] - 1])
    elif signal['type'] == 'sell':
      returns.append((df['Close'][signal['price'] - 1] - df['Close'][signal['price']]) / df['Close'][signal['price']])

  return returns


returns = backtest_volatility_breakout_strategy(df, 'BTC/USD', window_size=14)


import pandas as pd
import numpy as np
import talib

def bollinger_bands_trading(df, symbol, window_size=20, num_stds=2):
  """
  볼린저 밴드 전략을 구현합니다.

  Args:
    df: 데이터 프레임.
    symbol: 기호.
    window_size: 이동 평균을 계산하기 위한 창 크기.
    num_stds: 표준 편차의 수.

  Returns:
    매수 및 매도 신호의 리스트.
  """

  # 이동 평균을 계산합니다.
  ma = talib.MA(df['Close'], window_size)

  # 상단 및 하단 밴드를 계산합니다.
  upper_band = ma + num_stds * talib.STDDEV(df['Close'], window_size)
  lower_band = ma - num_stds * talib.STDDEV(df['Close'], window_size)

  # 매수 및 매도 신호를 생성합니다.
  signals = []
  for i in range(len(df) - window_size):
    # 가격이 상단 밴드를 돌파하면 매수합니다.
    if df['Close'][i + window_size] > upper_band[i + window_size]:
      signals.append({
        'symbol': symbol,
        'type': 'buy',
        'price': df['Close'][i + window_size]
      })
    # 가격이 하단 밴드를 돌파하면 매도합니다.
    elif df['Close'][i + window_size] < lower_band[i + window_size]:
      signals.append({
        'symbol': symbol,
        'type': 'sell',
        'price': df['Close'][i + window_size]
      })

  return signals

def backtest_bollinger_bands_strategy(df, symbol, window_size=20, num_stds=2):
  """
  볼린저 밴드 전략의 백테스트를 수행합니다.

  Args:
    df: 데이터 프레임.
    symbol: 기호.
    window_size: 이동 평균을 계산하기 위한 창 크기.
    num_stds: 표준 편차의 수.

  Returns:
    백테스트 결과.
  """

  # 매수 및 매도 신호를 생성합니다.
  signals = bollinger_bands_trading(df, symbol, window_size, num_stds)

  # 백테스트 결과를 계산합니다.
  returns = []
  for signal in signals:
    if signal['type'] == 'buy':
      returns.append((df['Close'][signal['price']] - df['Close'][signal['price'] - 1]) / df['Close'][signal['price'] - 1])
    elif signal['type'] == 'sell':
      returns.append((df['Close'][signal['price'] - 1] - df['Close'][signal['price']]) / df['Close'][signal['price']])

  return returns


returns = backtest_bollinger_bands_strategy(df, 'BTC/USD', window_size=20, num_stds=2)



import pandas as pd
import numpy as np
import talib

def rsi_trading(df, symbol, window_size=14):
  """
  RSI 전략을 구현합니다.

  Args:
    df: 데이터 프레임.
    symbol: 기호.
    window_size: RSI를 계산하기 위한 창 크기.

  Returns:
    매수 및 매도 신호의 리스트.
  """

  # RSI를 계산합니다.
  rsi = talib.RSI(df['Close'], window_size)

  # 매수 및 매도 신호를 생성합니다.
  signals = []
  for i in range(len(df) - window_size):
    # RSI가 30 미만이면 매수합니다.
    if rsi[i + window_size] < 30:
      signals.append({
        'symbol': symbol,
        'type': 'buy',
        'price': df['Close'][i + window_size]
      })
    # RSI가 70 이상이면 매도합니다.
    elif rsi[i + window_size] > 70:
      signals.append({
        'symbol': symbol,
        'type': 'sell',
        'price': df['Close'][i + window_size]
      })

  return signals

def backtest_rsi_strategy(df, symbol, window_size=14):
  """
  RSI 전략의 백테스트를 수행합니다.

  Args:
    df: 데이터 프레임.
    symbol: 기호.
    window_size: RSI를 계산하기 위한 창 크기.

  Returns:
    백테스트 결과.
  """

  # 매수 및 매도 신호를 생성합니다.
  signals = rsi_trading(df, symbol, window_size)

  # 백테스트 결과를 계산합니다.
  returns = []
  for signal in signals:
    if signal['type'] == 'buy':
      returns.append((df['Close'][signal['price']] - df['Close'][signal['price'] - 1]) / df['Close'][signal['price'] - 1])
    elif signal['type'] == 'sell':
      returns.append((df['Close'][signal['price'] - 1] - df['Close'][signal['price']]) / df['Close'][signal['price']])

  return returns


returns = backtest_rsi_strategy(df, 'BTC/USD', window_size=14)


import pandas as pd
import numpy as np
import talib

def macd_trading(df, symbol, window_size_fast=12, window_size_slow=26, window_size_signal=9):
  """
  MACD 전략을 구현합니다.

  Args:
    df: 데이터 프레임.
    symbol: 기호.
    window_size_fast: 빠른 이동 평균을 계산하기 위한 창 크기.
    window_size_slow: 느린 이동 평균을 계산하기 위한 창 크기.
    window_size_signal: 신호선을 계산하기 위한 창 크기.

  Returns:
    매수 및 매도 신호의 리스트.
  """

  # 빠른 이동 평균을 계산합니다.
  macd_fast = talib.MACD(df['Close'], window_size_fast, window_size_slow, window_size_signal)

  # 매수 및 매도 신호를 생성합니다.
  signals = []
  for i in range(len(df) - window_size_fast - window_size_slow - window_size_signal):
    # MACD 선이 신호선 위로 올라가면 매수합니다.
    if macd_fast[i + window_size_fast + window_size_slow] > macd_slow[i + window_size_fast + window_size_slow]:
      signals.append({
        'symbol': symbol,
        'type': 'buy',
        'price': df['Close'][i + window_size_fast + window_size_slow]
      })
    # MACD 선이 신호선 아래로 내려가면 매도합니다.
    elif macd_fast[i + window_size_fast + window_size_slow] < macd_slow[i + window_size_fast + window_size_slow]:
      signals.append({
        'symbol': symbol,
        'type': 'sell',
        'price': df['Close'][i + window_size_fast + window_size_slow]
      })

  return signals

def backtest_macd_strategy(df, symbol, window_size_fast=12, window_size_slow=26, window_size_signal=9):
  """
  MACD 전략의 백테스트를 수행합니다.

  Args:
    df: 데이터 프레임.
    symbol: 기호.
    window_size_fast: 빠른 이동 평균을 계산하기 위한 창 크기.
    window_size_slow: 느린 이동 평균을 계산하기 위한 창 크기.
    window_size_signal: 신호선을 계산하기 위한 창 크기.

  Returns:
    백테스트 결과.
  """

  # 매수 및 매도 신호를 생성합니다.
  signals = macd_trading(df, symbol, window_size_fast, window_size_slow, window_size_signal)

  # 백테스트 결과를 계산합니다.
  returns = []
  for signal in signals:
    if signal['type'] == 'buy':
      returns.append((df['Close'][signal['price']] - df['Close'][signal['price'] - 1]) / df['Close'][signal['price'] - 1])
    elif signal['type'] == 'sell':
      returns.append((df['Close'][signal['price'] - 1] - df['Close'][signal['price']]) / df['Close'][signal['price']])

  return returns


returns = backtest_macd_strategy(df, 'BTC/USD', window_size_fast=12, window_size_slow=26, window_size_signal=9)


import pandas as pd
import numpy as np
import talib

def stochastic_oscillator_trading(df, symbol, window_size=14, k=3):
  """
  스토캐스틱 오실레이터 전략을 구현합니다.

  Args:
    df: 데이터 프레임.
    symbol: 기호.
    window_size: 스토캐스틱 오실레이터를 계산하기 위한 창 크기.
    k: K값.

  Returns:
    매수 및 매도 신호의 리스트.
  """

  # 스토캐스틱 오실레이터를 계산합니다.
  stoch = talib.STOCH(df['High'], df['Low'], df['Close'], window_size=window_size, k=k)

  # 매수 및 매도 신호를 생성합니다.
  signals = []
  for i in range(len(df) - window_size):
    # 스토캐스틱 오실레이터가 80 이상이면 매도합니다.
    if stoch[i + window_size][2] > 80:
      signals.append({
        'symbol': symbol,
        'type': 'sell',
        'price': df['Close'][i + window_size]
      })
    # 스토캐스틱 오실레이터가 20 미만이면 매수합니다.
    elif stoch[i + window_size][2] < 20:
      signals.append({
        'symbol': symbol,
        'type': 'buy',
        'price': df['Close'][i + window_size]
      })

  return signals

def backtest_stochastic_oscillator_strategy(df, symbol, window_size=14, k=3):
  """
  스토캐스틱 오실레이터 전략의 백테스트를 수행합니다.

  Args:
    df: 데이터 프레임.
    symbol: 기호.
    window_size: 스토캐스틱 오실레이터를 계산하기 위한 창 크기.
    k: K값.

  Returns:
    백테스트 결과.
  """

  # 매수 및 매도 신호를 생성합니다.
  signals = stochastic_oscillator_trading(df, symbol, window_size, k)

  # 백테스트 결과를 계산합니다.
  returns = []
  for signal in signals:
    if signal['type'] == 'buy':
      returns.append((df['Close'][signal['price']] - df['Close'][signal['price'] - 1]) / df['Close'][signal['price'] - 1])
    elif signal['type'] == 'sell':
      returns.append((df['Close'][signal['price'] - 1] - df['Close'][signal['price']]) / df['Close'][signal['price']])

  return returns


returns = backtest_stochastic_oscillator_strategy(df, 'BTC/USD', window_size=14, k=3)


import pandas as pd
import numpy as np
import talib

def support_resistance_trading(df, symbol, window_size=14):
  """
  지지선 및 저항선 전략을 구현합니다.

  Args:
    df: 데이터 프레임.
    symbol: 기호.
    window_size: 지지선과 저항선을 계산하기 위한 창 크기.

  Returns:
    매수 및 매도 신호의 리스트.
  """

  # 이동 평균을 계산합니다.
  ma = talib.MA(df['Close'], window_size)

  # 지지선과 저항선을 계산합니다.
  support = df['Close'] - (ma - df['Close']).rolling(window_size).min()
  resistance = df['Close'] + (df['Close'] - ma).rolling(window_size).max()

  # 매수 및 매도 신호를 생성합니다.
  signals = []
  for i in range(len(df) - window_size):
    # 가격이 지지선을 돌파하면 매수합니다.
    if df['Close'][i + window_size] > support[i + window_size]:
      signals.append({
        'symbol': symbol,
        'type': 'buy',
        'price': df['Close'][i + window_size]
      })
    # 가격이 저항선을 돌파하면 매도합니다.
    elif df['Close'][i + window_size] < resistance[i + window_size]:
      signals.append({
        'symbol': symbol,
        'type': 'sell',
        'price': df['Close'][i + window_size]
      })

  return signals

def backtest_support_resistance_strategy(df, symbol, window_size=14):
  """
  지지선 및 저항선 전략의 백테스트를 수행합니다.

  Args:
    df: 데이터 프레임.
    symbol: 기호.
    window_size: 지지선과 저항선을 계산하기 위한 창 크기.

  Returns:
    백테스트 결과.
  """

  # 매수 및 매도 신호를 생성합니다.
  signals = support_resistance_trading(df, symbol, window_size)

  # 백테스트 결과를 계산합니다.
  returns = []
  for signal in signals:
    if signal['type'] == 'buy':
      returns.append((df['Close'][signal['price']] - df['Close'][signal['price'] - 1]) / df['Close'][signal['price'] - 1])
    elif signal['type'] == 'sell':
      returns.append((df['Close'][signal['price'] - 1] - df['Close'][signal['price']]) / df['Close'][signal['price']])

  return returns

returns = backtest_support_resistance_strategy(df, 'BTC/USD', window_size=14)

# 백테스트는 바드가 작성 하지 못한다고 답변함.


import pandas as pd
import numpy as np
import talib

def momentum_trading(df, symbol, window_size=14):
  """
  모멘텀 전략을 구현합니다.

  Args:
    df: 데이터 프레임.
    symbol: 기호.
    window_size: 모멘텀을 계산하기 위한 창 크기.

  Returns:
    매수 및 매도 신호의 리스트.
  """

  # 모멘텀을 계산합니다.
  momentum = df['Close'].rolling(window_size).pct_change()

  # 매수 및 매도 신호를 생성합니다.
  signals = []
  for i in range(len(df) - window_size):
    # 모멘텀이 양수이면 매수합니다.
    if momentum[i + window_size] > 0:
      signals.append({
        'symbol': symbol,
        'type': 'buy',
        'price': df['Close'][i + window_size]
      })
    # 모멘텀이 음수이면 매도합니다.
    elif momentum[i + window_size] < 0:
      signals.append({
        'symbol': symbol,
        'type': 'sell',
        'price': df['Close'][i + window_size]
      })

  return signals

def backtest_momentum_strategy(df, symbol, window_size=14):
  """
  모멘텀 전략의 백테스트를 수행합니다.

  Args:
    df: 데이터 프레임.
    symbol: 기호.
    window_size: 모멘텀을 계산하기 위한 창 크기.

  Returns:
    백테스트 결과.
  """

  # 매수 및 매도 신호를 생성합니다.
  signals = momentum_trading(df, symbol, window_size)

  # 백테스트 결과를 계산합니다.
  returns = []
  for signal in signals:
    if signal['type'] == 'buy':
      returns.append((df['Close'][signal['price']] - df['Close'][signal['price'] - 1]) / df['Close'][signal['price'] - 1])
    elif signal['type'] == 'sell':
      returns.append((df['Close'][signal['price'] - 1] - df['Close'][signal['price']]) / df['Close'][signal['price']])

  return returns


returns = backtest_momentum_strategy(df, 'BTC/USD', window_size=14)

