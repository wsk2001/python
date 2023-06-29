import talib 
import calendar
import getopt
import sys, time
import pyupbit
from common.utils import market_code
from datetime import datetime
import argparse
# import matplotlib.pyplot as plt

def macd(df):
    macd = df['close'].ewm(span=12, min_periods=9).mean() - df['close'].ewm(span=26, min_periods=19).mean()

    # MACD 선과 0선을 그래프로 표시합니다.
    # plt.plot(macd)
    # plt.axhline(0, color='red')

    # MACD 선이 0선을 상향 돌파하는 지점을 찾습니다.
    up_crossover = macd.index[macd > 0].min()

    # MACD 선이 0선을 하향 돌파하는 지점을 찾습니다.
    down_crossover = macd.index[macd < 0].min()

    # MACD 선이 0선을 상향 돌파한 후, 하락 반전이 발생했는지 확인합니다.
    if up_crossover < down_crossover:
        res = 'MACD UP'
    else:
        res = 'MACD DOWN'

    return res

def get_candlestick_pattern(symbol, df, posi=-1):
    # Recognize candlestick patterns.
    res = symbol.upper()

    lst = talib.CDL2CROWS(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDL2CROWS'
    
    lst = talib.CDL3BLACKCROWS(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDL3BLACKCROWS'

    lst = talib.CDL3INSIDE(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDL3INSIDE'


    lst = talib.CDL3LINESTRIKE(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDL3LINESTRIKE'

    lst = talib.CDL3OUTSIDE(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDL3OUTSIDE'

    lst = talib.CDL3STARSINSOUTH(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDL3STARSINSOUTH'

    lst = talib.CDL3WHITESOLDIERS(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDL3WHITESOLDIERS'

    lst = talib.CDLABANDONEDBABY(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLABANDONEDBABY'


    lst = talib.CDLADVANCEBLOCK(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLADVANCEBLOCK'


    lst = talib.CDLBELTHOLD(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLBELTHOLD'

    lst = talib.CDLBREAKAWAY(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLBREAKAWAY'


    lst = talib.CDLCLOSINGMARUBOZU(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLCLOSINGMARUBOZU'


    lst = talib.CDLCONCEALBABYSWALL(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLCONCEALBABYSWALL'


    lst = talib.CDLCOUNTERATTACK(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLCOUNTERATTACK'


    lst = talib.CDLDARKCLOUDCOVER(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLDARKCLOUDCOVER'


    lst = talib.CDLDOJI(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLDOJI'


    lst = talib.CDLDOJISTAR(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLDOJISTAR'


    lst = talib.CDLDRAGONFLYDOJI(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLDRAGONFLYDOJI'


    lst = talib.CDLENGULFING(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLENGULFING'

    lst = talib.CDLEVENINGDOJISTAR(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLEVENINGDOJISTAR'

    lst = talib.CDLEVENINGSTAR(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLEVENINGSTAR'


    lst = talib.CDLGAPSIDESIDEWHITE(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLGAPSIDESIDEWHITE'

    lst = talib.CDLGRAVESTONEDOJI(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLGRAVESTONEDOJI'

    lst = talib.CDLHAMMER(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLHAMMER'

    lst = talib.CDLHANGINGMAN(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLHANGINGMAN'

    lst = talib.CDLHARAMI(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLHARAMI'

    lst = talib.CDLHARAMICROSS(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLHARAMICROSS'


    lst = talib.CDLHIGHWAVE(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLHIGHWAVE'

    lst = talib.CDLHIKKAKE(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLHIKKAKE'

    lst = talib.CDLHIKKAKEMOD(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLHIKKAKEMOD'

    lst = talib.CDLHOMINGPIGEON(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLHOMINGPIGEON'

    lst = talib.CDLIDENTICAL3CROWS(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLIDENTICAL3CROWS'

    lst = talib.CDLINNECK(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLINNECK'

    lst = talib.CDLINVERTEDHAMMER(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLINVERTEDHAMMER'

    lst = talib.CDLKICKING(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLKICKING'

    lst = talib.CDLKICKINGBYLENGTH(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLKICKINGBYLENGTH'

    lst = talib.CDLLADDERBOTTOM(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLLADDERBOTTOM'

    lst = talib.CDLLONGLEGGEDDOJI(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLLONGLEGGEDDOJI'

    lst = talib.CDLLONGLINE(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLLONGLINE'


    lst = talib.CDLMARUBOZU(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLMARUBOZU'

    lst = talib.CDLMATCHINGLOW(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLMATCHINGLOW'

    lst = talib.CDLMATHOLD(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLMATHOLD'

    lst = talib.CDLMORNINGDOJISTAR(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLMORNINGDOJISTAR'

    lst = talib.CDLMORNINGSTAR(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLMORNINGSTAR'

    lst = talib.CDLONNECK(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLONNECK'

    lst = talib.CDLPIERCING(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLPIERCING'

    lst = talib.CDLRICKSHAWMAN(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLRICKSHAWMAN'

    lst = talib.CDLRISEFALL3METHODS(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLRISEFALL3METHODS'

    lst = talib.CDLSEPARATINGLINES(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLSEPARATINGLINES'

    lst = talib.CDLSHOOTINGSTAR(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLSHOOTINGSTAR'

    lst = talib.CDLSHORTLINE(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLSHORTLINE'

    lst = talib.CDLSPINNINGTOP(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLSPINNINGTOP'

    lst = talib.CDLSTALLEDPATTERN(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLSTALLEDPATTERN'

    lst = talib.CDLSTICKSANDWICH(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLSTICKSANDWICH'

    lst = talib.CDLTAKURI(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLTAKURI'

    lst = talib.CDLTASUKIGAP(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLTASUKIGAP'

    lst = talib.CDLTHRUSTING(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLTHRUSTING'

    lst = talib.CDLTRISTAR(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLTRISTAR'

    lst = talib.CDLUNIQUE3RIVER(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLUNIQUE3RIVER'

    lst = talib.CDLUPSIDEGAP2CROWS(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLUPSIDEGAP2CROWS'

    lst = talib.CDLXSIDEGAP3METHODS(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLXSIDEGAP3METHODS'

    if res == symbol.upper():
        res += ', ' + 'NO Pattern'
    else:
        res += ', ' + macd(df)
    
    # 캔들스틱 패턴을 반환합니다.
    # 미완성 (마지막 날짜 Data 만 취합 해서 확인 할 수 있도록 수정 필요)
    return res

def get_ohlcv(ticker):
    if not ticker.startswith('KRW-') and not ticker.startswith('BTC-') and not ticker.startswith('USDT-'):
        ticker = 'KRW-' + ticker

    df = pyupbit.get_ohlcv(ticker)

    return df

def main(argv):
    parser = argparse.ArgumentParser(description='캔들 패턴 인식')
    parser.add_argument('-s', '--symbol', required=False, default='ALL', help='심볼 (BTC, ETH, ADA, ..., default=all)')
    parser.add_argument('-p', '--position', required=False, default='1', help='검사일자 (당일 1, 어제 2, ..., default=1)')


    args = parser.parse_args()
    symbol = args.symbol
    posi = int(args.position) * -1

    if symbol.upper().startswith("ALL"):
        lst = pyupbit.get_tickers(fiat="KRW")
        lst.sort()

        for v in lst:
            time.sleep(0.1)
            ohlcv = get_ohlcv(v[4:])
            patterns = get_candlestick_pattern(v[4:], ohlcv, posi)
            print(patterns)

    else:
        # 캔들스틱 데이터를 가져옵니다.
        ohlcv = get_ohlcv(symbol)

        # 캔들스틱 패턴을 인식합니다.
        patterns = get_candlestick_pattern(symbol, ohlcv, posi)

        # 캔들스틱 패턴을 출력합니다.
        print(patterns)
    
    # ptns = talib.get_functions()

    # for ptn in ptns:
    #     if ptn.startswith("CDL"):
    #         print(ptn)

if __name__ == "__main__":
    main(sys.argv)

