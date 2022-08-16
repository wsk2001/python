# 현대 거래 기법 — Python의 반전 전략.

출처: https://medium.com/geekculture/modern-trading-techniques-a-reversal-strategy-in-python-474e8b7d5a36

RSI와 확률론을 사용하여 이중 반전 전략 만들기.

이 기사에서는 두 가지 방법과 두 가지 지표를 기반으로 한 흥미로운 전략에 대해 설명합니다. 목표는 중장기적으로 사용되는 반전 신호를 찾는 것입니다.

나는 나의 이전 책 '무역 전략의 책'의 성공 이후에 새로운 책을 출판했습니다. 지속적으로 업데이트되는 코드 전용 GitHub 페이지와 함께 고급 추세 추종 지표 및 전략을 제공합니다. 또한 이 책은 인쇄비에 최적화된 원색을 그대로 담고 있습니다. 관심이 있는 경우 아래 Amazon 링크를 방문하거나 PDF 버전을 구매하려는 경우 LinkedIn에서 저에게 연락하십시오.



**상대 강도 지수( Relative Strength Index)**

J. Welles Wilder Jr.가 처음 도입한 RSI는 가장 인기 있고 다양한 기술 지표 중 하나입니다. 극단값이 악용될 수 있는 반응을 나타내는 역방향 지표로 주로 사용됩니다. 일반적으로 다음 단계를 사용하여 기본 RSI를 계산합니다.

- 이전 가격에서 종가의 변화를 계산합니다.
- 양의 순 변화를 음의 순 변화와 분리하십시오.
- 양의 순 변화와 음의 순 변화의 절대값에 대한 평활 이동 평균을 계산합니다.
- 평활화된 양수 변화를 평활화된 음수 변화로 나눕니다. 이 계산을 상대 강도 - RS라고 합니다.
- RSI를 얻으려면 모든 시간 단계에 대해 아래에 표시된 정규화 공식을 적용하십시오.


![img](.\images\tnORUZCGx4CoQLE0.png)

![img](.\images\43-o8AYYi08vt2J7.png)

**첫 번째 패널의 GBPUSD, 두 번째 패널의 13기간 RSI.**

위 차트는 13기간 RSI와 함께 검은색 GBPUSD의 시간당 가치를 보여줍니다. 우리는 일반적으로 RSI가 25 근처에서 튀는 경향이 있는 반면 75 부근에서 일시 중지되는 경향이 있음을 알 수 있습니다. Python에서 RSI를 코딩하려면 시가, 고가, 저가 및 종가를 포함하는 4개의 열로 구성된 OHLC 배열이 필요합니다.

``` py
def adder(data, times):
    
    for i in range(1, times + 1):
    
        new = np.zeros((len(data), 1), dtype = float)
        
        data = np.append(data, new, axis = 1)    
    return data
def deleter(data, index, times):
    
    for i in range(1, times + 1):
    
        data = np.delete(data, index, axis = 1)    
    return data
   
def jump(data, jump):
    
    data = data[jump:, ]
    
    return data
def ma(data, lookback, close, where): 
    
    data = adder(data, 1)
    
    for i in range(len(data)):
           
            try:
                
                data[i, where] = (data[i - lookback + 1:i + 1, close].mean())
            
            except IndexError:
                
                pass
            
    data = jump(data, lookback)
    
    return data
def ema(data, alpha, lookback, what, where):
    
    alpha = alpha / (lookback + 1.0)
    
    beta  = 1 - alpha
    
    data = ma(data, lookback, what, where)
    data[lookback + 1, where] = (data[lookback + 1, what] * alpha) + (data[lookback, where] * beta)
    for i in range(lookback + 2, len(data)):
        
            try:
                
                data[i, where] = (data[i, what] * alpha) + (data[i - 1, where] * beta)
        
            except IndexError:
                
                pass
            
    return data
def rsi(data, lookback, close, where):
    
    data = adder(data, 5)
    
    for i in range(len(data)):
        
        data[i, where] = data[i, close] - data[i - 1, close]
     
    for i in range(len(data)):
        
        if data[i, where] > 0:
            
            data[i, where + 1] = data[i, where]
            
        elif data[i, where] < 0:
            
            data[i, where + 2] = abs(data[i, where])
            
    lookback = (lookback * 2) - 1 # From exponential to smoothed
    data = ema(data, 2, lookback, where + 1, where + 3)
    data = ema(data, 2, lookback, where + 2, where + 4)    
    data[:, where + 5] = data[:, where + 3] / data[:, where + 4]
    
    data[:, where + 6] = (100 - (100 / (1 + data[:, where + 5])))    
    data = deleter(data, where, 6)
    data = jump(data, lookback)     
    return data
```



더 많은 기사를 보고 싶다면 아래 링크를 통해 내 DAILY 뉴스레터(무료 요금제 사용 가능) 구독을 고려하십시오. 그것은 내 Medium 기사, 더 많은 거래 전략, 연구 및 분석과 관련된 코딩 수업을 제공하며 구독자는 내 첫 번째 책의 무료 PDF 사본을 받습니다. 유료 구독에서는 주당 5
7개의 기사를, 무료 플랜에서는 주당 1
2개의 기사를 기대할 수 있습니다. 이것은 내가 연구를 계속 공유하는 데 도움이 될 것입니다. 고맙습니다!



**스토캐스틱 오실레이터(The Stochastic Oscillator)**

스토캐스틱 오실레이터는 아래와 같은 정규화 공식을 사용하여 고점과 저점을 통합하여 과매수 및 과매수 영역을 찾습니다.

![img](.\images\tAc6vbBF4Un0Brxh.png)

과매수 수준은 시장이 매우 낙관적이며 통합될 것으로 인식되는 영역입니다. 과매도 수준은 시장이 극단적으로 약세라고 인식되고 반등할 수밖에 없는 영역입니다. 따라서 스토캐스틱 오실레이터는 극단적인 움직임의 반응 신호를 찾는 반대 지표입니다. OHLC 데이터에 대한 확률을 계산하는 아래 함수를 생성합니다.

``` py
def stochastic_oscillator(data, 
                             lookback, 
                             high, 
                             low, 
                             close, 
                             where, 
                             slowing = False, 
                             smoothing = False, 
                             slowing_period = 1, 
                             smoothing_period = 1):
            
    data = adder(data, 1)
        
    for i in range(len(data)):
            
        try:
            
            data[i, where] = (data[i, close] - min(data[i - lookback + 1:i + 1, low])) / (max(data[i - lookback + 1:i + 1, high]) - min(data[i - lookback + 1:i + 1, low]))
            
        except ValueError:
            
            pass
        
    data[:, where] = data[:, where] * 100  
            
    if slowing == True and smoothing == False:        
        data = ma(data, slowing_period, where, where + 1)
    
    if smoothing == True and slowing == False:        
        data = ma(data, smoothing_period, where, where + 1)
        
    if smoothing == True and slowing == True:
        data = ma(data, slowing_period, where,   where + 1)
        data = ma(data, smoothing_period, where, where + 2)        
       
    data = jump(data, lookback)    
    return data
```

![img](.\images\ZhSZp3V--1mbLIix.png)

**14주기 스토캐스틱 오실레이터가 있는 첫 번째 패널의 EURUSD 시간별 데이터.**

``` py
my_data = stochastic_oscillator(my_data, 
                             100, 
                             1, 
                             2, 
                             3, 
                             5, 
                             slowing = True, 
                             smoothing = False, 
                             slowing_period = 3, 
                             smoothing_period = 1)
# my_data must be an OHLC array with four columns composed of open, high, low, and close prices
```

더 많은 기술적 지표와 전략에 관심이 있다면 내 책도 관심을 가질 것입니다.



**전략 만들기**

이 전략에는 드문 신호가 있지만 일반적으로 일반 바닐라 지표보다 품질이 높습니다. 우리는 13일 RSI에서 정상적인 다이버전스를 찾을 것이며 100일 스토캐스틱 오실레이터는 극단적인 수준 근처에 있을 것입니다. 세부정보는 다음과 같습니다.

- RSI가 방금 강세 다이버전스를 확인한 동안 100일 스토캐스틱 오실레이터가 20 미만일 때마다 매수(매수).
- 100주기 스토캐스틱 오실레이터가 80을 넘고 RSI가 하락 다이버전스를 확인할 때마다 매도(매도)합니다.

당연히 가격이 상승하고 새로운 고점을 만들 때 가격 기반 지표가 고점을 낮추면 약세가 발생하고 편향을 롱에서 숏으로 변경할 가능성이 나타날 수 있습니다. 그것이 우리가 정상 발산이라고 부르는 것입니다. 우리는 다음을 알고 있습니다.

- 지표가 더 낮은 고점을 만드는 동안 가격이 더 높은 고점을 만들 때 이를 약세 다이버전스라고 하며 시장이 정체될 수 있습니다.
- 지표가 더 높은 저점을 만드는 동안 가격이 더 낮은 저점을 만들 때 이를 강세 다이버전스라고 하며 시장은 약간의 상승 잠재력을 보일 수 있습니다.


![img](D:\GitHub\python\virtual_assets\Doc\images\nJoOY0FYtBOtFFrDdzNU4A.png)

**Signal chart.**

``` py
def divergence(Data, indicator, lower_barrier, upper_barrier, width, buy, sell):
    Data = adder(Data, 2)
    for i in range(len(Data)):
        try:
            if Data[i, indicator] < lower_barrier:
                for a in range(i + 1, i + width):
                    # First trough
                    if Data[a, indicator] > lower_barrier:
                        for r in range(a + 1, a + width):
                            if Data[r, indicator] < lower_barrier and \
                            Data[r, indicator] > Data[i, indicator] and Data[r, 3] < Data[i, 3]:
                                for s in range(r + 1, r + width):
                                    # Second trough
                                    if Data[s, indicator] > lower_barrier:
                                        Data[s, buy] = 1
                                        break
                                    else:
                                        break
                            else:
                                break
                        else:
                            break
                    else:
                        break
        except IndexError:
            pass
    for i in range(len(Data)):
        try:
            if Data[i, indicator] > upper_barrier:
                for a in range(i + 1, i + width):
                    # First trough
                    if Data[a, indicator] < upper_barrier:
                        for r in range(a + 1, a + width):
                            if Data[r, indicator] > upper_barrier and \
                            Data[r, indicator] < Data[i, indicator] and Data[r, 3] > Data[i, 3]:
                                for s in range(r + 1, r + width):
                                    # Second trough
                                    if Data[s, indicator] < upper_barrier:
                                        Data[s, sell] = -1
                                        break
                                    else:
                                        break
                            else:
                                break
                        else:
                            break
                    else:
                        break
        except IndexError:
            pass 
    return Data
```

신호 차트는 스토캐스틱 오실레이터가 극단적인 판독값을 보여주는 동안 다이버전스가 검증되는 순간을 보여줍니다.


![img](D:\GitHub\python\virtual_assets\Doc\images\wTXp94tZnGUYqQUMwgBcCw.png)

**Signal chart.**



``` python
def signal(data, stochastic_column, bull_divergence, column, bear_divergence, buy, sell):
    data = adder(data, 5)

for i in range(len(data)):
        
        if data[i, bull_divergence] == 1 and data[i, stochastic_column] < 20:           
            data[i, buy] = 1
            
        if data[i, bear_divergence] == -1 and data[i, stochastic_column] > 80:
            data[i, sell] = -1       
            
    return data
```



![img](D:\GitHub\python\virtual_assets\Doc\images\dYPiRAJrN_WgWKuAo3F75A.png)

**Signal chart.**



### Conclusion

항상 백 테스트를 수행하는 것을 잊지 마십시오. 항상 다른 사람들이 틀렸다고 믿어야 합니다. 내 지표와 거래 스타일이 나에게는 효과가 있을 수 있지만 귀하에게는 그렇지 않을 수도 있습니다.

나는 숟가락으로 먹이지 않는다는 확고한 신념을 가지고 있습니다. 나는 베껴서가 아니라 행함으로써 배웠다. 아이디어, 기능, 직관, 전략 조건을 파악한 다음 이를 백테스트하고 개선할 수 있도록 스스로 정교화(더 나은)해야 합니다. 특정 백 테스팅 결과를 제공하지 않기로 한 내 선택은 독자가 전략을 더 스스로 탐색하고 더 많이 작업하도록 유도해야 합니다.

매체는 많은 흥미로운 읽을거리의 허브입니다. 글을 쓰기로 결정하기 전에 많은 기사를 읽었습니다. 내 추천 링크를 사용하여 Medium에 가입하는 것을 고려하십시오!

요약하자면, 내가 제공하는 전략이 현실적입니까? 예, 하지만 환경을 최적화해야 합니다(강력한 알고리즘, 저렴한 비용, 정직한 중개인, 적절한 위험 관리 및 주문 관리). 전략은 오직 거래만을 위한 것입니까? 아니오, 과매도된 RSI에 대해 매도의 이유로 또는 저항을 초과하는 매수를 매수하는 이유로 지겹도록 브레인스토밍을 자극하고 더 많은 거래 아이디어를 얻으려는 것입니다. 저는 객관적인 기술 분석이라는 새로운 분야를 소개하려고 합니다. 여기서 우리는 구식의 고전적인 방법에 의존하기 보다는 하드 데이터를 사용하여 기술을 판단합니다.

