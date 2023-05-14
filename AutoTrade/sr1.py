import pandas as pd
import matplotlib.pyplot as plt

# ��Ʈ���� OHLCV �����͸� �н��ϴ�.
df = pd.read_csv('bitcoin_ohlcv.csv', parse_dates=True)

# ���� ������ �����մϴ�.
high = df['High']
low = df['Low']

# �������� ���׼��� ã�� ���� ���� ������ �����̵� �����쿡 �����ŵ�ϴ�.
for i in range(len(df) - 2):
    # ������
    support = low[i] - (high[i] - low[i]) * 0.382

    # ���׼�
    resistance = high[i] + (high[i] - low[i]) * 0.618

    # �������� ���׼��� �÷����մϴ�.
    plt.plot([support, support], [df['Open'][i], df['Close'][i]], 'r--')
    plt.plot([resistance, resistance], [df['Open'][i], df['Close'][i]], 'g--')

# �÷��� ǥ���մϴ�.
plt.show()
