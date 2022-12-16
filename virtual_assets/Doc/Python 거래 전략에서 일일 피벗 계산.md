# Python 거래 전략에서 일일 피벗 계산

### 피벗 포인트란 무엇입니까?

피벗 포인트는 데이 트레이딩 에서 자주 사용되는 가격 수준입니다(하지만 스윙 거래에서도 사용할 수 있음). 그들은 일일 시장 세션 동안 가격에 대한 '자연적인' 지지 및 저항으로 간주되므로 시장이 그들에게 가까워질 때 종종 사소하지 않은 방식으로 행동하기 때문에 데이 트레이더에게 매우 유용할 수 있습니다.

여러 유형의 피벗 포인트가 있지만 클래식 피벗 포인트는 일반적으로 마지막 날의 고가, 저가 및 종가에서 시작하여 정의됩니다. 거래자는 이전 시장일의 이러한 가격에 일부 수학적 계산을 적용하여 현재 시장일의 피벗 수준을 계산하고 사용할 수 있습니다. 이 기사에서는 고전적인 피벗 포인트에 중점을 둘 것입니다.

데이 트레이더는 예를 들어 가격이 피벗 수준에 가까운 곳에서 거래 기회를 찾을 수 있습니다. 예를 들어 풀백이나 브레이크아웃을 기다리고 가장 가까운 피벗 수준을 목표로 사용합니다.

### 계산 방법

클래식 피벗 레벨은 마지막 날의 고가, 저가 및 종가에 적용된 [Tradingview 지식 기반](https://www.tradingview.com/support/solutions/43000521824-pivot-points-standard/)에서 가져온 다음 공식에 따라 계산됩니다.

- PP = (High + Low + Close) / 3

- R1 = 2 * PP — Low

- S1 = 2 * PP — High

- R2 = PP + (High — Low)

- S2 = PP — (High — Low)

- R3 = PP + 2 * (High — Low)

- S3 = PP — 2 * (High — Low)

  



PP는 주요 피벗 수준입니다. S1, S2 및 S3은 지원 수준입니다. R1, R2 및 R3은 저항 수준입니다.

``` py
last_day['Pivot'] = (last_day['High'] + last_day['Low'] + last_day['Close'])/3
last_day['R1'] = 2*last_day['Pivot'] - last_day['Low']
last_day['S1'] = 2*last_day['Pivot'] - last_day['High']
last_day['R2'] = last_day['Pivot'] + (last_day['High'] - last_day['Low'])
last_day['S2'] = last_day['Pivot'] - (last_day['High'] - last_day['Low'])
last_day['R3'] = last_day['Pivot'] + 2*(last_day['High'] - last_day['Low'])
last_day['S3'] = last_day['Pivot'] - 2*(last_day['High'] - last_day['Low'])
```



