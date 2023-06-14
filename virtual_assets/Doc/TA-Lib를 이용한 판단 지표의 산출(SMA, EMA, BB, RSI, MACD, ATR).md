# TA-Lib를 이용한 판단 지표의 산출(SMA, EMA, BB, RSI, MACD, ATR)

출처: https://qiita.com/__x__/items/ed91e995aec21ac89c8b

# ■ 개요

TA-Lib를 이용한 판단 지표(SMA, EMA, BB, RSI, MACD, ATR)의 산출하여
mplfinance를 이용하여 표시시킨다

일련의 코드는↓



# ■ 환경

device : mac book air 2022
yfinance : 0.2.12 (출시일 : 2023.02.16)
mplffinance : 0.12.9b7
pandas : 1.3.5

# ■ 구현

## (1) 데이터 수집 및 촛불 발 표시

#### ● 데이터 수집

yfinance에서 비트 코인 데이터를 수집했습니다.
데이터에 대한 자세한 내용은 2022년 일족 데이터를 수집했습니다.

```py
!pip install yfinance
#yfinance 및 pandas 가져오기
import yfinance as yf
import pandas as pd

#검색할 데이터 세부정보
name = 'BTC-USD'
start = '2022-01-01'
end = '2022-12-31'

#데이터 다운로드
df = yf.download(tickers=name, start=start, end=end)
df.head(3)
```

| 날짜       | 열려 있는    | 높은         | 낮은         | 닫다         | 조정 닫기    | 용량        |
| :--------- | :----------- | :----------- | :----------- | :----------- | :----------- | :---------- |
| 2022-01-01 | 46311.746094 | 47827.312500 | 46288.484375 | 47686.812500 | 47686.812500 | 24582667004 |
| 2022-01-02 | 47680.925781 | 47881.406250 | 46856.937500 | 47345.218750 | 47345.218750 | 27951569547 |
| 2022-01-03 | 47343.542969 | 47510.726562 | 45835.964844 | 46458.117188 | 46458.117188 | 33071628362 |

yfinance에 대한 자세한 내용은 이 문서를 참조하세요.



#### ● 촛불 발 표시

```bash
!pip install mplfinance
import mplfinance as mpf

mpf.plot(df, type="candle", figratio = (4, 2), volume=True, style="yahoo")
```

[![mplfinance_1](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F1582644%2F19f513f0-b4d1-d681-c783-2d2d65532879.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=f9440206dc77e6a52d373039a5622d86)](https://camo.qiitausercontent.com/8c56321cf125e9a191be84591590fb12d04335b6/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313538323634342f31396635313366302d623464312d643638312d633738332d3264326436353533323837392e706e67)

mplfinance에 대한 자세한 내용은이 기사를 참조하십시오.



## (2) Ta-Lib 설치

```bash
!pip install TA-Lib
```

## ( 3 ) SMA(이동 평균)

#### ● SMA 계산

```py
import talib
import numpy as np

df['SMA20'] = talib.SMA(np.array(df['Close']), 20)
df['SMA50'] = talib.SMA(np.array(df['Close']), 50)
df['SMA100'] =  talib.SMA(np.array(df['Close']), 100)
df[['SMA20', 'SMA50', 'SMA100']].tail(3)
```

| 날짜       | SMA20        | SMA50        | SMA100       |
| :--------- | :----------- | :----------- | :----------- |
| 2022-12-29 | 16945.709570 | 16821.523574 | 18212.409941 |
| 2022-12-30 | 16919.402637 | 16801.839863 | 18192.961797 |
| 2022-12-31 | 16891.567773 | 16792.103926 | 18164.301250 |

#### ● SMA를 mplfinance를 사용하여 표시

```py
sma = [ mpf.make_addplot(df['SMA20'], color="red"),
        mpf.make_addplot(df['SMA50'], color="blue"),
        mpf.make_addplot(df['SMA100'], color="green")]

mpf.plot(df, type="candle", figratio = (4, 2), style="yahoo", addplot=sma)
```

[![mplfinance_1](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F1582644%2F7e737767-3880-41b3-e9ee-b1cbfff81523.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=fa642c991892785a603fd03a13e08d06)](https://camo.qiitausercontent.com/34a5f1a83bd50db3cf0e5f8391e262ebbb3e3747/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313538323634342f37653733373736372d333838302d343162332d653965652d6231636266666638313532332e706e67)

## ( 4 ) EMA(지수평활이동평균)

#### ● EMA 계산

```py
df['EMA20'] = talib.EMA(np.array(df['Close']), 20)
df['EMA50'] = talib.EMA(np.array(df['Close']), 50)
df['EMA100'] =  talib.EMA(np.array(df['Close']), 100)
df[['EMA20', 'EMA50', 'EMA100']].tail(3)
```

| 날짜       | EMA20        | EMA50        | EMA100       |
| :--------- | :----------- | :----------- | :----------- |
| 2022-12-29 | 16857.778948 | 17269.299841 | 18345.835924 |
| 2022-12-30 | 16833.474851 | 17243.154197 | 18311.316123 |
| 2022-12-31 | 16806.238779 | 17215.873488 | 18276.388993 |

#### ● EMA를 mplfinance를 사용하여 표시

```py
ema = [ mpf.make_addplot(df['EMA20'], color="red"),
        mpf.make_addplot(df['EMA50'], color="blue"),
        mpf.make_addplot(df['EMA100'], color="green")]

mpf.plot(df, type="candle", figratio = (4, 2), style="yahoo", addplot=ema)
```

[![mplfinance_1](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F1582644%2Fa2743b13-9e27-2c67-ed8c-09c82c972949.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=c5b1c0b4bf978ec651d1fd29d6466cad)](https://camo.qiitausercontent.com/2e96ea3a7a035f623502164efa736780e21c183a/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313538323634342f61323734336231332d396532372d326336372d656438632d3039633832633937323934392e706e67)

## ( 5 ) BB(볼린저 밴드)

#### ●BB를 산출한다

```python
bb_period = 10
sigma = 2
matype = 0

df['BB_up'], df['BB_middle'], df['BB_down'] = talib.BBANDS(np.array(df['Close']), bb_period, sigma, sigma, matype)
df[['BB_up', 'BB_middle', 'BB_down']].tail(3)
```

| 날짜       | 비비업       | BB_중간      | bb_down      |
| :--------- | :----------- | :----------- | :----------- |
| 2022-12-29 | 17008.412859 | 16787.276953 | 16566.141048 |
| 2022-12-30 | 16987.531515 | 16756.905078 | 16526.278641 |
| 2022-12-31 | 16987.470883 | 16729.901172 | 16472.331461 |

#### ●BB를 mplfinance를 사용해 표시시킨다

```python
bb = [ mpf.make_addplot(df['BB_up'], color="blue"),
        mpf.make_addplot(df['BB_middle'], color="red"),
        mpf.make_addplot(df['BB_down'], color="blue")]

mpf.plot(df, type="candle", figratio = (4, 2), style="yahoo", addplot=bb)
```

[![mplfinance_1](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F1582644%2F0f8e7170-9f11-1257-09c7-01cee95bf8ea.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=ec7d9109aac6ea94c8ea6f61d7aa2224)](https://camo.qiitausercontent.com/0a1ece7c0c8ef7bf384ab56a11c96eb65266af2f/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313538323634342f30663865373137302d396631312d313235372d303963372d3031636565393562663865612e706e67)

## (6) RSI(상대력 지수)

#### ● RSI 계산

```python
rsi_period = 14

df['RSI'] = talib.RSI(df['Close'])
df['RSI_SMA14'] = talib.SMA(np.array(df['RSI']), rsi_period)
df[['RSI', 'RSI_SMA14']].tail(3)
```

| 날짜       | RSI       | RSI_SMA14 |
| :--------- | :-------- | :-------- |
| 2022-12-29 | 44.125248 | 45.155021 |
| 2022-12-30 | 43.408369 | 45.219953 |
| 2022-12-31 | 42.380864 | 45.054581 |

#### ● RSI를 mplfinance를 사용하여 표시

```python
rsi = [ mpf.make_addplot(df['RSI'], color="purple",panel=1),
        mpf.make_addplot(df['RSI_SMA14'], color="green",panel=1)]

mpf.plot(df, type="candle", figratio = (4, 2), style="yahoo", addplot=rsi)
```

[![mplfinance_1](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F1582644%2Fc93790af-72bf-6d4c-c9fe-211fc787a48f.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=75a278238aa7848244d2ab28a5b15950)](https://camo.qiitausercontent.com/d016776c84b1a9e932689d64f5e0ca59611989ad/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313538323634342f63393337393061662d373262662d366434632d633966652d3231316663373837613438662e706e67)

## (7) MACD(이동 평균 수렴 확산 수법)

#### ●MACD를 산출한다

```python
fast_period = 12
slow_period = 26
signal_period = 9

df["MACD"], df["MACD_signal"], df["MACD_hist"] = talib.MACD(df['Close'], fast_period, slow_period, signal_period)
df[['MACD', 'MACD_signal', 'MACD_hist']].tail(3)
```

| 날짜       | MACD        | MACD_시그널 | MACD_hist  |
| :--------- | :---------- | :---------- | :--------- |
| 2022-12-29 | -125.238723 | -110.046230 | -15.192493 |
| 2022-12-30 | -130.839866 | -114.204957 | -16.634909 |
| 2022-12-31 | -138.131805 | -118.990327 | -19.141478 |

#### ●MACD를 mplfinance를 사용해 표시시킨다

```python
macd = [
    mpf.make_addplot(df["MACD"], color='blue', panel=1),
    mpf.make_addplot(df["MACD_signal"], color='red', panel=1),
    mpf.make_addplot(df["MACD_hist"],type='bar', panel=1)
]

mpf.plot(df, type="candle", figratio = (4, 2), style="yahoo", addplot=macd)
```

[![mplfinance_1](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F1582644%2F6e07371c-6100-9fb3-6dea-e50594326554.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=aa7eade86175c7204cb3203f0474a790)](https://camo.qiitausercontent.com/bffcec9bac6c1914410af6ac19b2da4626a66996/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313538323634342f36653037333731632d363130302d396662332d366465612d6535303539343332363535342e706e67)

## ( 8 ) ATR

#### ●ATR 산출

```python
atr_period = 3
df["ATR"] = talib.ATR(np.array(df['High']), np.array(df['Low']), np.array(df['Close']), timeperiod=atr_period)
df[['ATR']].tail(3)
```

| 날짜       | ATR        |
| :--------- | :--------- |
| 2022-12-29 | 197.939283 |
| 2022-12-30 | 210.277230 |
| 2022-12-31 | 177.340419 |

#### ● ATR을 mplfinance를 사용하여 표시

```python
atr = [mpf.make_addplot(df["ATR"], color='blue', panel=1)]

mpf.plot(df, type="candle", figratio = (4, 2), style="yahoo", addplot=atr)
```

[![mplfinance_1](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F1582644%2F5f41c11f-d4aa-11a6-422c-3cb5a0b1d992.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=f13874b359cfbaf7a34af620c7e2cf18)](https://camo.qiitausercontent.com/c422605fe299a749cb340702dbc6b95240422ae0/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313538323634342f35663431633131662d643461612d313161362d343232632d3363623561306231643939322e706e67)

# ■ 참고문헌



공유