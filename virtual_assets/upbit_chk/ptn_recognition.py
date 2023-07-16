import talib 
import calendar
import getopt
import sys, time
import pyupbit
from common.utils import market_code
from datetime import datetime
import argparse
import pandas as pd

# import matplotlib.pyplot as plt

dic_cdc = {
    'CDL2CROWS': '강력한 매도',
    'CDL3BLACKCROWS': '강력한 매도',
    'CDL3INSIDE': '횡보',
    'CDL3LINESTRIKE': '강력한 매수',
    'CDL3OUTSIDE': '추세의 전환',
    'CDL3STARSINSOUTH': '강력한 매수',
    'CDL3WHITESOLDIERS': '강력한 매수',
    'CDLABANDONEDBABY': '강력한 매수',
    'CDLADVANCEBLOCK': '강력한 매도',
    'CDLBELTHOLD': '강력한 매수',
    'CDLBREAKAWAY': '추세의 전환',
    'CDLCLOSINGMARUBOZU': '추세의 전환',
    'CDLCONCEALBABYSWALL': '강력한 매도',
    'CDLCOUNTERATTACK': '강력한 매수',
    'CDLDARKCLOUDCOVER': '강력한 매도',
    'CDLDOJI': '추세의 전환',
    'CDLDOJISTAR': '추세의 전환',
    'CDLDRAGONFLYDOJI': '추세의 전환',
    'CDLENGULFING': '추세의 전환',
    'CDLEVENINGDOJISTAR': '추세의 전환',
    'CDLEVENINGSTAR': '추세의 전환',
    'CDLGAPSIDESIDEWHITE': '추세의 전환',
    'CDLGRAVESTONEDOJI': '추세의 전환',
    'CDLHAMMER': '추세의 전환',
    'CDLHANGINGMAN': '추세의 전환',
    'CDLHARAMI': '추세의 전환',
    'CDLHARAMICROSS': '추세의 전환',
    'CDLHIGHWAVE': '추세의 전환',
    'CDLHIKKAKE': '추세의 전환',
    'CDLHIKKAKEMOD': '추세의 전환',
    'CDLHOMINGPIGEON': '추세가 지속',
    'CDLIDENTICAL3CROWS': '하락 반전',
    'CDLINNECK': '추세의 전환',
    'CDLINVERTEDHAMMER': '상승 반전',
    'CDLKICKING': '매수',
    'CDLKICKINGBYLENGTH': '매수',
    'CDLLADDERBOTTOM': '매수',
    'CDLLONGLEGGEDDOJI': '매수',
    'CDLLONGLINE': '추세의 전환',
    'CDLMARUBOZU': '추세의 전환',
    'CDLMATCHINGLOW': '매수',
    'CDLMATHOLD': '매수 하락전',
    'CDLMORNINGDOJISTAR': '매수',
    'CDLMORNINGSTAR': '매수',
    'CDLONNECK': '매도',
    'CDLPIERCING': '매수',
    'CDLRICKSHAWMAN': '매수',
    'CDLRISEFALL3METHODS': '매도',
    'CDLSEPARATINGLINES': '매도',
    'CDLSHOOTINGSTAR': '매수',
    'CDLSHORTLINE': '상승 반전',
    'CDLSPINNINGTOP': '추세의 전환',
    'CDLSTALLEDPATTERN': '추세가 약화',
    'CDLSTICKSANDWICH': '추세가 약화',
    'CDLTAKURI': '추세의 전환',
    'CDLTASUKIGAP': '매도',
    'CDLTHRUSTING': '매수',
    'CDLTRISTAR': '매수',
    'CDLUNIQUE3RIVER': '추세의 전환',
    'CDLUPSIDEGAP2CROWS': '추세의 전환',
    'CDLXSIDEGAP3METHODS': '추세의 전환'
}

dic_cdc_name = {
    'CDL2CROWS':'Two Crows',
    'CDL3BLACKCROWS':'Three Black Crows',
    'CDL3INSIDE':'Three Inside Up/Down',
    'CDL3LINESTRIKE':'Three-Line Strike',
    'CDL3OUTSIDE':'Three Outside Up/Down',
    'CDL3STARSINSOUTH':'Three Stars In The South',
    'CDL3WHITESOLDIERS':'Three Advancing White Soldiers',
    'CDLABANDONEDBABY':'Abandoned Baby',
    'CDLADVANCEBLOCK':'Advance Block',
    'CDLBELTHOLD':'Belt-hold',
    'CDLBREAKAWAY':'Breakaway',
    'CDLCLOSINGMARUBOZU':'Closing Marubozu',
    'CDLCONCEALBABYSWALL':'Concealing Baby Swallow',
    'CDLCOUNTERATTACK':'Counterattack',
    'CDLDARKCLOUDCOVER':'Dark Cloud Cover',
    'CDLDOJI':'Doji',
    'CDLDOJISTAR':'Doji Star',
    'CDLDRAGONFLYDOJI':'Dragonfly Doji',
    'CDLENGULFING':'Engulfing Pattern',
    'CDLEVENINGDOJISTAR':'Evening Doji Star',
    'CDLEVENINGSTAR':'Evening Star',
    'CDLGAPSIDESIDEWHITE':'Up/Down-gap side-by-side white lines',
    'CDLGRAVESTONEDOJI':'Gravestone Doji',
    'CDLHAMMER':'Hammer',
    'CDLHANGINGMAN':'Hanging Man',
    'CDLHARAMI':'Harami Pattern',
    'CDLHARAMICROSS':'Harami Cross Pattern',
    'CDLHIGHWAVE':'High-Wave Candle',
    'CDLHIKKAKE':'Hikkake Pattern',
    'CDLHIKKAKEMOD':'Modified Hikkake Pattern',
    'CDLHOMINGPIGEON':'Homing Pigeon',
    'CDLIDENTICAL3CROWS':'Identical Three Crows',
    'CDLINNECK':'In-Neck Pattern',
    'CDLINVERTEDHAMMER':'Inverted Hammer',
    'CDLKICKING':'Kicking',
    'CDLKICKINGBYLENGTH':'Kicking - bull/bear determined by the longer marubozu',
    'CDLLADDERBOTTOM':'Ladder Bottom',
    'CDLLONGLEGGEDDOJI':'Long Legged Doji',
    'CDLLONGLINE':'Long Line Candle',
    'CDLMARUBOZU':'Marubozu',
    'CDLMATCHINGLOW':'Matching Low',
    'CDLMATHOLD':'Mat Hold',
    'CDLMORNINGDOJISTAR':'Morning Doji Star',
    'CDLMORNINGSTAR':'Morning Star',
    'CDLONNECK':'On-Neck Pattern',
    'CDLPIERCING':'Piercing Pattern',
    'CDLRICKSHAWMAN':'Rickshaw Man',
    'CDLRISEFALL3METHODS':'Rising/Falling Three Methods',
    'CDLSEPARATINGLINES':'Separating Lines',
    'CDLSHOOTINGSTAR':'Shooting Star',
    'CDLSHORTLINE':'Short Line Candle',
    'CDLSPINNINGTOP':'Spinning Top',
    'CDLSTALLEDPATTERN':'Stalled Pattern',
    'CDLSTICKSANDWICH':'Stick Sandwich',
    'CDLTAKURI':'Takuri (Dragonfly Doji with very long lower shadow)',
    'CDLTASUKIGAP':'Tasuki Gap',
    'CDLTHRUSTING':'Thrusting Pattern',
    'CDLTRISTAR':'Tristar Pattern',
    'CDLUNIQUE3RIVER':'Unique 3 River',
    'CDLUPSIDEGAP2CROWS':'Upside Gap Two Crows',
    'CDLXSIDEGAP3METHODS':'Upside/Downside Gap Three Methods'
}

# Pattern Recognition Functions
# https://github.com/wsk2001/ta-lib-python/blob/master/docs/func_groups/pattern_recognition.md
dic_cdl_functions = {
    'CDL2CROWS': talib.CDL2CROWS,
    'CDL3BLACKCROWS': talib.CDL3BLACKCROWS,
    'CDL3INSIDE': talib.CDL3INSIDE,
    'CDL3LINESTRIKE': talib.CDL3LINESTRIKE,
    'CDL3OUTSIDE': talib.CDL3OUTSIDE,
    'CDL3STARSINSOUTH': talib.CDL3STARSINSOUTH,
    'CDL3WHITESOLDIERS': talib.CDL3WHITESOLDIERS,
    'CDLABANDONEDBABY': talib.CDLABANDONEDBABY,
    'CDLADVANCEBLOCK': talib.CDLADVANCEBLOCK,
    'CDLBELTHOLD': talib.CDLBELTHOLD,
    'CDLBREAKAWAY': talib.CDLBREAKAWAY,
    'CDLCLOSINGMARUBOZU': talib.CDLCLOSINGMARUBOZU,
    'CDLCONCEALBABYSWALL': talib.CDLCONCEALBABYSWALL,
    'CDLCOUNTERATTACK': talib.CDLCOUNTERATTACK,
    'CDLDARKCLOUDCOVER': talib.CDLDARKCLOUDCOVER,
    'CDLDOJI': talib.CDLDOJI,
    'CDLDOJISTAR': talib.CDLDOJISTAR,
    'CDLDRAGONFLYDOJI': talib.CDLDRAGONFLYDOJI,
    'CDLENGULFING': talib.CDLENGULFING,
    'CDLEVENINGDOJISTAR': talib.CDLEVENINGDOJISTAR,
    'CDLEVENINGSTAR': talib.CDLEVENINGSTAR,
    'CDLGAPSIDESIDEWHITE': talib.CDLGAPSIDESIDEWHITE,
    'CDLGRAVESTONEDOJI': talib.CDLGRAVESTONEDOJI,
    'CDLHAMMER': talib.CDLHAMMER,
    'CDLHANGINGMAN': talib.CDLHANGINGMAN,
    'CDLHARAMI': talib.CDLHARAMI,
    'CDLHARAMICROSS': talib.CDLHARAMICROSS,
    'CDLHIGHWAVE': talib.CDLHIGHWAVE,
    'CDLHIKKAKE': talib.CDLHIKKAKE,
    'CDLHIKKAKEMOD': talib.CDLHIKKAKEMOD,
    'CDLHOMINGPIGEON': talib.CDLHOMINGPIGEON,
    'CDLIDENTICAL3CROWS': talib.CDLIDENTICAL3CROWS,
    'CDLINNECK': talib.CDLINNECK,
    'CDLINVERTEDHAMMER': talib.CDLINVERTEDHAMMER,
    'CDLKICKING': talib.CDLKICKING,
    'CDLKICKINGBYLENGTH': talib.CDLKICKINGBYLENGTH,
    'CDLLADDERBOTTOM': talib.CDLLADDERBOTTOM,
    'CDLLONGLEGGEDDOJI': talib.CDLLONGLEGGEDDOJI,
    'CDLLONGLINE': talib.CDLLONGLINE,
    'CDLMARUBOZU': talib.CDLMARUBOZU,
    'CDLMATCHINGLOW': talib.CDLMATCHINGLOW,
    'CDLMATHOLD': talib.CDLMATHOLD,
    'CDLMORNINGDOJISTAR': talib.CDLMORNINGDOJISTAR,
    'CDLMORNINGSTAR': talib.CDLMORNINGSTAR,
    'CDLONNECK': talib.CDLONNECK,
    'CDLPIERCING': talib.CDLPIERCING,
    'CDLRICKSHAWMAN': talib.CDLRICKSHAWMAN,
    'CDLRISEFALL3METHODS': talib.CDLRISEFALL3METHODS,
    'CDLSEPARATINGLINES': talib.CDLSEPARATINGLINES,
    'CDLSHOOTINGSTAR': talib.CDLSHOOTINGSTAR,
    'CDLSHORTLINE': talib.CDLSHORTLINE,
    'CDLSPINNINGTOP': talib.CDLSPINNINGTOP,
    'CDLSTALLEDPATTERN': talib.CDLSTALLEDPATTERN,
    'CDLSTICKSANDWICH': talib.CDLSTICKSANDWICH,
    'CDLTAKURI': talib.CDLTAKURI,
    'CDLTASUKIGAP': talib.CDLTASUKIGAP,
    'CDLTHRUSTING': talib.CDLTHRUSTING,
    'CDLTRISTAR': talib.CDLTRISTAR,
    'CDLUNIQUE3RIVER': talib.CDLUNIQUE3RIVER,
    'CDLUPSIDEGAP2CROWS': talib.CDLUPSIDEGAP2CROWS,
    'CDLXSIDEGAP3METHODS': talib.CDLXSIDEGAP3METHODS
}

# Cycle Indicator Functions
# https://github.com/wsk2001/ta-lib-python/blob/master/docs/func_groups/cycle_indicators.md
dic_ci_functions = {
    'HT_DCPHASE': talib.HT_DCPHASE,
    'HT_DCPHASE': talib.HT_DCPHASE,
    'HT_PHASOR': talib.HT_PHASOR,
    'HT_SINE': talib.HT_SINE,
    'HT_TRENDMODE': talib.HT_TRENDMODE
}

# Statistic Functions
# https://github.com/wsk2001/ta-lib-python/blob/master/docs/func_groups/statistic_functions.md
dic_statistic_functions = {
    'BETA': talib.BETA,                                 # Beta - high, low
    'CORREL': talib.CORREL,                             # 피어슨의 상관 계수(r) - high, low
    'LINEARREG': talib.LINEARREG,                       # Linear Regression - close
    'LINEARREG_ANGLE': talib.LINEARREG_ANGLE,           # Linear Regression Angle - close
    'LINEARREG_INTERCEPT': talib.LINEARREG_INTERCEPT,   # Linear Regression Intercept - close
    'LINEARREG_SLOPE': talib.LINEARREG_SLOPE,           # Linear Regression Slope - close
    'STDDEV': talib.STDDEV,                             # Standard Deviation - close
    'TSF': talib.TSF,                                   # Time Series Forecast - close
    'VAR': talib.VAR,                                   # Variance - close

}

# Volatility Indicator Functions
# https://github.com/wsk2001/ta-lib-python/blob/master/docs/func_groups/volatility_indicators.md
dic_vi_functions = {
    'ATR': talib.ATR,           # high, low, close
    'NATR': talib.NATR,         # high, low, close
    'TRANGE': talib.TRANGE,     # high, low, close
}
    
# Momentum Indicator Functions
# - 필수 입력 param 의 개 수가 달라 일반화 하기 어려움.
# https://github.com/wsk2001/ta-lib-python/blob/master/docs/func_groups/momentum_indicators.md

# Overlap Studies Functions
# - 필수 입력 param 의 개 수가 달라 일반화 하기 어려움.
# https://github.com/wsk2001/ta-lib-python/blob/master/docs/func_groups/overlap_studies.md

# Price Transform Functions
# - 필수 입력 param 의 개 수가 달라 일반화 하기 어려움.
# https://github.com/wsk2001/ta-lib-python/blob/master/docs/func_groups/price_transform.md



def donchian(df, period=20):
    hi = pd.Series(df['high'])
    lo = pd.Series(df['low'])
    uc = hi.rolling(period, min_periods=period).max()
    lc = lo.rolling(period, min_periods=period).min()
    mc = (uc - lc) / 2
    return lc, mc, uc

def get_HT_DCPERIOD(df, posi=-1):
    '''
    HT_DCPERIOD는 Hilbert Transform Indicator의 Dominant Cycle Period로, 주어진 데이터의 주기적 패턴을 찾는 데 사용되는 지표입니다. HT_DCPERIOD는 Hilbert Transform Indicator를 사용하여 데이터의 진폭을 찾은 다음, 해당 진폭이 가장 큰 주기를 Dominant Cycle Period로 계산합니다. Dominant Cycle Period는 추세의 길이를 측정하는 데 사용할 수 있으며, 추세가 끝나갈 때를 예측하는 데에도 사용할 수 있습니다.

    HT_DCPERIOD는 다음과 같은 방법으로 계산됩니다.

    Hilbert Transform Indicator를 사용하여 데이터의 진폭을 찾습니다.
    해당 진폭이 가장 큰 주기를 Dominant Cycle Period로 계산합니다.
    HT_DCPERIOD는 주로 추세의 길이를 측정하는 데 사용됩니다. Dominant Cycle Period가 길수록 추세가 길어질 가능성이 높습니다. HT_DCPERIOD는 추세가 끝나갈 때를 예측하는 데에도 사용할 수 있습니다. Dominant Cycle Period가 감소하는 경우 추세가 끝나갈 가능성이 높습니다.

    HT_DCPERIOD는 다음과 같은 장점이 있습니다.

    추세의 길이를 측정할 수 있습니다.
    추세가 끝나갈 때를 예측할 수 있습니다.
    사용하기 쉽습니다.
    HT_DCPERIOD는 다음과 같은 단점이 있습니다.

    데이터의 특성에 따라 정확도가 떨어질 수 있습니다.
    다른 지표와 함께 사용하여야 효과적입니다.
    '''
    real = talib.HT_DCPERIOD(df['close'])
    return real



def get_macd(df):
    macd, signal, hist = talib.MACD(df['close'], fastperiod=12, slowperiod=26, signalperiod=9)
    return macd, signal, hist 

def macd_trend(df, posi=-1):
    if len(df) < 26:
        return 'MACD(HOLD)', 0
    
    # Calculate the MACD line
    macd, signal, hist = talib.MACD(df['close'], fastperiod=12, slowperiod=26, signalperiod=9)

    # Calculate the 0 line
    zero_line = 0

    # Determine the trend
    if macd[posi] > signal[posi] and macd[posi] > zero_line:
        return 'MACD(매수)', 100
    elif macd[posi] < signal[posi] and macd[posi] < zero_line:
        return 'MACD(매도)', -100
    else:
        return 'MACD(홀드)', 0

# Python에서 ta-lib를 사용할 때 -100, +100, -200, +200 등과 같은 숫자는 무엇입니까?
# +200 bullish pattern with confirmation
# +100 bullish pattern (most cases)
# 0 none
# -100 bearish pattern
# -200 bearish pattern with confirmation

def get_cdl_patterns(symbol, df, posi=-1):
    # Recognize candlestick patterns.
    res = symbol.upper()
    point = 0

    for key, func in dic_cdl_functions.items():
        lst = func(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
        if lst[posi] != 0:
            res += ', ' + key[3:] + '(' + dic_cdc[key] + ') ' + str(lst[posi])
            point += lst[posi]

    if res != symbol.upper():
        txt, v = macd_trend(df, posi)
        point += v
        res += ', ' + txt

    return res, point    

def rsi_determine_buy_sell(df, posi=-1):
    # RSI 계산
    rsi = talib.RSI(df['close'], timeperiod=14)

    # 매수/매도 판단 로직
    if rsi[posi] < 30:  # RSI가 30 미만이면 매수 신호
        return "RSI 매수"
    elif rsi[posi] > 70:  # RSI가 70 초과이면 매도 신호
        return "RSI 매도"
    else:
        return "RSI 홀드"

# ADX는 0에서 100까지의 값을 가지며, 값이 높을수록 추세가 강하다는 것을 의미합니다
def get_adx(df, posi=-1):
    real = talib.ADX(df['high'], df['low'], df['close'], timeperiod=14)
    return 'ADX ' + f'{real[posi]:.2f}'

def get_bbands(df, posi=-1):
    upperband, middleband, lowerband = talib.BBANDS(df['close'])
    return f'{upperband[posi]:.2f}' , f'{middleband[posi]:.2f}', f'{lowerband[posi]:.2f}'

# 지지선, 저항선
def get_sr(df, posi=-1):
    close_prices = df['close'].values
    high_prices = df['high'].values
    low_prices = df['low'].values
    supports = talib.SAR(high_prices, low_prices)
    return  supports, close_prices[posi]

def get_ohlcv(ticker, interval='day'):
    if not ticker.startswith('KRW-') and not ticker.startswith('BTC-') and not ticker.startswith('USDT-'):
        ticker = 'KRW-' + ticker

    df = pyupbit.get_ohlcv(ticker, interval=interval)

    return df

def main(argv):
    parser = argparse.ArgumentParser(description='캔들 패턴 인식')
    parser.add_argument('-s', '--symbol', required=False, default='ALL', help='심볼 (BTC, ETH, ADA, ..., default=all)')
    parser.add_argument('-p', '--position', required=False, default='1', help='검사일자 (당일 1, 어제 2, ..., default=1)')
    parser.add_argument('-i', '--interval', required=False, default='day', help='check interval (default=day)')

    args = parser.parse_args()
    symbol = args.symbol
    posi = int(args.position) * -1
    interval = args.interval

    now = datetime.now()
    print()
    if posi == -2:
        print('업비트 원화마켓 캔들 패턴 추출 시간 (어제 종가 기준): ' + now.strftime('%Y-%m-%d %H:%M:%S') + ' interval=' + interval)
    elif posi == -1:
        print('업비트 원화마켓 캔들 패턴 추출 시간 (현재 기준): ' + now.strftime('%Y-%m-%d %H:%M:%S') + ' interval=' + interval)
    else:
        dat_posi = str(abs(posi+1)) 
        print('업비트 원화마켓 캔들 패턴 추출 시간 (' + dat_posi + '일전 기준): ' + now.strftime('%Y-%m-%d %H:%M:%S') + ' interval=' + interval)
    print()
    if symbol.upper().startswith("ALL"):
        lst = pyupbit.get_tickers(fiat="KRW")
        lst.sort()

        ptn_score_list = []
        ptn_score_list.clear()

        for v in lst:
            time.sleep(0.1)
            df = get_ohlcv(v[4:], interval)
            patterns, point = get_cdl_patterns(v[4:], df, posi)
            # print(".", end="")
            if patterns != v[4:].upper():
                # print(patterns, point)
                ptn_score_list.append([v[4:], point])
        
        ptn_score_list.sort(key=lambda x: x[1])
        for i in ptn_score_list:
            print(i)
 
    else:
        df = get_ohlcv(symbol, interval)

        patterns, point = get_cdl_patterns(symbol, df, posi)
        patterns += ', ' + rsi_determine_buy_sell(df, posi)

        # indicators = talib.get_function_groups()['Momentum Indicators']
        # indicators = talib.get_function_groups()['Overlap Studies']
        # indicators = talib.get_function_groups()['Pattern Recognition']

        # for indicator in indicators:
        #     print(indicator)

        # print(lst)

        print(patterns, point)

        values = get_HT_DCPERIOD(df)
        for v in values:
            print(v)

        # print()
        # print('donchain start')
        # print(donchian(df))
        # print('donchain end')


    # ptns = talib.get_functions()

    # for ptn in ptns:
    #     if not ptn.startswith("CDL"):
    #         print(ptn)

if __name__ == "__main__":
    main(sys.argv)

