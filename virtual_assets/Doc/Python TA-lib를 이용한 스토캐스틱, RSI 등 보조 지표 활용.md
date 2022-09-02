# Python TA-lib를 이용한 스토캐스틱, RSI 등 보조 지표 활용

출처: https://hichoco.tistory.com/entry/%EC%97%85%EB%B9%84%ED%8A%B8-API%EC%99%80-Python-TA-lib%EB%A5%BC-%EC%9D%B4%EC%9A%A9%ED%95%9C-%EC%8A%A4%ED%86%A0%EC%BA%90%EC%8A%A4%ED%8B%B1-RSI-%EB%93%B1-%EB%B3%B4%EC%A1%B0-%EC%A7%80%ED%91%9C-%ED%99%9C%EC%9A%A9



[이전 포스팅](https://blog.coinali.me/entry/업비트-API를-이용한-코인-RSI-알리미-프로그램)에서는 업비트 API를 통해 가져온 캔들 데이터를 pandas의 DataFrame으로 변환한 뒤, RSI 값을 생성해 알림 등에 활용하는 코드를 Python으로 작성해보았습니다.

 

이번에는 [RSI](https://en.wikipedia.org/wiki/Relative_strength_index) 뿐만 아니라 [MACD(Moving Average Convergence/Divergence)](https://en.wikipedia.org/wiki/MACD), [스토캐스틱(Stochastic)](https://en.wikipedia.org/wiki/Stochastic_oscillator), [ADX(Average Directional Movement Index)](https://en.wikipedia.org/wiki/Average_directional_movement_index) 등등 다양한 보조 지표를 쉽게 생성할 수 있도록 도와주는 TA-lib를 사용하는 코드를 파이썬으로 작성해보도록 하겠습니다.

------

먼저 [Python TA-Lib](https://github.com/mrjbq7/ta-lib)를 설치해야 합니다. 참고로 Python TA-Lib는 [TA-Lib](https://ta-lib.org/)의 Wrapper이므로 먼저 TA-Lib가 깔려 있어야 합니다 (Python TA-Lib의 문서에 나와 있는 것처럼 사용 중인 운영체제에 따라 TA-Lib 설치 방법은 다를 수 있습니다.)

```
pip install TA-Lib
```

 

설치가 완료되었다면, RSI를 계산하는 법은 간단합니다.

```
import talib as ta

ta.RSI(df['close'], timeperiod=14)
```

(df 변수는 [이전 포스팅](https://blog.coinali.me/entry/업비트-API를-이용한-코인-RSI-알리미-프로그램)에서 작성한 업비트 캔들 데이터를 pandas.DataFrame으로 바꾼 데이터를 담고 있습니다.)

 

 

Python TA-Lib는 정말 다양한 보조 지표를 쉽게 계산할 수 있도록 다음과 같은 함수 목록을 제공하고 있습니다.

```
ADX                  Average Directional Movement Index
ADXR                 Average Directional Movement Index Rating
APO                  Absolute Price Oscillator
AROON                Aroon
AROONOSC             Aroon Oscillator
BOP                  Balance Of Power
CCI                  Commodity Channel Index
CMO                  Chande Momentum Oscillator
DX                   Directional Movement Index
MACD                 Moving Average Convergence/Divergence
MACDEXT              MACD with controllable MA type
MACDFIX              Moving Average Convergence/Divergence Fix 12/26
MFI                  Money Flow Index
MINUS_DI             Minus Directional Indicator
MINUS_DM             Minus Directional Movement
MOM                  Momentum
PLUS_DI              Plus Directional Indicator
PLUS_DM              Plus Directional Movement
PPO                  Percentage Price Oscillator
ROC                  Rate of change : ((price/prevPrice)-1)*100
ROCP                 Rate of change Percentage: (price-prevPrice)/prevPrice
ROCR                 Rate of change ratio: (price/prevPrice)
ROCR100              Rate of change ratio 100 scale: (price/prevPrice)*100
RSI                  Relative Strength Index
STOCH                Stochastic
STOCHF               Stochastic Fast
STOCHRSI             Stochastic Relative Strength Index
TRIX                 1-day Rate-Of-Change (ROC) of a Triple Smooth EMA
ULTOSC               Ultimate Oscillator
WILLR                Williams' %R
```

 

다음은 STOCH, MACD, ADX 등을 구하는 예시입니다.

```
# Stochastic
ta.STOCH(high=df['high'], low=df['low'], close=df['close'],
         fastk_period=3, slowk_period=1, slowd_period=1)

# MACD
ta.MACD(real=df['close'], fastperiod=12, slowperiod=26, signalperiod=9)

# ADX
ta.ADX(high=df['high'], low=df['low'], close=df['close'], timeperiod=14)
```

 

TA-Lib는 이러한 모멘텀 인디케이터 외에도 이동평균선, 볼린저 밴드, 파라볼릭 SAR 등등 다양한 지표들을 쉽게 계산할 수 있도록 도와줍니다. 이외에도 망치(Hammer), 도지(Doji) 등등 다양한 캔들 패턴 인식을 위한 방법도 제공하고 있는데, 이는 다음 포스팅에서 다루도록 하겠습니다.