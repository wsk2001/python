# Ta-Lib 함수 모음

출처: https://blog.naver.com/PostView.nhn?blogId=tamiel&logNo=221900701118&parentCategoryNo=11&categoryNo=&viewDate=&isShowPopularPosts=false&from=postView



 Overlap Studies Functions



BBANDS - Bollinger Bands

upperband, middleband, lowerband = BBANDS(close, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)



DEMA - Double Exponential Moving Average

real = DEMA(close, timeperiod=30)



EMA - Exponential Moving Average

real = EMA(close, timeperiod=30)



HT_TRENDLINE - Hilbert Transform - Instantaneous Trendline

real = HT_TRENDLINE(close)



KAMA - Kaufman Adaptive Moving Average

real = KAMA(close, timeperiod=30)



MA - Moving average

real = MA(close, timeperiod=30, matype=0)



MAMA - MESA Adaptive Moving Average

mama, fama = MAMA(close, fastlimit=0, slowlimit=0)



MAVP - Moving average with variable period

real = MAVP(close, periods, minperiod=2, maxperiod=30, matype=0)



MIDPOINT - MidPoint over period

real = MIDPOINT(close, timeperiod=14)



MIDPRICE - Midpoint Price over period

real = MIDPRICE(high, low, timeperiod=14)



SAR - Parabolic SAR

real = SAR(high, low, acceleration=0, maximum=0)



SAREXT - Parabolic SAR - Extended

real = SAREXT(high, low, startvalue=0, offsetonreverse=0, accelerationinitlong=0, accelerationlong=0, accelerationmaxlong=0, accelerationinitshort=0, accelerationshort=0, accelerationmaxshort=0)



SMA - Simple Moving Average

real = SMA(close, timeperiod=30)



T3 - Triple Exponential Moving Average (T3)

real = T3(close, timeperiod=5, vfactor=0)



TEMA - Triple Exponential Moving Average

real = TEMA(close, timeperiod=30)



TRIMA - Triangular Moving Average

real = TRIMA(close, timeperiod=30)



WMA - Weighted Moving Average

real = WMA(close, timeperiod=30)



\- Momentum Indicator Functions



ADX - Average Directional Movement Index

real = ADX(high, low, close, timeperiod=14)



ADXR - Average Directional Movement Index Rating

real = ADXR(high, low, close, timeperiod=14)



APO - Absolute Price Oscillator

real = APO(close, fastperiod=12, slowperiod=26, matype=0)



AROON - Aroon

aroondown, aroonup = AROON(high, low, timeperiod=14)



AROONOSC - Aroon Oscillator

real = AROONOSC(high, low, timeperiod=14)



BOP - Balance Of Power

real = BOP(open, high, low, close)



CCI - Commodity Channel Index

real = CCI(high, low, close, timeperiod=14)



CMO - Chande Momentum Oscillator

real = CMO(close, timeperiod=14)



DX - Directional Movement Index

real = DX(high, low, close, timeperiod=14)



MACD - Moving Average Convergence/Divergence

macd, macdsignal, macdhist = MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)



MACDEXT - MACD with controllable MA type

macd, macdsignal, macdhist = MACDEXT(close, fastperiod=12, fastmatype=0, slowperiod=26, slowmatype=0, signalperiod=9, signalmatype=0)



MACDFIX - Moving Average Convergence/Divergence Fix 12/26

macd, macdsignal, macdhist = MACDFIX(close, signalperiod=9)



MFI - Money Flow Index

real = MFI(high, low, close, volume, timeperiod=14)



MINUS_DI - Minus Directional Indicator

real = MINUS_DI(high, low, close, timeperiod=14)



MINUS_DM - Minus Directional Movement

real = MINUS_DM(high, low, timeperiod=14)



MOM - Momentum

real = MOM(close, timeperiod=10)



PLUS_DI - Plus Directional Indicator

real = PLUS_DI(high, low, close, timeperiod=14)



PLUS_DM - Plus Directional Movement

real = PLUS_DM(high, low, timeperiod=14)



PPO - Percentage Price Oscillator

real = PPO(close, fastperiod=12, slowperiod=26, matype=0)



ROC - Rate of change : ((price/prevPrice)-1)*100

real = ROC(close, timeperiod=10)



ROCP - Rate of change Percentage: (price-prevPrice)/prevPrice

real = ROCP(close, timeperiod=10)



ROCR - Rate of change ratio: (price/prevPrice)

real = ROCR(close, timeperiod=10)



ROCR100 - Rate of change ratio 100 scale: (price/prevPrice)*100

real = ROCR100(close, timeperiod=10)



RSI - Relative Strength Index

real = RSI(close, timeperiod=14)



STOCH - Stochastic

slowk, slowd = STOCH(high, low, close, fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)



STOCHF - Stochastic Fast

fastk, fastd = STOCHF(high, low, close, fastk_period=5, fastd_period=3, fastd_matype=0)



STOCHRSI - Stochastic Relative Strength Index

fastk, fastd = STOCHRSI(close, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)



TRIX - 1-day Rate-Of-Change (ROC) of a Triple Smooth EMA

real = TRIX(close, timeperiod=30)



ULTOSC - Ultimate Oscillator

real = ULTOSC(high, low, close, timeperiod1=7, timeperiod2=14, timeperiod3=28)



WILLR - Williams' %R

real = WILLR(high, low, close, timeperiod=14)



\- Volume Indicator Functions



AD - Chaikin A/D Line

real = AD(high, low, close, volume)



ADOSC - Chaikin A/D Oscillator

real = ADOSC(high, low, close, volume, fastperiod=3, slowperiod=10)



OBV - On Balance Volume

real = OBV(close, volume)



\- Volatility Indicator Functions



ATR - Average True Range

real = ATR(high, low, close, timeperiod=14)



NATR - Normalized Average True Range

real = NATR(high, low, close, timeperiod=14)



TRANGE - True Range

real = TRANGE(high, low, close)



\- Price Transform Functions



AVGPRICE - Average Price

real = AVGPRICE(open, high, low, close)



MEDPRICE - Median Price

real = MEDPRICE(high, low)



TYPPRICE - Typical Price

real = TYPPRICE(high, low, close)



WCLPRICE - Weighted Close Price

real = WCLPRICE(high, low, close)



\- Cycle Indicator Functions



HT_DCPERIOD - Hilbert Transform - Dominant Cycle Period

real = HT_DCPERIOD(close)



HT_DCPHASE - Hilbert Transform - Dominant Cycle Phase

real = HT_DCPHASE(close)



HT_PHASOR - Hilbert Transform - Phasor Components

inphase, quadrature = HT_PHASOR(close)



HT_SINE - Hilbert Transform - SineWave

sine, leadsine = HT_SINE(close)



HT_TRENDMODE - Hilbert Transform - Trend vs Cycle Mode

integer = HT_TRENDMODE(close)



\- Pattern Recognition Functions



CDL2CROWS - Two Crows

integer = CDL2CROWS(open, high, low, close)



CDL3BLACKCROWS - Three Black Crows

integer = CDL3BLACKCROWS(open, high, low, close)



CDL3INSIDE - Three Inside Up/Down

integer = CDL3INSIDE(open, high, low, close)



CDL3LINESTRIKE - Three-Line Strike

integer = CDL3LINESTRIKE(open, high, low, close)



CDL3OUTSIDE - Three Outside Up/Down

integer = CDL3OUTSIDE(open, high, low, close)



CDL3STARSINSOUTH - Three Stars In The South

integer = CDL3STARSINSOUTH(open, high, low, close)



CDL3WHITESOLDIERS - Three Advancing White Soldiers

integer = CDL3WHITESOLDIERS(open, high, low, close)



CDLABANDONEDBABY - Abandoned Baby

integer = CDLABANDONEDBABY(open, high, low, close, penetration=0)



CDLADVANCEBLOCK - Advance Block

integer = CDLADVANCEBLOCK(open, high, low, close)



CDLBELTHOLD - Belt-hold

integer = CDLBELTHOLD(open, high, low, close)



CDLBREAKAWAY - Breakaway

integer = CDLBREAKAWAY(open, high, low, close)



CDLCLOSINGMARUBOZU - Closing Marubozu

integer = CDLCLOSINGMARUBOZU(open, high, low, close)



CDLCONCEALBABYSWALL - Concealing Baby Swallow

integer = CDLCONCEALBABYSWALL(open, high, low, close)



CDLCOUNTERATTACK - Counterattack

integer = CDLCOUNTERATTACK(open, high, low, close)



CDLDARKCLOUDCOVER - Dark Cloud Cover

integer = CDLDARKCLOUDCOVER(open, high, low, close, penetration=0)



CDLDOJI - Doji

integer = CDLDOJI(open, high, low, close)



CDLDOJISTAR - Doji Star

integer = CDLDOJISTAR(open, high, low, close)



CDLDRAGONFLYDOJI - Dragonfly Doji

integer = CDLDRAGONFLYDOJI(open, high, low, close)



CDLENGULFING - Engulfing Pattern

integer = CDLENGULFING(open, high, low, close)



CDLEVENINGDOJISTAR - Evening Doji Star

integer = CDLEVENINGDOJISTAR(open, high, low, close, penetration=0)



CDLEVENINGSTAR - Evening Star

integer = CDLEVENINGSTAR(open, high, low, close, penetration=0)



CDLGAPSIDESIDEWHITE - Up/Down-gap side-by-side white lines

integer = CDLGAPSIDESIDEWHITE(open, high, low, close)



CDLGRAVESTONEDOJI - Gravestone Doji

integer = CDLGRAVESTONEDOJI(open, high, low, close)



CDLHAMMER - Hammer

integer = CDLHAMMER(open, high, low, close)



CDLHANGINGMAN - Hanging Man

integer = CDLHANGINGMAN(open, high, low, close)



CDLHARAMI - Harami Pattern

integer = CDLHARAMI(open, high, low, close)



CDLHARAMICROSS - Harami Cross Pattern

integer = CDLHARAMICROSS(open, high, low, close)



CDLHIGHWAVE - High-Wave Candle

integer = CDLHIGHWAVE(open, high, low, close)



CDLHIKKAKE - Hikkake Pattern

integer = CDLHIKKAKE(open, high, low, close)



CDLHIKKAKEMOD - Modified Hikkake Pattern

integer = CDLHIKKAKEMOD(open, high, low, close)



CDLHOMINGPIGEON - Homing Pigeon

integer = CDLHOMINGPIGEON(open, high, low, close)



CDLIDENTICAL3CROWS - Identical Three Crows

integer = CDLIDENTICAL3CROWS(open, high, low, close)



CDLINNECK - In-Neck Pattern

integer = CDLINNECK(open, high, low, close)



CDLINVERTEDHAMMER - Inverted Hammer

integer = CDLINVERTEDHAMMER(open, high, low, close)



CDLKICKING - Kicking

integer = CDLKICKING(open, high, low, close)



CDLKICKINGBYLENGTH - Kicking - bull/bear determined by the longer marubozu

integer = CDLKICKINGBYLENGTH(open, high, low, close)



CDLLADDERBOTTOM - Ladder Bottom

integer = CDLLADDERBOTTOM(open, high, low, close)



CDLLONGLEGGEDDOJI - Long Legged Doji

integer = CDLLONGLEGGEDDOJI(open, high, low, close)



CDLLONGLINE - Long Line Candle

integer = CDLLONGLINE(open, high, low, close)



CDLMARUBOZU - Marubozu

integer = CDLMARUBOZU(open, high, low, close)



CDLMATCHINGLOW - Matching Low

integer = CDLMATCHINGLOW(open, high, low, close)



CDLMATHOLD - Mat Hold

integer = CDLMATHOLD(open, high, low, close, penetration=0)



CDLMORNINGDOJISTAR - Morning Doji Star

integer = CDLMORNINGDOJISTAR(open, high, low, close, penetration=0)



CDLMORNINGSTAR - Morning Star

integer = CDLMORNINGSTAR(open, high, low, close, penetration=0)



CDLONNECK - On-Neck Pattern

integer = CDLONNECK(open, high, low, close)



CDLPIERCING - Piercing Pattern

integer = CDLPIERCING(open, high, low, close)



CDLRICKSHAWMAN - Rickshaw Man

integer = CDLRICKSHAWMAN(open, high, low, close)



CDLRISEFALL3METHODS - Rising/Falling Three Methods

integer = CDLRISEFALL3METHODS(open, high, low, close)



CDLSEPARATINGLINES - Separating Lines

integer = CDLSEPARATINGLINES(open, high, low, close)



CDLSHOOTINGSTAR - Shooting Star

integer = CDLSHOOTINGSTAR(open, high, low, close)



CDLSHORTLINE - Short Line Candle

integer = CDLSHORTLINE(open, high, low, close)



CDLSPINNINGTOP - Spinning Top

integer = CDLSPINNINGTOP(open, high, low, close)



CDLSTALLEDPATTERN - Stalled Pattern

integer = CDLSTALLEDPATTERN(open, high, low, close)



CDLSTICKSANDWICH - Stick Sandwich

integer = CDLSTICKSANDWICH(open, high, low, close)



CDLTAKURI - Takuri (Dragonfly Doji with very long lower shadow)

integer = CDLTAKURI(open, high, low, close)



CDLTASUKIGAP - Tasuki Gap

integer = CDLTASUKIGAP(open, high, low, close)



CDLTHRUSTING - Thrusting Pattern

integer = CDLTHRUSTING(open, high, low, close)



CDLTRISTAR - Tristar Pattern

integer = CDLTRISTAR(open, high, low, close)



CDLUNIQUE3RIVER - Unique 3 River

integer = CDLUNIQUE3RIVER(open, high, low, close)



CDLUPSIDEGAP2CROWS - Upside Gap Two Crows

integer = CDLUPSIDEGAP2CROWS(open, high, low, close)



CDLXSIDEGAP3METHODS - Upside/Downside Gap Three Methods

integer = CDLXSIDEGAP3METHODS(open, high, low, close)



---

\- Statistic Functions



BETA - Beta

real = BETA(high, low, timeperiod=5)



CORREL - Pearson's Correlation Coefficient (r)

real = CORREL(high, low, timeperiod=30)



LINEARREG - Linear Regression

real = LINEARREG(close, timeperiod=14)



LINEARREG_ANGLE - Linear Regression Angle

real = LINEARREG_ANGLE(close, timeperiod=14)



LINEARREG_INTERCEPT - Linear Regression Intercept

real = LINEARREG_INTERCEPT(close, timeperiod=14)



LINEARREG_SLOPE - Linear Regression Slope

real = LINEARREG_SLOPE(close, timeperiod=14)



STDDEV - Standard Deviation

real = STDDEV(close, timeperiod=5, nbdev=1)



TSF - Time Series Forecast

real = TSF(close, timeperiod=14)



VAR - Variance

real = VAR(close, timeperiod=5, nbdev=1)



\- Math Transform Functions



ACOS - Vector Trigonometric ACos

real = ACOS(close)



ASIN - Vector Trigonometric ASin

real = ASIN(close)



ATAN - Vector Trigonometric ATan

real = ATAN(close)



CEIL - Vector Ceil

real = CEIL(close)



COS - Vector Trigonometric Cos

real = COS(close)



COSH - Vector Trigonometric Cosh

real = COSH(close)



EXP - Vector Arithmetic Exp

real = EXP(close)



FLOOR - Vector Floor

real = FLOOR(close)



LN - Vector Log Natural

real = LN(close)



LOG10 - Vector Log10

real = LOG10(close)



SIN - Vector Trigonometric Sin

real = SIN(close)



SINH - Vector Trigonometric Sinh

real = SINH(close)



SQRT - Vector Square Root

real = SQRT(close)



TAN - Vector Trigonometric Tan

real = TAN(close)



TANH - Vector Trigonometric Tanh

real = TANH(close)



\- Math Operator Functions



ADD - Vector Arithmetic Add

real = ADD(high, low)



DIV - Vector Arithmetic Div

real = DIV(high, low)



MAX - Highest value over a specified period

real = MAX(close, timeperiod=30)



MAXINDEX - Index of highest value over a specified period

integer = MAXINDEX(close, timeperiod=30)



MIN - Lowest value over a specified period

real = MIN(close, timeperiod=30)



MININDEX - Index of lowest value over a specified period

integer = MININDEX(close, timeperiod=30)



MINMAX - Lowest and highest values over a specified period

min, max = MINMAX(close, timeperiod=30)



MINMAXINDEX - Indexes of lowest and highest values over a specified period

minidx, maxidx = MINMAXINDEX(close, timeperiod=30)



MULT - Vector Arithmetic Mult

real = MULT(high, low)



SUB - Vector Arithmetic Substraction

real = SUB(high, low)



SUM - Summation

real = SUM(close, timeperiod=30)

