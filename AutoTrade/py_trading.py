import pandas as pd
import numpy as np
import talib

def volatility_breakout_trading(df, symbol, window_size=14):
  """
  ������ ���� ������ �����մϴ�.

  Args:
    df: ������ ������.
    symbol: ��ȣ.
    window_size: �������� ����ϱ� ���� â ũ��.

  Returns:
    �ż� �� �ŵ� ��ȣ�� ����Ʈ.
  """

  # �������� ����մϴ�.
  volatility = talib.STDDEV(df['Close'], window_size)

  # �ż� �� �ŵ� ��ȣ�� �����մϴ�.
  signals = []
  for i in range(len(df) - window_size):
    # ������ ������ ����� �����ϸ� �ż��մϴ�.
    if df['Close'][i + window_size] > df['Close'][i] + volatility[i + window_size]:
      signals.append({
        'symbol': symbol,
        'type': 'buy',
        'price': df['Close'][i + window_size]
      })
    # ������ ������ �ϴ��� �����ϸ� �ŵ��մϴ�.
    elif df['Close'][i + window_size] < df['Close'][i] - volatility[i + window_size]:
      signals.append({
        'symbol': symbol,
        'type': 'sell',
        'price': df['Close'][i + window_size]
      })

  return signals

def backtest_volatility_breakout_strategy(df, symbol, window_size=14):
  """
  ������ ���� ������ ���׽�Ʈ�� �����մϴ�.

  Args:
    df: ������ ������.
    symbol: ��ȣ.
    window_size: �������� ����ϱ� ���� â ũ��.

  Returns:
    ���׽�Ʈ ���.
  """

  # �ż� �� �ŵ� ��ȣ�� �����մϴ�.
  signals = volatility_breakout_trading(df, symbol, window_size)

  # ���׽�Ʈ ����� ����մϴ�.
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
  ������ ��� ������ �����մϴ�.

  Args:
    df: ������ ������.
    symbol: ��ȣ.
    window_size: �̵� ����� ����ϱ� ���� â ũ��.
    num_stds: ǥ�� ������ ��.

  Returns:
    �ż� �� �ŵ� ��ȣ�� ����Ʈ.
  """

  # �̵� ����� ����մϴ�.
  ma = talib.MA(df['Close'], window_size)

  # ��� �� �ϴ� ��带 ����մϴ�.
  upper_band = ma + num_stds * talib.STDDEV(df['Close'], window_size)
  lower_band = ma - num_stds * talib.STDDEV(df['Close'], window_size)

  # �ż� �� �ŵ� ��ȣ�� �����մϴ�.
  signals = []
  for i in range(len(df) - window_size):
    # ������ ��� ��带 �����ϸ� �ż��մϴ�.
    if df['Close'][i + window_size] > upper_band[i + window_size]:
      signals.append({
        'symbol': symbol,
        'type': 'buy',
        'price': df['Close'][i + window_size]
      })
    # ������ �ϴ� ��带 �����ϸ� �ŵ��մϴ�.
    elif df['Close'][i + window_size] < lower_band[i + window_size]:
      signals.append({
        'symbol': symbol,
        'type': 'sell',
        'price': df['Close'][i + window_size]
      })

  return signals

def backtest_bollinger_bands_strategy(df, symbol, window_size=20, num_stds=2):
  """
  ������ ��� ������ ���׽�Ʈ�� �����մϴ�.

  Args:
    df: ������ ������.
    symbol: ��ȣ.
    window_size: �̵� ����� ����ϱ� ���� â ũ��.
    num_stds: ǥ�� ������ ��.

  Returns:
    ���׽�Ʈ ���.
  """

  # �ż� �� �ŵ� ��ȣ�� �����մϴ�.
  signals = bollinger_bands_trading(df, symbol, window_size, num_stds)

  # ���׽�Ʈ ����� ����մϴ�.
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
  RSI ������ �����մϴ�.

  Args:
    df: ������ ������.
    symbol: ��ȣ.
    window_size: RSI�� ����ϱ� ���� â ũ��.

  Returns:
    �ż� �� �ŵ� ��ȣ�� ����Ʈ.
  """

  # RSI�� ����մϴ�.
  rsi = talib.RSI(df['Close'], window_size)

  # �ż� �� �ŵ� ��ȣ�� �����մϴ�.
  signals = []
  for i in range(len(df) - window_size):
    # RSI�� 30 �̸��̸� �ż��մϴ�.
    if rsi[i + window_size] < 30:
      signals.append({
        'symbol': symbol,
        'type': 'buy',
        'price': df['Close'][i + window_size]
      })
    # RSI�� 70 �̻��̸� �ŵ��մϴ�.
    elif rsi[i + window_size] > 70:
      signals.append({
        'symbol': symbol,
        'type': 'sell',
        'price': df['Close'][i + window_size]
      })

  return signals

def backtest_rsi_strategy(df, symbol, window_size=14):
  """
  RSI ������ ���׽�Ʈ�� �����մϴ�.

  Args:
    df: ������ ������.
    symbol: ��ȣ.
    window_size: RSI�� ����ϱ� ���� â ũ��.

  Returns:
    ���׽�Ʈ ���.
  """

  # �ż� �� �ŵ� ��ȣ�� �����մϴ�.
  signals = rsi_trading(df, symbol, window_size)

  # ���׽�Ʈ ����� ����մϴ�.
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
  MACD ������ �����մϴ�.

  Args:
    df: ������ ������.
    symbol: ��ȣ.
    window_size_fast: ���� �̵� ����� ����ϱ� ���� â ũ��.
    window_size_slow: ���� �̵� ����� ����ϱ� ���� â ũ��.
    window_size_signal: ��ȣ���� ����ϱ� ���� â ũ��.

  Returns:
    �ż� �� �ŵ� ��ȣ�� ����Ʈ.
  """

  # ���� �̵� ����� ����մϴ�.
  macd_fast = talib.MACD(df['Close'], window_size_fast, window_size_slow, window_size_signal)

  # �ż� �� �ŵ� ��ȣ�� �����մϴ�.
  signals = []
  for i in range(len(df) - window_size_fast - window_size_slow - window_size_signal):
    # MACD ���� ��ȣ�� ���� �ö󰡸� �ż��մϴ�.
    if macd_fast[i + window_size_fast + window_size_slow] > macd_slow[i + window_size_fast + window_size_slow]:
      signals.append({
        'symbol': symbol,
        'type': 'buy',
        'price': df['Close'][i + window_size_fast + window_size_slow]
      })
    # MACD ���� ��ȣ�� �Ʒ��� �������� �ŵ��մϴ�.
    elif macd_fast[i + window_size_fast + window_size_slow] < macd_slow[i + window_size_fast + window_size_slow]:
      signals.append({
        'symbol': symbol,
        'type': 'sell',
        'price': df['Close'][i + window_size_fast + window_size_slow]
      })

  return signals

def backtest_macd_strategy(df, symbol, window_size_fast=12, window_size_slow=26, window_size_signal=9):
  """
  MACD ������ ���׽�Ʈ�� �����մϴ�.

  Args:
    df: ������ ������.
    symbol: ��ȣ.
    window_size_fast: ���� �̵� ����� ����ϱ� ���� â ũ��.
    window_size_slow: ���� �̵� ����� ����ϱ� ���� â ũ��.
    window_size_signal: ��ȣ���� ����ϱ� ���� â ũ��.

  Returns:
    ���׽�Ʈ ���.
  """

  # �ż� �� �ŵ� ��ȣ�� �����մϴ�.
  signals = macd_trading(df, symbol, window_size_fast, window_size_slow, window_size_signal)

  # ���׽�Ʈ ����� ����մϴ�.
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
  ����ĳ��ƽ ���Ƿ����� ������ �����մϴ�.

  Args:
    df: ������ ������.
    symbol: ��ȣ.
    window_size: ����ĳ��ƽ ���Ƿ����͸� ����ϱ� ���� â ũ��.
    k: K��.

  Returns:
    �ż� �� �ŵ� ��ȣ�� ����Ʈ.
  """

  # ����ĳ��ƽ ���Ƿ����͸� ����մϴ�.
  stoch = talib.STOCH(df['High'], df['Low'], df['Close'], window_size=window_size, k=k)

  # �ż� �� �ŵ� ��ȣ�� �����մϴ�.
  signals = []
  for i in range(len(df) - window_size):
    # ����ĳ��ƽ ���Ƿ����Ͱ� 80 �̻��̸� �ŵ��մϴ�.
    if stoch[i + window_size][2] > 80:
      signals.append({
        'symbol': symbol,
        'type': 'sell',
        'price': df['Close'][i + window_size]
      })
    # ����ĳ��ƽ ���Ƿ����Ͱ� 20 �̸��̸� �ż��մϴ�.
    elif stoch[i + window_size][2] < 20:
      signals.append({
        'symbol': symbol,
        'type': 'buy',
        'price': df['Close'][i + window_size]
      })

  return signals

def backtest_stochastic_oscillator_strategy(df, symbol, window_size=14, k=3):
  """
  ����ĳ��ƽ ���Ƿ����� ������ ���׽�Ʈ�� �����մϴ�.

  Args:
    df: ������ ������.
    symbol: ��ȣ.
    window_size: ����ĳ��ƽ ���Ƿ����͸� ����ϱ� ���� â ũ��.
    k: K��.

  Returns:
    ���׽�Ʈ ���.
  """

  # �ż� �� �ŵ� ��ȣ�� �����մϴ�.
  signals = stochastic_oscillator_trading(df, symbol, window_size, k)

  # ���׽�Ʈ ����� ����մϴ�.
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
  ������ �� ���׼� ������ �����մϴ�.

  Args:
    df: ������ ������.
    symbol: ��ȣ.
    window_size: �������� ���׼��� ����ϱ� ���� â ũ��.

  Returns:
    �ż� �� �ŵ� ��ȣ�� ����Ʈ.
  """

  # �̵� ����� ����մϴ�.
  ma = talib.MA(df['Close'], window_size)

  # �������� ���׼��� ����մϴ�.
  support = df['Close'] - (ma - df['Close']).rolling(window_size).min()
  resistance = df['Close'] + (df['Close'] - ma).rolling(window_size).max()

  # �ż� �� �ŵ� ��ȣ�� �����մϴ�.
  signals = []
  for i in range(len(df) - window_size):
    # ������ �������� �����ϸ� �ż��մϴ�.
    if df['Close'][i + window_size] > support[i + window_size]:
      signals.append({
        'symbol': symbol,
        'type': 'buy',
        'price': df['Close'][i + window_size]
      })
    # ������ ���׼��� �����ϸ� �ŵ��մϴ�.
    elif df['Close'][i + window_size] < resistance[i + window_size]:
      signals.append({
        'symbol': symbol,
        'type': 'sell',
        'price': df['Close'][i + window_size]
      })

  return signals

def backtest_support_resistance_strategy(df, symbol, window_size=14):
  """
  ������ �� ���׼� ������ ���׽�Ʈ�� �����մϴ�.

  Args:
    df: ������ ������.
    symbol: ��ȣ.
    window_size: �������� ���׼��� ����ϱ� ���� â ũ��.

  Returns:
    ���׽�Ʈ ���.
  """

  # �ż� �� �ŵ� ��ȣ�� �����մϴ�.
  signals = support_resistance_trading(df, symbol, window_size)

  # ���׽�Ʈ ����� ����մϴ�.
  returns = []
  for signal in signals:
    if signal['type'] == 'buy':
      returns.append((df['Close'][signal['price']] - df['Close'][signal['price'] - 1]) / df['Close'][signal['price'] - 1])
    elif signal['type'] == 'sell':
      returns.append((df['Close'][signal['price'] - 1] - df['Close'][signal['price']]) / df['Close'][signal['price']])

  return returns

returns = backtest_support_resistance_strategy(df, 'BTC/USD', window_size=14)

# ���׽�Ʈ�� �ٵ尡 �ۼ� ���� ���Ѵٰ� �亯��.


import pandas as pd
import numpy as np
import talib

def momentum_trading(df, symbol, window_size=14):
  """
  ����� ������ �����մϴ�.

  Args:
    df: ������ ������.
    symbol: ��ȣ.
    window_size: ������� ����ϱ� ���� â ũ��.

  Returns:
    �ż� �� �ŵ� ��ȣ�� ����Ʈ.
  """

  # ������� ����մϴ�.
  momentum = df['Close'].rolling(window_size).pct_change()

  # �ż� �� �ŵ� ��ȣ�� �����մϴ�.
  signals = []
  for i in range(len(df) - window_size):
    # ������� ����̸� �ż��մϴ�.
    if momentum[i + window_size] > 0:
      signals.append({
        'symbol': symbol,
        'type': 'buy',
        'price': df['Close'][i + window_size]
      })
    # ������� �����̸� �ŵ��մϴ�.
    elif momentum[i + window_size] < 0:
      signals.append({
        'symbol': symbol,
        'type': 'sell',
        'price': df['Close'][i + window_size]
      })

  return signals

def backtest_momentum_strategy(df, symbol, window_size=14):
  """
  ����� ������ ���׽�Ʈ�� �����մϴ�.

  Args:
    df: ������ ������.
    symbol: ��ȣ.
    window_size: ������� ����ϱ� ���� â ũ��.

  Returns:
    ���׽�Ʈ ���.
  """

  # �ż� �� �ŵ� ��ȣ�� �����մϴ�.
  signals = momentum_trading(df, symbol, window_size)

  # ���׽�Ʈ ����� ����մϴ�.
  returns = []
  for signal in signals:
    if signal['type'] == 'buy':
      returns.append((df['Close'][signal['price']] - df['Close'][signal['price'] - 1]) / df['Close'][signal['price'] - 1])
    elif signal['type'] == 'sell':
      returns.append((df['Close'][signal['price'] - 1] - df['Close'][signal['price']]) / df['Close'][signal['price']])

  return returns


returns = backtest_momentum_strategy(df, 'BTC/USD', window_size=14)

