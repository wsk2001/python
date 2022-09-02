[OBV 거래량 지표를 이용한 알고리즘 투자 전략 (feat. 파이썬)](https://skyeong.net/281)

[데이터 사이언스/데이터 분석 실습](https://skyeong.net/category/데이터 사이언스/데이터 분석 실습) 2020. 12. 25. 18:31

> 주의: 이 글은 교육적인 목적으로 작성되었습니다. 투자 조언으로 받아 들여서는 안되며, 투자는 본인의 재량에 따라 하십시오.

출처: https://skyeong.net/281?category=944392



이번 글에서는 On-Balance Volume이라는 거래량 지표와 파이썬 프로그래밍을 사용한 간단한 거래 전략에 대해 설명해 드리겠습니다. 주식 시장의 모멘텀 방향을 예측하는 것은 매우 어려운 일이긴 하지만 한번 시도해 보겠습니다. 통계와 확률에 대해 잘 이해하고있는 사람도 이번에 소개드릴 내용을 이해하고 프로그래밍하는데 어려움을 겼을 수 있습니다. 알고리즘 거래는 가격, 타이밍, 그리고 거래량과 같은 변수를 이용하여 미리 프로그래밍된 자동화 거래 지침을 사용하여 주문을 실행하는 프로세스입니다.

금융 분야에서 가장 인기 있는 프로그래밍 언어 중 하나인 파이썬과 On-Balance Volume (OBV)이라는 지표를 이용하여 주식을 매매 할 시기를 알 수 있는 거래 전략을 만들어 보겠습니다.

## OBV (On-Balance Volume) 란 무엇입니까? 

거래량 균형(OBV)은 주식 거래량 흐름을 사용하여 주가의 변화를 예측하는 기술 거래 모멘텀 지표입니다. Joseph Granville은 1963년 저서 New Key to Stock Market Profits에서 처음으로 OBV 지표를 발표했습니다. Granville은 거래량이 시장의 핵심 원동력이라고 믿고 거래량 변화에 따라 시장의 주요 움직임이 발생할 때를 예측 할 수 있도록 OBV를 설계했습니다. Granville는 거의 저서에서 OBV에 의해 생성 된 예측을 "단단하게 감긴 스프링"이라고 설명했습니다. 그는 주가의 큰 변화없이 거래량이 급격히 증가하면 결국 가격이 상승하거나 하락할 것이라고 믿었습니다.

### OBV 추세 신호

- 가격과 OBV 모두 더 높은 정점과 더 높은 저점을 만들면 상승 추세가 계속 될 것입니다. 
- 가격이 계속해서 저점을 낮추고 OBV가 저점을 낮추지 못하면 하락 추세가 정체되거나 반등 할 가능성이 높습니다.이를 포지티브 다이버전스라고 합니다. 
- 거래 기간 동안 OBV가 상승하면 누적이 발생할 수 있습니다. 이는 상승 돌파에 대한 경고입니다. 
- 거래 기간 동안 OBV가 하락하면 분배가 발생할 수 있습니다. 이는 하락 돌파에 대한 경고입니다. 
- 가격이 계속해서 더 높은 피크를 만들고 OBV가 더 높은 피크를 만들지 못하면 상승 추세가 정체되거나 실패 할 가능성이 있습니다.이를 음의 발산이라고 합니다. 
- 가격이 계속해서 저점을 낮추고 OBV가 저점을 낮추지 못하면 하락 추세가 정체되거나 실패 할 가능성이 높습니다. 이를 양의 발산이라고 합니다.

## OBV 계산 방법

OBV는 다음 공식에 의해서 계산됩니다.  



![img](https://blog.kakaocdn.net/dn/uf4dC/btqRnN9Xga0/LvkkutvFpbVOSBC12y0zL0/img.png)



 

## **OBV를 이용한 매수/매도 타이밍 전략** 

### **전략 #1** 

OBV를 사용하는 거래자는 거래 전략을 세우기 위해 OBV의 변화율에 관심을 가지는 경우가 있습니다. OBV가 상승 방향으로 움직이고 있다면 큰 주가 상승이 올 수 있다고 생각 할 수 있고, OBV가 하락 방향으로 움직이고 있다면 큰 주가 하락을 생각할 수 있습니다. 예를 들어, OBV가 해당 가격 변동보다 빠르게 하락하면 조만간 엄청나게 큰 가격 하락이 올 가능성이 있음을 알 수 있습니다.

### **전략 #2**

OBV에 이동 평균을 추가하여 주식을 매매 할 시기를 결정하고 교차점(Cross-over)을 신호로 거래할 수도 있습니다. 이것이 이번에 소개해 드릴 내용입니다.

> OBV가 지수 이동 평균 (EMA) 이상에서 거래를 시작하면 주식을 매수할 타이밍을 의미합니다.
> OBV가 지수 이동 평균 (EMA) 아래에서 거래를 시작하면 주식을 매도할 타이밍을 의미합니다.

참고 : OBV의 장기 이동 평균으로 100일 기간 지수 이동 평균을 추가하면 단기 이동 평균보다 더 효과적입니다. 200 지수 이동 평균은 매수/매도 타이밍을 조금 더 적게 산출해 줍니다. OBV에서 매수/매도 타이밍을 Whipsaw라고 하는데, 이는 특정 시간에 유가 증권의 가격이 한 방향으로 움직이다가 반대 방향으로 빠르게 움직일 때를 의미하며 주식의 매수와 매도에 대한 거래량의 움직임을 설명해 줍니다.

## **OBV 전략의 요점** 

OBV는 거래량이 늘어난 날과 내려간날의 단순 누적 합계입니다. OBV가 가격과 함께 움직이면 현재 추세와 동행하고 있음을 알 수 있습니다. OBV와 가격 사이의 차이가 발생한다면 주가 흐림이 반전 될 수 있음을 의미합니다. 추세선을 사용하면 OBV와 가격 흐림에 차이가 발생하는지 파악하여 거래 기회를 획득하는데 도움이 될 수 있습니다. OBV는 가격 변화 방향을 예측하는데도 도움이 됩니다. OBV를 이용함에 있어 주의해야 할 점이 있습니다. 가령, 어떤 특별한 이유 없이 거래량이 급증하는 경우가 있는데, 이런 경우에는 지표가 왜곡되어 객관적인 해석을 더 어려워 지기도 합니다. 또한 OBV가 종종 가격을 선도하는 것처럼 보일 수 있지만, 이것은 종종 우리가 찾고자 하는 증거를 검색하는 경우입니다. 따라서 OBV는 가격 분석과 함께 활용될 수 있는 지표지만 전적으로 OBV에 의존해서 투자전략을 세우기에는 한계가 있습니다.

- OBV는 가격 예측을 위해 거래량의 변화를 사용하는 기술적 지표입니다. 
- OBV는 해당 종목에 반영된 강세 또는 약세에 대한 군중 심리를 보여줍니다. 
- 가격과 OBV 간의 상대적인 추세 흐름을 비교하면, 주식 차트 하단에서 띄워놓고 보는 (빨간색 또는 초록색으로 표시되는) 거래량 히스토그램 보다 더 많은 정보를 알 수 있습니다.

## **파이썬을 이용한 OBV 투자 전략**

파이썬을 이용해서 OBV를 계산하고, 이를 기반으로 투자 전략을 세워보겠습니다. 우선 분석이 필요한 라이브러리를 Import 하겠습니다.

```
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
```

 

## **주식 데이터 불러오기**

실습에 사용하게될 예제로 코로나19 백신 개발 업체로 잘 알려진 아스트라제네카(NYSE: AZN) 데이터를 사용하겠습니다. 야후 파이낸스에서 데이터를 가져오려면 yfinance 라이브러리가 필요합니다. yfinance 라이브러리가 없다면, '!pip install yfinance'를 통해서 설치해주세요.

```
import yfinance as yf
df = yf.download('AZN', start="2018-12-01", end="2020-11-30")
df['Date'] = df.index
df.head()
```



![img](https://blog.kakaocdn.net/dn/b9zCYT/btqReRstpCf/aRG0kbb7d7aOlO2D0KCoxK/img.png)



 

## **주가 데이터 시각화**

아래 파이썬 코드를 이용하여 yfinance에서 불러온 주가 데이터를 시각화 해보겠습니다.

```
# Create and plot the graph
plt.figure(figsize=(12.2,4.5)) #width = 12.2in, height = 4.5
plt.plot( df['Close'],  label='Close')#plt.plot( X-Axis , Y-Axis, line_width, alpha_for_blending,  label)
plt.xticks(rotation=45) 
plt.title('Close Price History')
plt.xlabel('Date',fontsize=18)
plt.ylabel('Price USD ($)',fontsize=18)
plt.show()
```



![img](https://blog.kakaocdn.net/dn/bF0iH7/btqRheUZT0f/NpbfS953qeU7IEsiuJpUs1/img.png)



 

## **OBV 계산하기**

```
#Calculate the On Balance Volume
OBV = []
OBV.append(0)
for i in range(1, len(df.Close)):
    #If the closing price is above the prior close price 
    if df.Close[i] > df.Close[i-1]: 
        #then: Current OBV = Previous OBV + Current Volume
        OBV.append(OBV[-1] + df.Volume[i]) 
    elif df.Close[i] < df.Close[i-1]:
        OBV.append( OBV[-1] - df.Volume[i])
    else:
       OBV.append(OBV[-1])
```

 

## **OBV와** **지수 이동 평균을 새로운 컬럼에 추가하기**

```
# OBV값을 pd.DataFrame의 새로운 컬럼에 추가 
df['OBV'] = OBV

# 지수 평균 이동값 계산
df['OBV_EMA'] = df['OBV'].ewm(com=20).mean()

# 데이터 출력
df
```



![img](https://blog.kakaocdn.net/dn/6jdpe/btqRoRD08QY/uoPX6tr5wmKiYGKUJaOIl0/img.png)



 

 

## **OBV와 OBV의 지수 이동 평균값 시각화**

```
#Create and plot the graph
plt.figure(figsize=(12.2,4.5)) #width = 12.2in, height = 4.5
plt.plot( df['OBV'],  label='OBV', color= 'orange')
plt.plot( df['OBV_EMA'],  label='OBV_EMA', color= 'purple')
plt.xticks(rotation=45) 
plt.title('OBV/OBV_EMA')
plt.xlabel('Date',fontsize=18)
plt.ylabel('Price USD ($)',fontsize=18)
plt.show()
```



![img](https://blog.kakaocdn.net/dn/ohVEq/btqRigrABTU/x4YO7GbLYnnKUSzBCoVXn1/img.png)



 

## **매수/매도 타이밍 신호 찾는 함수 생성**

- 매수 신호: OBV > OBV_EMA
- 매도 신호: OBV < OBV_EMA

```
def buy_sell(signal, col1, col2):
  sigPriceBuy = []
  sigPriceSell = []
  flag = -1 #A flag for the trend upward/downward

  #Loop through the length of the data set
  for i in range(0,len(signal)):

    #if OBV > OBV_EMA  and flag != 1 then buy else sell
      if signal[col1][i] > signal[col2][i] and flag != 1:
          sigPriceBuy.append(signal['Close'][i])
          sigPriceSell.append(np.nan)
          flag = 1

      #else  if OBV < OBV_EMA  and flag != 0 then sell else buy
      elif signal[col1][i] < signal[col2][i] and flag != 0:    
          sigPriceSell.append(signal['Close'][i])
          sigPriceBuy.append(np.nan)
          flag = 0

      #else   OBV == OBV_EMA  so append NaN 
      else: 
        sigPriceBuy.append(np.nan)
        sigPriceSell.append(np.nan)

  return (sigPriceBuy, sigPriceSell)
```

 

## **매수/매도 신호값을 새로운 컬럼에 추가**

```
x = buy_sell(df, 'OBV','OBV_EMA' )
df['Buy_Signal_Price'] = x[0]
df['Sell_Signal_Price'] = x[1]
#Show the data frame
df
```



![img](https://blog.kakaocdn.net/dn/bZdlcQ/btqRoQrCsQR/wETNUaJHh8on4AS1R7qaTk/img.png)



## **매도/매도 신호 시각화**

```
# Create and plot the graph
plt.figure(figsize=(12.2,4.5)) #width = 12.2in, height = 4.5
plt.scatter(df.index, df['Buy_Signal_Price'], color = 'green', 
                    label='Buy Signal',  marker = '^', alpha = 1)
plt.scatter(df.index, df['Sell_Signal_Price'], color = 'red',
                    label='Sell Signal', marker = 'v', alpha = 1)
plt.plot( df['Close'],  label='Close Price', alpha = 0.35)
plt.xticks(rotation=45)
plt.title('The Stock Buy / Sell Signals')
plt.xlabel('Date',fontsize=18)
plt.ylabel('Close Price USD ($)',fontsize=18)
plt.legend( loc='upper left')
plt.show()
```



![img](https://blog.kakaocdn.net/dn/b4xrX3/btqRnNa1ErW/yUhJ2nOevjthWycyl52Ktk/img.png)



그래프를 살펴보면 OBV를 이용한 투자 전략이 어느정도 잘 작동하는 것 같습니다. 즉, 이 데이터 세트에 이 전략을 사용했다면, 이 기간 내에 수익을 올렸을 것입니다. 그러나 이 지표가 완벽하지 않으며 전략이 성공을 보장하지 않는다는 점을 명심하십시오. 이 전략을 사용하기 전에 더 많은 테스트를 수행해야하며 주식을 매매 할시기에 대한 자세한 정보를 위해 OBV 전략과 함께 다른 지표를 함께 사용하시길 권장드립니다.

참고) 이 글은 randerson112358의 Know When To Buy and Sell Stock Using A Trading Strategy With On-Balance Volume (OBV) and Python을 각색하여 한글로 번역한 글입을 밝힙니다. 원문은 [링크](https://randerson112358.medium.com/stock-trading-strategy-using-on-balance-volume-obv-python-77a7c719cdac)를 통해서 확인하실 수 있습니다.



---

[이동평균선과 RSI를 이용한 알고리즘 투자전략 (feat. 파이썬)](https://skyeong.net/278)

[데이터 사이언스/데이터 분석 실습](https://skyeong.net/category/데이터 사이언스/데이터 분석 실습) 2020. 12. 25. 18:31

> 이 글은 교육적인 목적으로 작성되었습니다. 투자 조언으로 받아 들여서는 안되며, 투자는 본인의 재량에 따라 하십시오.

## **주식 시장의 기술 지표란****?**

주식 시장의 기술 지표란 주식 가격의 추이 또는 회사의 재무 데이터를 해석하여 미래의 가격 변동을 예측하는데 사용되는 일종의 참고 자료라고 할 수 있습니다. 주식 시장의 기술 지표는 투자자가 보유하고 있는 종목을 매도 할 타이밍인지? 아니면, 새로운 종목을 매수 할 타이밍인지? 등을 결정하는데 참고로 활용할 수 있습니다.

## **기본적인 기술 지표**

단순 이동 평균(Simple Moving Average, SMA) : 단순 이동 평균선은 "이평선"이라고도 불리며, 현재 주가의 트렌드가 계속 될지 또는 하락 추세를 반전하는 계기가 될지 여부를 판단하는데 도움이 될 수있는 기술적 추세 지표입니다. 단순 이동 평균선을 약간 변형한 것으로 지수 이동 평균선이 있는데, 이는 최근의 주가 흐름에 더 많은 가중치를 둔 이평선 이라고 할 수 있습니다.

지수 이동 평균(Exponential Moving Average, EMA) : 지수 이동 평균선은 가장 최근 데이터에 더 큰 가중치와 중요성을 부여하는 이동 평균입니다. 다른 이동 평균과 마찬가지로 이 기술 추세 지표는 과거 평균값과의 교차 및 다이버전스를 하는 시점을 기반으로 매수 및 매도 타이밍을 결정하는데 활용할 수 있습니다.

이동 평균 수렴 발산(Moving Average Convergence Divergence, MACD) : 이동 평균 수렴 발산선은 주식 가격의 두가지 이동 평균선 간의 관계를 보여주는 추세 추종 모멘텀 지표입니다. 이동 평균 수렴 발산선은 12일 지수 이동 평균선에서 26일 지수 이동 평균선을 뺀 값으로 계산됩니다.

상대적 강도 지수(Relative Strength Index, RSI): 상대적 강도 지수는 주식 또는 기타 자산 가격의 과매수 또는 과매도 상태를 평가하기 위한 방법으로 최근 가격 변화의 규모를 측정하기 위한 기술 분석에 사용되는 모멘텀 지표입니다. 

## **지표를 이용한 몇 가지 거래 전략**

**이동 평균 교차점(Moving Average Crossover)**: 주식 시장 기술 분석에서 이동 평균 교차점은 두 이동 평균이 서로 교차 하는 시점을 의미합니다. 이중 이동 평균 교차 거래 전략이란 단기 이동 평균이 장기 이동 평균 위로 r교차할 때 매수(또는 장기 보유) 신호를 나타내고 장기 이동 평균선이 단기 이동 평균선 위로 교차하면 매도(또는 단기 보유)를 알라는 신호를 나타냅니다. 이번 글에서는 이중 단순 이동 평균 교차 전략과 3가지 지수 이동 평균 교차 전략을 파이썬으로 프로그래밍하는 방법을 소개해 드리겠습니다.

> 매수 신호: 단기 이동 평균선 > 장기 이동 평균선
> 매도 신호: 단기 이동 평균선 < 장기 이동 평균선



![img](https://blog.kakaocdn.net/dn/8uNHZ/btqRhesKKDx/oiWiPWEwWQJojO9FsXjn4K/img.png)



 

**3개의 지수 이동 평균선을 이용하는 교차 전략:** 다양한 길이의 3가지(Short, Middle, Long) 지수 이동 평균을 사용하는 거래 방법입니다. 이 전략은 Middle의 이동 평균선이 Long 이동 평균을 넘어서고 Short 이동 평균이 Middle 이동 평균을 넘어갈 때를 매수 타이밍이라고 합니다. 또한, 이 전략에서 Short 이동 평균이 Middle 이동 평균 아래로 교차하는 경우를 매도 타이밍이라고 합니다.

> 매수 신호: Middle > Long
> 매도 신호: Short > Middle



![img](https://blog.kakaocdn.net/dn/cQqyqo/btqQ56J4acI/wJd7pB362ySva6BUJMyrvk/img.png)



 

**이동 평균 수렴/발산 (Moving Average Convergence/Divergence, MACD) 크로스 오버** : 이동 평균 수렴/발산의 줄임말인 MACD는 주가의 기술적 분석에 사용되는 거래 지표 중 한가지입니다. MACD 지표가 신호선을 교차하면 이는 주가의 모멘텀을 받으며 변화할 것임을 의미합니다. 예를 들어 MACD 지표가 신호선보다 크면 이는 강세 크로스 오버로 간주되어 매수하기 좋은 시점을 나타내며, MACD 지표가 신호선보다 작으면 약세 크로스 오버로 간주되어 매도하기에 좋은 시점을 나타냅니다.

> 매수 신호: 이동 평균 수림/발산 > 신호선
> 매도 신호: 이동 평균 수렴/발산 > 신호선



![img](https://blog.kakaocdn.net/dn/sQOCE/btqQ3hkNHJq/iWAZRzekpkrtMCkzd9FFPK/img.png)



**상대적 강도 지수(Relative Strength Index, \**RSI\**)**: RSI는 주식이 과매수인지 과매도인지를 결정하기 위해 사용되는 기술 지표입니다. RSI를 계산하기 위해 분석에 사용되는 기간은 일반적으로 14일입니다. RSI는 (70 및 30), (80 및 20) 및 (90 및 10)와 같이 표시된 높은 수준값과 낮은 수준 값을 함께 표시하며, 0에서 100까지의 범위를 갖습니다. 높은 수준이 높고 낮은 수준이 낮을수록 가격 모멘텀 이동이 더 강함을 나타냅니다. 예를 들어 RSI는 70을 초과하면 과매 수로 간주되고 30 미만에서는 과매도 된 것으로 간주됩니다. 50의 RSI 값은 중립 상태를 나타냅니다.

> 매수 신호: RSI = 30 또는 그 이하
> 매도 신호: RSI = 70 또는 그 이상



![img](https://blog.kakaocdn.net/dn/LUC3t/btqRawVt3aL/V6srN9L68KkmgcS6SpSNOk/img.png)



 

------

 

## **파이썬을 이용한 기술지표 계산**

파이썬을 이용해서 위에서 설명한 4가지 기술지표를 계산해 보겠습니다. 우선 분석이 필요한 라이브러리를 Import 하겠습니다.

```
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
```

이제 예시 데이터를 야후에서 다운로드 받오겠습니다. 2020년에 미국 주식시장을 뜨겁게 했던 종목 중에 하나인 테슬라(NYSE: TSLA)의 최근 1년 데이터를 예제로 사용하겠습니다. 야후 파이낸스를 통해 데이터를 가져오겠습니다. 혹시 관련 라이브러리가 없는 분은 아래 명령어로 라이브러리를 설치해 주시기 바랍니다.

```
! pip install yfinance
```

### **주식 데이터 가져오기**

```
import yfinance as yf
df = yf.download('TSLA', start="2019-12-01", end="2020-11-30")
df['Date'] = df.index
df.head()
```



![img](https://blog.kakaocdn.net/dn/vOid8/btqRePUyvOR/29MFGqn6WViC20q3kppoj1/img.png)테슬라(NYSE: TSLA) 주가 데이터 샘플



이제 위에서 설명했던 이동 평균선을 계산하는 함수들을 먼저 만들어 보겠습니다. 함수를 만든 후에, 해당 함수를 이용해서 매수/매도 타이밍을 찾는 부분을 설명 드릴께요.

### **단순 이동 평균(SMA)과 지수 이동 평균(EMA)을 계산하는 함수**

단순 이동 평균을 계산할때는 보통 30일 평균 값으로 계산하고, 지수 이동 평균을 계산할때는 보통 20일 평균 값으로 계산합니다.

```
# 단순 이동 평균(Simple Moving Average, SMA)
def SMA(data, period=30, column='Close'):
  return data[column].rolling(window=period).mean()

# 지수 이동 평균(Exponential Moving Average, EMA)
def EMA(data, period=20, column='Close'):
  return data[column].ewm(span=period, adjust=False).mean()
```

 

### **이동 평균 수렴/발산을 계산하는 함수(MACD)**

이동 평균 수렴/발산에서 단기 지수 이동 평균은 12일 평균값으로 계산하고, 장기 지수 이동 평균은 26일 평균값으로 하며, 신호선의 경우는 9일 평균값으로 계산합니다.

```
def MACD(data, period_long=26, period_short=12, period_signal=9, column='Close'):

  # 단기 지수 이평선 계산 (AKA Fast moving average)
  ShortEMA = EMA(data, period_short, column=column)

  # 장기 지수 이평선 계산 (AKA Slow moving average)
  LongEMA = EMA(data, period_long, column=column)

  # 이동 평균 수렴/발산 계산 
  data['MACD'] = ShortEMA - LongEMA

  # 신호선 계산 
  data['Signal_Line'] = EMA(data, period_signal, column='MACD')

 return data
```

 

### **상대적 강도 지수를 계산하는 함수(RSI)**

상대적 강도 지수(Relative Strength Index, RSI)는 보통 14일 동안의 데이터를 사용하여 계산합니다.

```
def RSI(data, period = 14, column = 'Close'):
  delta = data[column].diff(1)
  delta = delta.dropna() # or delta[1:]

  up =  delta.copy()  # delta 값 복사
  down = delta.copy() # delta 값 복사
  up[up < 0] = 0 
  down[down > 0] = 0 
  data['up'] = up
  data['down'] = down

  AVG_Gain = SMA(data, period, column='up')
  AVG_Loss = abs(SMA(data, period, column='down'))
  RS = AVG_Gain / AVG_Loss

  RSI = 100.0 - (100.0/ (1.0 + RS))
  data['RSI'] = RSI

  return data
```

 

### **각 이동 평균값을 DataFrame에 추가하기**

```
df = MACD(df, period_long=26, period_short=12, period_signal=9)
df = RSI(df, period=14)
df['SMA'] = SMA(df, period=30)
df['EMA'] = EMA(df, period=20)
df.tail()
```



![img](https://blog.kakaocdn.net/dn/3SEuE/btqReRx1mY2/pR5YofxdiG34suGijSiREK/img.png)



 

### **이동 평균 수렴/발산과 신호선 시각화**

```
column_list = ['MACD','Signal_Line']
df[column_list].plot(figsize=(12.2,6.4)) #Plot the data
plt.title('MACD for TSLA')
plt.ylabel('USD Price ($)')
```



![img](https://blog.kakaocdn.net/dn/b95ViD/btqReP73bgf/rXsDShm9Ckc9jZvyDRCLK1/img.png)



 

### **단순 이동 평균선과 주가 데이터 시각화**

```
column_list = ['SMA','Close']
df[column_list].plot(figsize=(12.2,6.4)) #Plot the data
plt.title('SMA for TSLA')
plt.ylabel('USD Price ($)')
```



![img](https://blog.kakaocdn.net/dn/RmY9E/btqRcHo51Gy/rZDdKGLM92fR1efcx2py61/img.png)



 

### **지수 이동 평균선과 주가 데이터 시각화**

```
column_list = ['EMA','Close']
df[column_list].plot(figsize=(12.2,6.4)) #Plot the data
plt.title('EMA for TSLA')
plt.ylabel('USD Price ($)')
```



![img](https://blog.kakaocdn.net/dn/ch5DIj/btqQ3gTIDlt/Uax5bzGTeraixpa5GTe6K0/img.png)



 

### **상대적 강도 지수(RSI) 시각화**

상대적 강도지수가 70이상이면 매도 타이밍이고, 30이하이면 매수 타이밍입니다.

```
column_list = ['RSI']
df[column_list].plot(figsize=(12.2,6.4)) #Plot the data
plt.title('RSI for TSLA')
plt.ylabel('USD Price ($)')
```



![img](https://blog.kakaocdn.net/dn/bmCi4w/btqQ8OhRMvK/3J3qVBk3xdYiKQHoB3oIak/img.png)



지금까지 설명해 드린 방법으로 자신만의 거래 전략을 만들어 보세요! 하나의 차트에 대해서 한가지 지표만으로 매수 또는 매도 타이밍을 잡는 것보다는 다양한 지표를 살펴보고, 여러 지표들이 어떤 방향성을 갖는지 비교/확인하면서 자신만의 거래 전략을 세워보는 것을 권장합니다.

참고) 이 글은 randerson112358의 Stock Market Technical Indicators를 각색하여 한글로 번역한 글입을 밝힙니다. 원문은 [링크](https://randerson112358.medium.com/stock-market-technical-indicators-5ffd179a30f9)를 통해서 확인하실 수 있습니다.



---

[자금 흐름 지표를 이용한 알고리즘 투자 전략 (feat. 파이썬)](https://skyeong.net/282)

[데이터 사이언스/데이터 분석 실습](https://skyeong.net/category/데이터 사이언스/데이터 분석 실습) 2020. 12. 25. 18:32

> 이 글은 교육적인 목적으로 작성되었습니다. 투자 조언으로 받아 들여서는 안되며, 투자는 본인의 재량에 따라 하십시오.

이번 글에서는 자금 흐름 지표(Money Flow Index, MFI)라는 거래 전략을 설명드리고 파이썬으로 코딩하는 방법을 알려드리겠습니다. MFI는 거래량 가중 [상대적 강도 지수](https://brunch.co.kr/@skyeong/16/write)(Relative Strength Index, RSI)라고도 하며, 자산 중에서 과매수 또는 과매도 신호를 식별하기 위해 가격 및 거래량 데이터를 이용해 계산합니다. 

MFI 값이 80 이상이면 과매수(매도 타이밍)로 간주되고, 20 미만이면 과매도(매수 타이밍)로 간주됩니다. 또한 MFI값이 90 또는 10인 경우를 임계값 이라고 합니다.

> 매도 신호: MFI > 80
> 매수 신호: MFI < 20

 

## **화폐 흐름 지수 계산**

MFI를 계산하기 전에 대표 주가(typical price)를 먼저 계산하려고 합니다. 대표 주가는 주식 일봉 차트에서 3개의 값을 평균낸 가격을 나타냅니다. 즉, 최고가, 최저가, 그리고 종가의 평균 값을 의미합니다. 

> Typical price = (high + low + close)/3

다음으로, 대표 주가가 시간이 지남에 따라서 하락하면 음수가 되고, 반대로 시간이 지남에 따라서 상승하면 양수가 되도록 자금 흐름 지수(MFI)를 계산해 보겠습니다. MFI는 대표 주가에 볼륨을 곱하해서 구할 수 있습니다.

> Money flow (MF) = typical price X volume

위의 계산을 통해서 주어진 기간 내에 양의 자금 흐름과 음의 자금 흐름을 알 수 있습니다. 현재 대표 주가가 전날 대표 주가 보다 높은 모든 날은 전날 자금 흐름(money flow)을 양의 자금에 추가하고, 현재 대표 주가가 전날 대표 주가 보다 낮은 날은 자금 흐름(money flow)을 음의 자금 흐름에 추가합니다. 현재 대표 주가와 전날 대표주가가 동일(대표 주가에 변동이 없음)하다면, 해당 날짜의 양의 자금 흐름(money flow)과 음의 자금흐름을 모두 0으로 표시합니다.

> Money flow ratio (MFI) = positive money flow / negative money flow

마지막으로 자금 흐름 지수를 계산해 보겠습니다. 우리가 알고 싶은 것은 돈의 흐름에 대한 긍정적 또는 부정적 방향성 입니다. 아래에서 Money Flow Index (MFI)를 계산하는 두 가지 공식을 소개해 드리겠습니다.

> Equation 1: MFI = 100 - ( 100 / (1 + MFI) )
> Equation 2: 100 x (positive_money_flow / (positive_MF + negative_MF))

 

## **계산과정 요약**

1. 대표 주가(typical price)를 계산 
2. 돈의 흐름(money flow)을 계산 
3. 돈 흐름을 양수와 음수 흐름으로 나눕니다. 
4. 선택적으로 화폐 비율을 계산합니다. 
5. 자금 흐름 지수(money flow index)를 계산합니다.



![img](https://blog.kakaocdn.net/dn/bI70KC/btqRlInyfEA/zAktomMnkUCUjDxIMozMB1/img.png)MFI 계산공식 (출처: investopedia.com)



## **파이썬을 이용한 기술지표 계산**

파이썬을 이용해서 위에서 설명한 4가지 기술지표를 계산해 보겠습니다. 우선 분석이 필요한 라이브러리를 Import 하겠습니다.

```
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
```

이제 예시 데이터를 야후에서 다운로드 받오겠습니다. 2021년은 그린에너지의 해가 될 것으로 기대되고 있기 때문에, 전기차 배터리의 핵심 원료인 리튬을 생산하는 리튬아메리카(NYSE: LAC)의 최근 1년 데이터를 예제로 사용하겠습니다. 야후 파이낸스를 통해 데이터를 가져오겠습니다. 혹시 관련 라이브러리가 없는 분은 아래 명령어로 라이브러리를 설치해 주시기 바랍니다.

```
! pip install yfinance
```

### **주식 데이터 가져오기**

```
import yfinance as yf
df = yf.download('LAC', start="2019-12-01", end="2020-11-30")
df['Date'] = df.index
df.head()
```



![img](https://blog.kakaocdn.net/dn/es9MZI/btqRpsYlpUW/hAvHdXrkOxqTtxkkfwsBR1/img.png)



 

### **주식 차트 시각화**

```
plt.figure(figsize=(12.2, 4.5)) # width = 12.2in, height = 4.5
plt.plot( df['Close'],  label='Close Price')
plt.title('Close Price History')
plt.xlabel('Date',fontsize=18)
plt.ylabel('Close Price USD ($)',fontsize=18)
plt.legend(df.columns.values, loc='upper left')
plt.show()
```



![img](https://blog.kakaocdn.net/dn/uPP1m/btqRpuV9UQY/OkrgFQtu2zfvcafkKx0bj0/img.png)



 

### **대표 주가(typical price) 계산**

```
typical_price = (df['Close'] + df['High'] + df['Low']) / 3
typical_price
```



![img](https://blog.kakaocdn.net/dn/cbNPoj/btqRpuhyws9/GKzvdxx4UCPYnoaAXFX2wK/img.png)



### **자금 흐름(money flow) 계산**

```
money_flow = typical_price * df['Volume']
money_flow
```



![img](https://blog.kakaocdn.net/dn/cn0eGZ/btqRlIHUFUX/r48KwNfcod7kal4EmdS8Jk/img.png)



 

### **양의 자금 흐름과 음의 자금 흐름 계산**

```
positive_flow =[] 
negative_flow = [] 
for i in range(1, len(typical_price)):
  # 현재 대표 주가가 어제 대표주가보다 높을때
  if typical_price[i] > typical_price[i-1]: 
    positive_flow.append(money_flow[i-1]) 
    negative_flow.append(0)  # Append 0 to the negative flow list
  # 현재 대표 주가가 어제 대표주가보다 낮을때
  elif typical_price[i] < typical_price[i-1]:
    negative_flow.append(money_flow[i-1]) 
    positive_flow.append(0)  # Append 0 to the positive flow list
  # 대표 주가의 변동이 없을때
  else: 
    positive_flow.append(0)
    negative_flow.append(0)
```

 

### **지정된 기간 내 양의 자금 흐름과 음의 자금 흐름 계산**

```
period = 14

positive_mf =[]
negative_mf = [] 

# 기간내 모든 양의 자금흐름
for i in range(period-1, len(positive_flow)):
  positive_mf.append(sum(positive_flow[i+1-period : i+1]))

# 기간내 모든 음의 자금흐름 
for i in range(period-1, len(negative_flow)):
  negative_mf.append(sum(negative_flow[i+1-period : i+1]))
```

 

### **자금 흐름 지수(MFI) 계산**

```
mfi = 100 * (np.array(positive_mf) / (np.array(positive_mf)  + np.array(negative_mf) ))
mfi
```



![img](https://blog.kakaocdn.net/dn/PH5VI/btqRgiJ9TN6/RbDSwxk7qHQIanCOFh3Hak/img.png)



 

### **자금 흐름 지수(MFI) 시각화**

```
df2 = pd.DataFrame()
df2['MFI'] = mfi
# Create and plot the graph
plt.figure(figsize=(12.2,4.5)) 
plt.plot( df2['MFI'],  label='MFI')
plt.axhline(10, linestyle='--', color = 'orange')  # Over Sold line (매수)
plt.axhline(20, linestyle='--',color = 'blue')     # Over Sold Line (매수)
plt.axhline(80, linestyle='--', color = 'blue')    # Over Bought line (매도)
plt.axhline(90, linestyle='--', color = 'orange')  # Over Bought line (매도)
plt.title('MFI')
plt.ylabel('MFI Values',fontsize=18)
plt.legend(df2.columns.values, loc='upper left')
plt.show()
```



![img](https://blog.kakaocdn.net/dn/bWdQs5/btqRoQFaChf/gmVPbgMFYJcP9miA5Ktz1K/img.png)



 

###  **MFI 값을 DataFrame에 추가하기**

```
#Create a new data frame
new_df = pd.DataFrame()
new_df = df[period:]
new_df['MFI'] = mfi
new_df.tail()
```



![img](https://blog.kakaocdn.net/dn/bWkIGV/btqRjgEP5VD/TBC37rWcF2gzwenDuOZ6i1/img.png)



 

### **MFI를 이용해서 매수/매도 타이밍 찾는 함수 생성**

- 매도 타이밍: MFI > 80
- 매수 타이밍: MFI < 20

```
def get_signal(data, high, low):
  buy_signal = [] 
  sell_signal = [] 
  for i in range(len(data['MFI'])):
      if data['MFI'][i] > high: # 매도 타이밍 
        buy_signal.append(np.nan)
        sell_signal.append(data['Close'][i])
      elif data['MFI'][i] < low: # 매수 타이밍
        buy_signal.append(data['Close'][i])
        sell_signal.append(np.nan)
      else:
        buy_signal.append(np.nan)
        sell_signal.append(np.nan)
  return (buy_signal, sell_signal)
```

 

### **매수/매도 시점을 DataFrame에 추가하기**

```
buy_signal, sell_signal = get_signal(new_df, 80, 20)
new_df['Buy'] = buy_signal
new_df['Sell'] = sell_signal

# 결과 출력 (매수 또는 매도 신호에 NULL이 아닌 값이 있는 경우만 출력)
new_df.loc[new_df.Buy.notnull() | new_df.Sell.notnull()].head(10)
```



![img](https://blog.kakaocdn.net/dn/bX4wKh/btqRePIeKwZ/jnqyAKn6LyHcEIPgypUozK/img.png)



 

### **주식 데이터와 매수/매도 타이밍을 모두 시각화**

```
# plot the close price history
plt.figure(figsize=(12.2,4.5))
plt.plot(new_df.index, new_df['Close'],alpha = 0.5, label='Close Price')
plt.scatter(new_df.index, new_df['Buy'], color = 'green',
                    label='Oversold/ Buy Signal', marker = '^', alpha = 1)
plt.scatter(new_df.index, new_df['Sell'], color = 'red',
                    label='Overbought/ Sell Signal', marker = 'v', alpha = 1)
plt.title('Close Price')
plt.xlabel('Date',fontsize=18)
plt.xticks(rotation = 45)
plt.ylabel('Close Price USD ($)',fontsize=18)
plt.legend( loc='upper left')
plt.show()

# plot the corresponding MFI values and significant levels
plt.figure(figsize=(12.4,3.5))
plt.title('MFI Plot')
plt.plot(new_df.index, new_df['MFI'])
plt.axhline(10, linestyle='--',color = 'orange') #Buy
plt.axhline(20, linestyle='--', color = 'blue') #Sell
plt.axhline(80, linestyle='--', color = 'blue') #Sell
plt.axhline(90, linestyle='--', color = 'orange') #Sell
plt.xlabel('Date',fontsize=18)
plt.xticks(rotation = 45)
plt.ylabel('MFI Values (0 - 100)',fontsize=18)
plt.show()
```



![img](https://blog.kakaocdn.net/dn/ceL7yj/btqRePIeKu2/1mnUo3yQTB2EmBjeSCSLs0/img.png)

![img](https://blog.kakaocdn.net/dn/yWsBL/btqRjgdOM7J/YN8EmhO9zKE5BPCVkTAWlk/img.png)



위의 차트를 보면 빨간색으로 표시된 매도 신호와 녹색으로 표시된 매수 신호를 확인할 수 있습니다. 자금 흐름 지표에 따르면 2020년 3월 정도에 리튬아메키라 주식을 평균 주당 3-4달러 정도에 매수 해야 할것처럼 보입니다. 이후에 2020년 10월에 주당 평균 약 15달러에 매도 신호가 잡혔습니다. 그리고 이후에 2020년 11월에는 주당 약 10달러 정도에서 매수 타이밍 신호가 잡혔네요. MFI와 다른 지표들을 잘 활용해서 좋은 성과를 내시길 바랍니다.

참고) 이 글은 randerson112358의 Algorithmic Trading Strategy Using Money Flow Index (MFI) and Python를 각색하여 한글로 번역한 글입을 밝힙니다. 원문은 [링크](https://randerson112358.medium.com/algorithmic-trading-strategy-using-money-flow-index-mfi-python-aa46461a5ea5)를 통해서 확인하실 수 있습니다.