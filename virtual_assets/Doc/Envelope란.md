# Envelope란?

https://kpumangyou.tistory.com/94



n일의 이동평균선에 +m%,-m%를 뜻한다.

 

### 분석 내용

보통 20일 이동평균선을 사용하고 m은 트레이더의 성향에 따라 많이 다르나 가장 보편적으로 사용되는 10으로 두고 분석해보겠다.

하향 envelope선에 돌파 또는 지지할시 매수 하고 m%만큼 떨어지면 손절, m%만큼 상승하면 익절하도록 세팅해 두었다.

 

 

####  코드

```python
!pip install yfinance
import pandas as pd
import matplotlib.pyplot as plt
import bs4
import yfinance as yf
from urllib.request import urlopen # url의 소스코드를 긁어오는 기능
```

필요한 라이브러리들을 불러와 줬다.

 

```python
# 종목코드 불러오기
stock_code = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0]
stock_code = stock_code[['회사명','종목코드']]
# rename(columns = {'원래 이름' : '바꿀 이름'}) 칼럼 이름 바꾸기
stock_code = stock_code.rename(columns = {'회사명':'company','종목코드':'code'})
# 종목코드가 6자리이기 때문에 6자리를 맞춰주기 위해 설정해줌 
stock_code.code = stock_code.code.map('{:06d}'.format) #6자리가 아닌 수를 앞에 0으로 채우기 위함
stock_code.tail(3)
```

상장된 기업정보들을 크롤링 해주었다.

 

```python
# 코스피 200 종목의 이름을 웹 크롤링함
import bs4
from urllib.request import urlopen # url의 소스코드를 긁어오는 기능
#//*[@id="tab_con1"]/div[3]/table/tbody/tr[1]/td/span[1]/em
company_name = []
for i in range(1,21):
  page = i
  url = 'https://finance.naver.com/sise/entryJongmok.nhn?&page={page}'.format(page = page)
  source = urlopen(url).read()
  source = bs4.BeautifulSoup(source,'lxml')
  source = source.find_all('a',target = '_parent')
  for j in range(len(source)):
    name = source[j].text
    company_name.append(name)
```

네이버 금융에서 코스피 200종목들의 이름을 크롤링 하였다. 크롤링하는 방법은 블로그 글에 자세하게 나와있다.

```python
code = []
for i in company_name:
  for j in range(len(stock_code)):
    if stock_code['company'][j] == i:
      code.append(stock_code['code'][j])
      break
code
```

코스피 200종목들의 종목코드들을 불러왔다.

```python
def envelope(N,ma): #엔벨로프 설정 함수 
  idx = ma.index
  plus = {}
  minus = {}
  for i in range(len(ma)):
    plus[idx[i]] = ma[i]+((ma[i]*N)/100)
    minus[idx[i]] = ma[i]-((ma[i]*N)/100)
  return plus,minus
```

ma 이동평균선만큼 N의 엔벨로프선을 만드는 함수이다.

 

#### 벡테스팅 함수

```python
# 벡테스팅 함수
import yfinance as yf
import matplotlib.pyplot as plt
def buy(price,cash,finance,Average_price):
  finance = cash/price
  Average_price  = price
  cash = cash%price
  return cash,finance,Average_price
def sell(price,cash,finance,Average_price):
  cash = finance*price+cash
  finance = 0
  Average_price = 0
  return cash,finance,Average_price
def backtesting(code,cash,N,min_percent):
  start_cash = cash
  finance = 0
  Average_price = 0
  data = yf.download(code)
  ma20 = data['Adj Close'].rolling(window = 20).mean()
  ma60 = data['Adj Close'].rolling(window = 60).mean()
  ma112 = data['Adj Close'].rolling(window = 112).mean()
  marker_buy = []
  marker_sell = []
  marker = []
  plus,minus = envelope(N,ma20)
  plus = pd.Series(plus)
  minus = pd.Series(minus)
  for i in range(1,len(data)):
    if data['Adj Close'][i-1]>minus[i-1] and data['Adj Close'][i]<=minus[i]:
      if finance == 0:
        cash,finance,Average_price = buy(data['Adj Close'][i],cash,finance,Average_price)
        line = []
        line.append(data.index[i])
        line.append(i)
        marker.append(line)
    if finance != 0 and Average_price+((Average_price*N)/100) <= data['Adj Close'][i]:
      cash,finance,Average_price = sell(data['Adj Close'][i],cash,finance,Average_price)
      line = []
      line.append(data.index[i])
      line.append(i)
      marker.append(line)
      print(cash)
    elif finance != 0 and Average_price-((Average_price*min_percent)/100)>=data['Adj Close'][i]:
      cash,finance,Average_price = sell(data['Adj Close'][i],cash,finance,Average_price)
      line = []
      line.append(data.index[i])
      line.append(i)
      marker.append(line)
      print(cash)
  '''
  fig = plt.figure(figsize = (50,20))
  fig = plt.plot(data['Adj Close'])
  fig = plt.plot(minus)
  fig = plt.plot(plus)
  win = 0
  lose = 0
  for i in range(0,len(marker)-1,2):
    start = marker[i]
    end = marker[i+1]
    if data['Adj Close'][start[1]]<data['Adj Close'][end[1]]:
      fig = plt.axvspan(start[0],end[0],color = 'blue',alpha = 0.1)
      win = win+1
    else:
      fig = plt.axvspan(start[0],end[0],color = 'red',alpha = 0.1)
      lose = lose+1
  plt.legend() 
  print(win,lose)
  '''
  print('백테스팅 총 수익률:',round(((cash-start_cash+(finance*data['Adj Close'][len(data)-1]))/start_cash)*100,2),'%')
  print('잔고:',round(cash+(finance*data['Adj Close'][len(data)-1]),2),'원')
  print('종목코드:',code)
  return round(((cash-start_cash+(finance*data['Adj Close'][-1]))/start_cash)*100)
```

주석 부분은 그래프가 그려지는 부분이다.

 

## 결과

-89, -86, -80, -79, -79, -79, -78, -77, -66, -65, -62, -61, -60, -59, -59, -58, -55, -49, -47, -44, -42, -41, -41, -38, -37, -34, -33, -33, -31, -31, -31, -30, -29, -28, -28, -23, -22, -22, -22, -21, -21, -20, -17, -17, -16, -16, -15, -15, -15, -14, -13, -12, -12, -11, -10, -9, -7, -6, -6, -6, -4, -3, -1, 0, 0, 0, 0, 1, 1, 1, 2, 2, 4, 5, 6, 6, 7, 8, 9, 9, 10, 14, 15, 15, 16, 17, 18, 18, 19, 22, 23, 26, 26, 26, 26, 29, 29, 30, 30, 31, 31, 32, 35, 36, 40, 40, 42, 43, 45, 46, 47, 47, 47, 48, 49, 50, 53, 55, 56, 57, 57, 58, 62, 64, 66, 70, 73, 82, 84, 92, 93, 93, 96, 97, 102, 103, 105, 105, 106, 107, 115, 115, 117, 123, 135, 147, 150, 152, 160, 174, 183, 188, 190, 190, 193, 195, 214, 215, 217, 237, 247, 250, 258, 264, 272, 281, 297, 304, 324, 335, 355, 374, 398, 438, 440, 472, 523, 532, 577, 624, 698, 1209, 1240,

 

수익 : 37

손실 : 63

결과가 너무 안좋았다. 하지만 분석중에 알아낸 사실이 하나 있었다. envelope를 거래량이 많은 상태에서 돌파하게 된다면 대부분 손실을 본다는 사실이었다. 하지만 거래량이 터지지 않고 하향돌파하면 곧바로 반등이 나오거나 일주일이내에 수익이 나오는것을 알 수 있었다. 다음 포스팅에서는 이번에 분석한 것을 반영해서 포스팅 해보겠다.

 



### 분석내용

envelope선을 기준으로 envelope 하향선을 돌파시 매수, 매수를 할시에는 3분할로 분할 매수를 하였다.

손절은 평단가의 5%로 잡고 손절하였고 익절은 envelope 상향선 돌파 또는 평단가의 5%에 도달시 익절을 하였다.

분석에 사용된 차트는 업비트 모든 종목을 대상으로 하였고 1시간 차트를 사용하였다. 기간은 1000시간으로 대략 41일동안에 트레이딩을 백테스팅하였다.

 

#### 분석 결과

아래 보이는 결과가 수익률이다. 보다시피 손해를 본 코인이 단 하나도 없었다. 하지만 근 한달간은 코인시장이 상승장이라는 것을 감안하면 어느정도 이해가 된다. 그래도 모든 종목이 수익을 본 것은 그래도 나쁘지 않은 전략이라고 생각한다. 이 매매전략을 더 업그레이드해서 실전 매매로 해봐도 좋을 것 같다는 생각을 했다. 

22.36 % 20.64 % 11.81 % 25.98 % 6.9 % 10.99 % 12.13 % 86.31 % 27.04 % 73.26 % 21.8 % 23.82 % 49.61 % 59.15 % 17.86 % 31.49 % 80.0 % 32.22 % 42.09 % 26.16 % 14.51 % 22.64 % 57.14 % 32.42 % 123.52 % 22.8 % 21.18 % 28.7 % 11.62 % 30.47 % 27.69 % 34.21 % 46.65 % 1.76 % 19.71 % 29.53 % 80.35 % 50.92 % 65.01 % 43.31 % 56.15 % 60.3 % 28.81 % 22.87 % 51.58 % 36.74 % 20.37 % 22.89 % 133.75 % 13.15 % 16.84 % 42.98 % 40.83 % 22.03 % 17.23 % 34.51 % 134.8 % 57.72 % 16.89 % 44.28 % 14.46 % 72.45 % 19.14 % 28.44 % 169.49 % 45.48 % 42.45 % 21.83 % 40.73 % 57.96 % 70.18 % 26.06 % 44.98 % 37.54 % 72.34 % 73.36 % 26.12 % 15.42 % 33.76 % 8.32 % 30.45 % 51.29 % 31.15 % 101.24 % 48.84 % 40.22 % 21.11 % 24.11 % 37.8 % 39.7 % 88.29 % 77.15 % 24.56 % 16.11 % 5.19 % 28.15 % 34.55 % 31.6 % 24.93 % 85.47 % 44.47 % 53.45 %

 

#### 코드

```python
import pyupbit
import pandas as pd
import matplotlib.pyplot as plt
```

필요한 라이브러리를 불러왔다.



```python
def draw_graph(list1,list_buy,list_sell,data):
  fig = plt.figure(figsize = (20,5))
  for i in range(len(list1)):
    fig = plt.plot(list1[i])
  for i in range(len(list_buy)):
    fig = plt.axvspan(list_buy[i][0],list_buy[i][0],color = 'blue',alpha = 0.1)
  for i in range(len(list_sell)):
    fig = plt.axvspan(list_sell[i][0],list_sell[i][0],color = 'red',alpha = 0.1)
  fig = plt.legend()
  fig = plt.show()
  fig2 = plt.figure(figsize = (20,2))
  fig2 = plt.plot(data['volume'])
```

매수,매도 타이밍을 보기 위해서 그래프를 그리는 함수를 만들었다.



```python
def set_envelop(data,gap):
  ma20 = data['close'].rolling(window = 20).mean()
  idx = ma20.index
  en_high,en_low =  [],[]
  for i in range(len(ma20)):
    en_high.append(ma20[i]+((ma20[i]*gap)/100))
    en_low.append(ma20[i]-((ma20[i]*gap)/100))
  en_high = pd.Series(en_high,index = idx)
  en_low = pd.Series(en_low,index  = idx)
  return en_high,en_low
```

data에 코인 차트데이터를 주고 gap에는 몇%의 envelope를 설정할 지 설정해주면 된다.



```python
# 벡테스팅 함수
def buy(price,cash,finance,Average_price,div_count):
  div_count = div_count + 1
  buy_cash = cash/3
  Average_price = ((Average_price*finance)+(price*buy_cash/price))/(finance+buy_cash/price)
  finance = finance+buy_cash/price
  cash = cash-buy_cash
  return cash,finance,Average_price,div_count

def sell(price,cash,finance,Average_price,div_count):
  cash = finance*price+cash
  finance = 0
  Average_price = 0
  div_count = 0
  return cash,finance,Average_price,div_count

def backtesting(data):
  start_cash = 10000000
  cash,finance,Average_price = start_cash,0,0
  div_count = 0
  list_buy,list_sell = [],[]
  en_high,en_low = set_envelop(data,3)
  for i in range(1,len(data)):
    if div_count < 3:
      if data['close'][i-1]>en_low[i-1] and data['close'][i]<=en_low[i]:
        cash,finance,Average_price,div_count = buy(en_low[i],cash,finance,Average_price,div_count)
        line = []
        line.append(data.index[i])
        line.append(i)
        list_buy.append(line)
    else:
      if data['close'][i-1]<en_high[i-1] and data['close'][i]>=en_high[i]:
        cash,finance,Average_price,div_count = sell(en_high[i],cash,finance,Average_price,div_count)
        line  = []
        line.append(data.index[i])
        line.append(i)
        list_sell.append(line)
      elif data['close'][i]+Average_price*5/100>=Average_price:
        cash,finance,Average_price,div_count = sell(en_high[i],cash,finance,Average_price,div_count)
        line  = []
        line.append(data.index[i])
        line.append(i)
        list_sell.append(line)
      elif data['close'][i]+Average_price*5/100<=Average_price:
        cash,finance,Average_price,div_count = sell(en_high[i],cash,finance,Average_price,div_count)
        line  = []
        line.append(data.index[i])
        line.append(i)
        list_sell.append(line)
  """
  list1 = []
  list1.append(en_high)
  list1.append(en_low)
  list1.append(data['close'])
  draw_graph(list1,list_buy,list_sell,data)
  """
  print('백테스팅 총 수익률:',round(((cash-start_cash+(finance*data['close'][len(data)-1]))/start_cash)*100,2),'%')
  return round(((cash-start_cash+(finance*data['close'][len(data)-1]))/start_cash)*100,2)
```

벡테스팅을 하는 함수이다. 매매전략을 추가 할 수도 있다.



```python
result = []
for i in range(len(code_name)):
  line = []
  name = code_name[i]
  data = pyupbit.get_ohlcv(name,interval="minute60",count = 1000)
  backtesting_result = backtesting(data)
  line.append(name)
  line.append(backtesting_result)
  result.append(line)
```

모든 코인에 대하여 백테스팅을 하고 리스트에 저장하였다.



