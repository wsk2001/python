# Ta-Lib 함수 모음

출처: https://blog.naver.com/PostView.nhn?blogId=tamiel&logNo=221900701118&parentCategoryNo=11&categoryNo=&viewDate=&isShowPopularPosts=false&from=postView



### Overlap Studies Functions

**BBANDS** - Bollinger Bands

``` py
upperband, middleband, lowerband = BBANDS(close, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
```



**DEMA** - Double Exponential Moving Average

``` python
real = DEMA(close, timeperiod=30)
```



**EMA** - Exponential Moving Average

``` python
real = EMA(close, timeperiod=30)
```



**HT_TRENDLINE** - Hilbert Transform - Instantaneous Trendline

``` python
real = HT_TRENDLINE(close)
```



**KAMA** - Kaufman Adaptive Moving Average

``` python
real = KAMA(close, timeperiod=30)
```



**MA** - Moving average

``` python
real = MA(close, timeperiod=30, matype=0)
```



**MAMA** - MESA Adaptive Moving Average

``` python
mama, fama = MAMA(close, fastlimit=0, slowlimit=0)
```



**MAVP** - Moving average with variable period

``` python
real = MAVP(close, periods, minperiod=2, maxperiod=30, matype=0)
```



**MIDPOINT** - MidPoint over period

``` python
real = MIDPOINT(close, timeperiod=14)
```



**MIDPRICE** - Midpoint Price over period

``` python
real = MIDPRICE(high, low, timeperiod=14)
```



**SAR** - Parabolic SAR

``` python
real = SAR(high, low, acceleration=0, maximum=0)
```



**SAREXT** - Parabolic SAR - Extended

``` python
real = SAREXT(high, low, startvalue=0, offsetonreverse=0, accelerationinitlong=0, accelerationlong=0, accelerationmaxlong=0, accelerationinitshort=0, accelerationshort=0, accelerationmaxshort=0)
```



**SMA** - Simple Moving Average

``` python
real = SMA(close, timeperiod=30)
```



**T3** - Triple Exponential Moving Average (T3)

``` python
real = T3(close, timeperiod=5, vfactor=0)
```



**TEMA** - Triple Exponential Moving Average

``` python
real = TEMA(close, timeperiod=30)
```



**TRIMA** - Triangular Moving Average

``` python
real = TRIMA(close, timeperiod=30)
```



**WMA** - Weighted Moving Average

``` python
real = WMA(close, timeperiod=30)
```



### Momentum Indicator Functions

**ADX** - Average Directional Movement Index

``` python
real = ADX(high, low, close, timeperiod=14)
```



**ADXR** - Average Directional Movement Index Rating

``` python
real = ADXR(high, low, close, timeperiod=14)
```



**APO** - Absolute Price Oscillator

``` python
real = APO(close, fastperiod=12, slowperiod=26, matype=0)
```



**AROON** - Aroon

``` python
aroondown, aroonup = AROON(high, low, timeperiod=14)
```



**AROONOSC** - Aroon Oscillator

``` python
real = AROONOSC(high, low, timeperiod=14)
```



**BOP** - Balance Of Power

``` python
real = BOP(open, high, low, close)
```



**CCI** - Commodity Channel Index

``` python
real = CCI(high, low, close, timeperiod=14)
```



**CMO** - Chande Momentum Oscillator

``` python
real = CMO(close, timeperiod=14)
```



**DX** - Directional Movement Index

``` python
real = DX(high, low, close, timeperiod=14)
```



**MACD** - Moving Average Convergence/Divergence

``` python
macd, macdsignal, macdhist = MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
```



**MACDEXT** - MACD with controllable MA type

``` python
macd, macdsignal, macdhist = MACDEXT(close, fastperiod=12, fastmatype=0, slowperiod=26, slowmatype=0, signalperiod=9, signalmatype=0)
```



**MACDFIX** - Moving Average Convergence/Divergence Fix 12/26

``` python
macd, macdsignal, macdhist = MACDFIX(close, signalperiod=9)
```



**MFI** - Money Flow Index

``` python
real = MFI(high, low, close, volume, timeperiod=14)
```



**MINUS_D**I - Minus Directional Indicator

``` python
real = MINUS_DI(high, low, close, timeperiod=14)
```



**MINUS_DM** - Minus Directional Movement

``` python
real = MINUS_DM(high, low, timeperiod=14)
```



**MOM** - Momentum

``` python
real = MOM(close, timeperiod=10)
```



**PLUS_DI** - Plus Directional Indicator

``` python
real = PLUS_DI(high, low, close, timeperiod=14)
```



**PLUS_DM** - Plus Directional Movement

``` python
real = PLUS_DM(high, low, timeperiod=14)
```



**PPO** - Percentage Price Oscillator

``` python
real = PPO(close, fastperiod=12, slowperiod=26, matype=0)
```



**ROC** - Rate of change : ((price/prevPrice)-1)*100

``` python
real = ROC(close, timeperiod=10)
```



**ROCP** - Rate of change Percentage: (price-prevPrice)/prevPrice

``` python
real = ROCP(close, timeperiod=10)
```



**ROCR** - Rate of change ratio: (price/prevPrice)

``` python
real = ROCR(close, timeperiod=10)
```



**ROCR100** - Rate of change ratio 100 scale: (price/prevPrice)*100

``` python
real = ROCR100(close, timeperiod=10)
```



**RSI** - Relative Strength Index

``` python
real = RSI(close, timeperiod=14)
```



**STOCH** - Stochastic

``` python
slowk, slowd = STOCH(high, low, close, fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
```



**STOCHF** - Stochastic Fast

``` python
fastk, fastd = STOCHF(high, low, close, fastk_period=5, fastd_period=3, fastd_matype=0)
```



**STOCHRSI** - Stochastic Relative Strength Index

``` python
fastk, fastd = STOCHRSI(close, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)
```



**TRIX** - 1-day Rate-Of-Change (ROC) of a Triple Smooth EMA

``` python
real = TRIX(close, timeperiod=30)
```



**ULTOSC** - Ultimate Oscillator

``` python
real = ULTOSC(high, low, close, timeperiod1=7, timeperiod2=14, timeperiod3=28)
```



**WILLR** - Williams' %R

``` python
real = WILLR(high, low, close, timeperiod=14)
```



### Volume Indicator Functions

**AD** - Chaikin A/D Line
``` python
real = AD(high, low, close, volume)
```



**ADOSC** - Chaikin A/D Oscillator

``` python
real = ADOSC(high, low, close, volume, fastperiod=3, slowperiod=10)
```



**OBV** - On Balance Volume

``` python
real = OBV(close, volume)
```



### Volatility Indicator Functions

**ATR** - Average True Range
``` python
real = ATR(high, low, close, timeperiod=14)
```



**NATR** - Normalized Average True Range

``` python
real = NATR(high, low, close, timeperiod=14)
```



**TRANGE** - True Range

``` python
real = TRANGE(high, low, close)
```



### Price Transform Functions

**AVGPRICE** - Average Price

``` python
real = AVGPRICE(open, high, low, close)
```



***MEDPRICE*** - Median Price

``` python
real = MEDPRICE(high, low)
```



**TYPPRICE** - Typical Price

``` python
real = TYPPRICE(high, low, close)
```



**WCLPRICE** - Weighted Close Price

``` python
real = WCLPRICE(high, low, close)
```



### Cycle Indicator Functions

**HT_DCPERIOD** - Hilbert Transform - Dominant Cycle Period

``` python
real = HT_DCPERIOD(close)
```



**HT_DCPHASE** - Hilbert Transform - Dominant Cycle Phase

``` python
real = HT_DCPHASE(close)
```



**HT_PHASOR** - Hilbert Transform - Phasor Components

``` python
inphase, quadrature = HT_PHASOR(close)
```



**HT_SINE** - Hilbert Transform - SineWave

``` python
sine, leadsine = HT_SINE(close)
```



**HT_TRENDMODE** - Hilbert Transform - Trend vs Cycle Mode

``` python
integer = HT_TRENDMODE(close)
```



### Pattern Recognition Functions

**CDL2CROWS** - Two Crows
``` python
integer = CDL2CROWS(open, high, low, close)
```



**CDL3BLACKCROWS** - Three Black Crows

``` python
integer = CDL3BLACKCROWS(open, high, low, close)
```



**CDL3INSIDE** - Three Inside Up/Down

``` python
integer = CDL3INSIDE(open, high, low, close)
```



**CDL3LINESTRIKE** - Three-Line Strike

``` python
integer = CDL3LINESTRIKE(open, high, low, close)
```



**CDL3OUTSIDE** - Three Outside Up/Down

``` python
integer = CDL3OUTSIDE(open, high, low, close)
```



**CDL3STARSINSOUTH** - Three Stars In The South

``` python
integer = CDL3STARSINSOUTH(open, high, low, close)
```



**CDL3WHITESOLDIERS** - Three Advancing White Soldiers

``` python
integer = CDL3WHITESOLDIERS(open, high, low, close)
```



**CDLABANDONEDBABY** - Abandoned Baby

``` python
integer = CDLABANDONEDBABY(open, high, low, close, penetration=0)
```



**CDLADVANCEBLOCK** - Advance Block

``` python
integer = CDLADVANCEBLOCK(open, high, low, close)
```



**CDLBELTHOLD** - Belt-hold

``` python
integer = CDLBELTHOLD(open, high, low, close)
```



**CDLBREAKAWAY** - Breakaway

``` python
integer = CDLBREAKAWAY(open, high, low, close)
```



**CDLCLOSINGMARUBOZU** - Closing Marubozu

``` python
integer = CDLCLOSINGMARUBOZU(open, high, low, close)
```



**CDLCONCEALBABYSWALL** - Concealing Baby Swallow

``` python
integer = CDLCONCEALBABYSWALL(open, high, low, close)
```



**CDLCOUNTERATTACK** - Counterattack

``` python
integer = CDLCOUNTERATTACK(open, high, low, close)
```



**CDLDARKCLOUDCOVER** - Dark Cloud Cover

``` python
integer = CDLDARKCLOUDCOVER(open, high, low, close, penetration=0)
```



**CDLDOJI** - Doji

``` python
integer = CDLDOJI(open, high, low, close)
```



**CDLDOJISTAR** - Doji Star

``` python
integer = CDLDOJISTAR(open, high, low, close)
```



**CDLDRAGONFLYDOJI** - Dragonfly Doji

``` python
integer = CDLDRAGONFLYDOJI(open, high, low, close)
```



**CDLENGULFING** - Engulfing Pattern

``` python
integer = CDLENGULFING(open, high, low, close)
```



**CDLEVENINGDOJISTAR** - Evening Doji Star

``` python
integer = CDLEVENINGDOJISTAR(open, high, low, close, penetration=0)
```



**CDLEVENINGSTAR** - Evening Star

``` python
integer = CDLEVENINGSTAR(open, high, low, close, penetration=0)
```



**CDLGAPSIDESIDEWHITE** - Up/Down-gap side-by-side white lines

``` python
integer = CDLGAPSIDESIDEWHITE(open, high, low, close)
```



**CDLGRAVESTONEDOJI** - Gravestone Doji

``` python
integer = CDLGRAVESTONEDOJI(open, high, low, close)
```



**CDLHAMMER** - Hammer

``` python
integer = CDLHAMMER(open, high, low, close)
```



**CDLHANGINGMAN** - Hanging Man

``` python
integer = CDLHANGINGMAN(open, high, low, close)
```



**CDLHARAMI** - Harami Pattern

``` python
integer = CDLHARAMI(open, high, low, close)
```



**CDLHARAMICROS**S - Harami Cross Pattern

``` python
integer = CDLHARAMICROSS(open, high, low, close)
```



**CDLHIGHWAVE** - High-Wave Candle

``` python
integer = CDLHIGHWAVE(open, high, low, close)
```



**CDLHIKKAKE** - Hikkake Pattern

``` python
integer = CDLHIKKAKE(open, high, low, close)
```



**CDLHIKKAKEMOD** - Modified Hikkake Pattern

``` python
integer = CDLHIKKAKEMOD(open, high, low, close)
```



**CDLHOMINGPIGEON** - Homing Pigeon

``` python
integer = CDLHOMINGPIGEON(open, high, low, close)
```



**CDLIDENTICAL3CROWS** - Identical Three Crows

``` python
integer = CDLIDENTICAL3CROWS(open, high, low, close)
```



**CDLINNECK** - In-Neck Pattern

``` python
integer = CDLINNECK(open, high, low, close)
```



**CDLINVERTEDHAMMER** - Inverted Hammer

``` python
integer = CDLINVERTEDHAMMER(open, high, low, close)
```



**CDLKICKING** - Kicking

``` python
integer = CDLKICKING(open, high, low, close)
```



**CDLKICKINGBYLENGTH** - Kicking - bull/bear determined by the longer marubozu

``` python
integer = CDLKICKINGBYLENGTH(open, high, low, close)
```



**CDLLADDERBOTTOM** - Ladder Bottom

``` python
integer = CDLLADDERBOTTOM(open, high, low, close)
```



**CDLLONGLEGGEDDOJI** - Long Legged Doji

``` python
integer = CDLLONGLEGGEDDOJI(open, high, low, close)
```



**CDLLONGLINE** - Long Line Candle

``` python
integer = CDLLONGLINE(open, high, low, close)
```



**CDLMARUBOZU** - Marubozu

``` python
integer = CDLMARUBOZU(open, high, low, close)
```



**CDLMATCHINGLOW** - Matching Low

``` python
integer = CDLMATCHINGLOW(open, high, low, close)
```



**CDLMATHOLD** - Mat Hold

``` python
integer = CDLMATHOLD(open, high, low, close, penetration=0)
```



**CDLMORNINGDOJISTAR** - Morning Doji Star

``` python
integer = CDLMORNINGDOJISTAR(open, high, low, close, penetration=0)
```



**CDLMORNINGSTAR** - Morning Star

``` python
integer = CDLMORNINGSTAR(open, high, low, close, penetration=0)
```



**CDLONNECK** - On-Neck Pattern

``` python
integer = CDLONNECK(open, high, low, close)
```



**CDLPIERCING** - Piercing Pattern

``` python
integer = CDLPIERCING(open, high, low, close)
```



**CDLRICKSHAWMAN** - Rickshaw Man

``` python
integer = CDLRICKSHAWMAN(open, high, low, close)
```



**CDLRISEFALL3METHODS** - Rising/Falling Three Methods

``` python
integer = CDLRISEFALL3METHODS(open, high, low, close)
```



**CDLSEPARATINGLINES** - Separating Lines

``` python
integer = CDLSEPARATINGLINES(open, high, low, close)
```



**CDLSHOOTINGSTAR** - Shooting Star

``` python
integer = CDLSHOOTINGSTAR(open, high, low, close)
```



**CDLSHORTLINE** - Short Line Candle

``` python
integer = CDLSHORTLINE(open, high, low, close)
```



**CDLSPINNINGTOP** - Spinning Top

``` python
integer = CDLSPINNINGTOP(open, high, low, close)
```



**CDLSTALLEDPATTERN** - Stalled Pattern

``` python
integer = CDLSTALLEDPATTERN(open, high, low, close)
```



**CDLSTICKSANDWICH** - Stick Sandwich

``` python
integer = CDLSTICKSANDWICH(open, high, low, close)
```



**CDLTAKURI** - Takuri (Dragonfly Doji with very long lower shadow)

``` python
integer = CDLTAKURI(open, high, low, close)
```



**CDLTASUKIGAP** - Tasuki Gap

``` python
integer = CDLTASUKIGAP(open, high, low, close)
```



**CDLTHRUSTING** - Thrusting Pattern

``` python
integer = CDLTHRUSTING(open, high, low, close)
```



**CDLTRISTAR** - Tristar Pattern

``` python
integer = CDLTRISTAR(open, high, low, close)
```



**CDLUNIQUE3RIVER** - Unique 3 River

``` python
integer = CDLUNIQUE3RIVER(open, high, low, close)
```



**CDLUPSIDEGAP2CROWS** - Upside Gap Two Crows

``` python
integer = CDLUPSIDEGAP2CROWS(open, high, low, close)
```



**CDLXSIDEGAP3METHODS** - Upside/Downside Gap Three Methods

``` python
integer = CDLXSIDEGAP3METHODS(open, high, low, close)
```



### Statistic Functions

**BETA** - Beta

``` python
real = BETA(high, low, timeperiod=5)
```



**CORREL** - Pearson's Correlation Coefficient (r)

``` python
real = CORREL(high, low, timeperiod=30)
```



**LINEARREG** - Linear Regression

``` python
real = LINEARREG(close, timeperiod=14)
```



**LINEARREG_ANGLE** - Linear Regression Angle

``` python
real = LINEARREG_ANGLE(close, timeperiod=14)
```



**LINEARREG_INTERCEPT** - Linear Regression Intercept

``` python
real = LINEARREG_INTERCEPT(close, timeperiod=14)
```



**LINEARREG_SLOPE** - Linear Regression Slope

``` python
real = LINEARREG_SLOPE(close, timeperiod=14)
```



**STDDEV** - Standard Deviation

``` python
real = STDDEV(close, timeperiod=5, nbdev=1)
```



**TSF** - Time Series Forecast

``` python
real = TSF(close, timeperiod=14)
```



**VAR** - Variance

``` python
real = VAR(close, timeperiod=5, nbdev=1)
```



### Math Transform Functions

**ACOS** - Vector Trigonometric ACos

``` python
real = ACOS(close)
```



**ASIN** - Vector Trigonometric ASin

``` python
real = ASIN(close)
```



**ATAN** - Vector Trigonometric ATan

``` python
real = ATAN(close)
```



**CEIL** - Vector Ceil

``` python
real = CEIL(close)
```



**COS** - Vector Trigonometric Cos

``` python
real = COS(close)
```



**COSH** - Vector Trigonometric Cosh

``` python
real = COSH(close)
```



**EXP** - Vector Arithmetic Exp

``` python
real = EXP(close)
```



**FLOOR** - Vector Floor

``` python
real = FLOOR(close)
```



**LN** - Vector Log Natural

``` python
real = LN(close)
```



**LOG10** - Vector Log10

``` python
real = LOG10(close)
```



**SIN** - Vector Trigonometric Sin

``` python
real = SIN(close)
```



**SINH** - Vector Trigonometric Sinh

``` python
real = SINH(close)
```



**SQRT** - Vector Square Root

``` python
real = SQRT(close)
```



**TAN** - Vector Trigonometric Tan

``` python
real = TAN(close)
```



**TANH** - Vector Trigonometric Tanh

``` python
real = TANH(close)
```



### Math Operator Functions

**ADD** - Vector Arithmetic Add

``` python
real = ADD(high, low)
```



**DIV** - Vector Arithmetic Div

``` python
real = DIV(high, low)
```



**MAX** - Highest value over a specified period

``` python
real = MAX(close, timeperiod=30)
```



**MAXINDEX** - Index of highest value over a specified period

``` python
integer = MAXINDEX(close, timeperiod=30)
```



**MIN** - Lowest value over a specified period

``` python
real = MIN(close, timeperiod=30)
```



**MININDEX** - Index of lowest value over a specified period

``` python
integer = MININDEX(close, timeperiod=30)
```



**MINMAX** - Lowest and highest values over a specified period

``` python
min, max = MINMAX(close, timeperiod=30)
```



**MINMAXINDEX** - Indexes of lowest and highest values over a specified period

``` python
minidx, maxidx = MINMAXINDEX(close, timeperiod=30)
```



**MULT** - Vector Arithmetic Mult

``` python
real = MULT(high, low)
```



**SUB** - Vector Arithmetic Substraction

``` python
real = SUB(high, low)
```



**SUM** - Summation

``` python
real = SUM(close, timeperiod=30)
```
