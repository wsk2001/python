import pandas as pd
import matplotlib.pyplot as plt

# 비트코인 OHLCV 데이터를 읽습니다.
df = pd.read_csv('bitcoin_ohlcv.csv', parse_dates=True)

# 고가와 저가를 추출합니다.
high = df['High']
low = df['Low']

# 지지선과 저항선을 찾기 위해 고가와 저가를 슬라이딩 윈도우에 통과시킵니다.
for i in range(len(df) - 2):
    # 지지선
    support = low[i] - (high[i] - low[i]) * 0.382

    # 저항선
    resistance = high[i] + (high[i] - low[i]) * 0.618

    # 지지선과 저항선을 플로팅합니다.
    plt.plot([support, support], [df['Open'][i], df['Close'][i]], 'r--')
    plt.plot([resistance, resistance], [df['Open'][i], df['Close'][i]], 'g--')

# 플롯을 표시합니다.
plt.show()
