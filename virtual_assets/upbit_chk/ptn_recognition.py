import talib 
import calendar
import getopt
import sys, time
import pyupbit
from common.utils import market_code
from datetime import datetime
import argparse
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

def get_macd(df):
    macd, signal, hist = talib.MACD(df['close'], fastperiod=12, slowperiod=26, signalperiod=9)
    return macd, signal, hist 

def macd_trend(df, posi=-1):
    if len(df) < 26:
        return 'MACD no signal'
    
    # Calculate the MACD line
    macd_line = df['close'].ewm(span=12, min_periods=12).mean() - df['close'].ewm(span=26, min_periods=26).mean()

    # Calculate the signal line
    signal_line = macd_line.ewm(span=9, min_periods=9).mean()

    # Calculate the 0 line
    zero_line = 0

    # Determine the trend
    if macd_line[posi] > signal_line[posi] and macd_line[posi] > zero_line:
        return 'MACD 매수'
    elif macd_line[posi] < signal_line[posi] and macd_line[posi] < zero_line:
        return 'MACD 매도'
    else:
        return 'MACD 홀드'

def get_candlestick_pattern(symbol, df, posi=-1):
    # Recognize candlestick patterns.
    res = symbol.upper()

    lst = talib.CDL2CROWS(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDL2CROWS(' + dic_cdc['CDL2CROWS'] + ')'
    
    lst = talib.CDL3BLACKCROWS(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDL3BLACKCROWS(' + dic_cdc['CDL3BLACKCROWS'] + ')'

    lst = talib.CDL3INSIDE(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDL3INSIDE(' + dic_cdc['CDL3INSIDE'] + ')'


    lst = talib.CDL3LINESTRIKE(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDL3LINESTRIKE(' + dic_cdc['CDL3LINESTRIKE'] + ')'

    lst = talib.CDL3OUTSIDE(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDL3OUTSIDE(' + dic_cdc['CDL3OUTSIDE'] + ')'

    lst = talib.CDL3STARSINSOUTH(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDL3STARSINSOUTH(' + dic_cdc['CDL3STARSINSOUTH'] + ')'

    lst = talib.CDL3WHITESOLDIERS(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDL3WHITESOLDIERS(' + dic_cdc['CDL3WHITESOLDIERS'] + ')'

    lst = talib.CDLABANDONEDBABY(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLABANDONEDBABY(' + dic_cdc['CDLABANDONEDBABY'] + ')'


    lst = talib.CDLADVANCEBLOCK(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLADVANCEBLOCK(' + dic_cdc['CDLADVANCEBLOCK'] + ')'


    lst = talib.CDLBELTHOLD(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLBELTHOLD(' + dic_cdc['CDLBELTHOLD'] + ')'

    lst = talib.CDLBREAKAWAY(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLBREAKAWAY(' + dic_cdc['CDLBREAKAWAY'] + ')'


    lst = talib.CDLCLOSINGMARUBOZU(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLCLOSINGMARUBOZU(' + dic_cdc['CDLCLOSINGMARUBOZU'] + ')'


    lst = talib.CDLCONCEALBABYSWALL(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLCONCEALBABYSWALL(' + dic_cdc['CDLCONCEALBABYSWALL'] + ')'


    lst = talib.CDLCOUNTERATTACK(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLCOUNTERATTACK(' + dic_cdc['CDLCOUNTERATTACK'] + ')'


    lst = talib.CDLDARKCLOUDCOVER(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLDARKCLOUDCOVER(' + dic_cdc['CDLDARKCLOUDCOVER'] + ')'


    lst = talib.CDLDOJI(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLDOJI(' + dic_cdc['CDLDOJI'] + ')'


    lst = talib.CDLDOJISTAR(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLDOJISTAR(' + dic_cdc['CDLDOJISTAR'] + ')'


    lst = talib.CDLDRAGONFLYDOJI(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLDRAGONFLYDOJI(' + dic_cdc['CDLDRAGONFLYDOJI'] + ')'


    lst = talib.CDLENGULFING(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLENGULFING(' + dic_cdc['CDLENGULFING'] + ')'

    lst = talib.CDLEVENINGDOJISTAR(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLEVENINGDOJISTAR(' + dic_cdc['CDLEVENINGDOJISTAR'] + ')'

    lst = talib.CDLEVENINGSTAR(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLEVENINGSTAR(' + dic_cdc['CDLEVENINGSTAR'] + ')'

    lst = talib.CDLGAPSIDESIDEWHITE(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLGAPSIDESIDEWHITE(' + dic_cdc['CDLGAPSIDESIDEWHITE'] + ')'

    lst = talib.CDLGRAVESTONEDOJI(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLGRAVESTONEDOJI(' + dic_cdc['CDLGRAVESTONEDOJI'] + ')'

    lst = talib.CDLHAMMER(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLHAMMER(' + dic_cdc['CDLHAMMER'] + ')'

    lst = talib.CDLHANGINGMAN(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLHANGINGMAN(' + dic_cdc['CDLHANGINGMAN'] + ')'

    lst = talib.CDLHARAMI(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLHARAMI(' + dic_cdc['CDLHARAMI'] + ')'

    lst = talib.CDLHARAMICROSS(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLHARAMICROSS(' + dic_cdc['CDLHARAMICROSS'] + ')'


    lst = talib.CDLHIGHWAVE(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLHIGHWAVE(' + dic_cdc['CDLHIGHWAVE'] + ')'

    lst = talib.CDLHIKKAKE(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLHIKKAKE(' + dic_cdc['CDLHIKKAKE'] + ')'

    lst = talib.CDLHIKKAKEMOD(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLHIKKAKEMOD(' + dic_cdc['CDLHIKKAKEMOD'] + ')'

    lst = talib.CDLHOMINGPIGEON(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLHOMINGPIGEON(' + dic_cdc['CDLHOMINGPIGEON'] + ')'

    lst = talib.CDLIDENTICAL3CROWS(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLIDENTICAL3CROWS(' + dic_cdc['CDLIDENTICAL3CROWS'] + ')'

    lst = talib.CDLINNECK(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLINNECK(' + dic_cdc['CDLINNECK'] + ')'

    lst = talib.CDLINVERTEDHAMMER(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLINVERTEDHAMMER(' + dic_cdc['CDLINVERTEDHAMMER'] + ')'

    lst = talib.CDLKICKING(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLKICKING(' + dic_cdc['CDLKICKING'] + ')'

    lst = talib.CDLKICKINGBYLENGTH(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLKICKINGBYLENGTH(' + dic_cdc['CDLKICKINGBYLENGTH'] + ')'

    lst = talib.CDLLADDERBOTTOM(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLLADDERBOTTOM(' + dic_cdc['CDLLADDERBOTTOM'] + ')'

    lst = talib.CDLLONGLEGGEDDOJI(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLLONGLEGGEDDOJI(' + dic_cdc['CDLLONGLEGGEDDOJI'] + ')'

    lst = talib.CDLLONGLINE(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLLONGLINE(' + dic_cdc['CDLLONGLINE'] + ')'


    lst = talib.CDLMARUBOZU(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLMARUBOZU(' + dic_cdc['CDLMARUBOZU'] + ')'

    lst = talib.CDLMATCHINGLOW(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLMATCHINGLOW(' + dic_cdc['CDLMATCHINGLOW'] + ')'

    lst = talib.CDLMATHOLD(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLMATHOLD(' + dic_cdc['CDLMATHOLD'] + ')'

    lst = talib.CDLMORNINGDOJISTAR(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLMORNINGDOJISTAR(' + dic_cdc['CDLMORNINGDOJISTAR'] + ')'

    lst = talib.CDLMORNINGSTAR(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLMORNINGSTAR(' + dic_cdc['CDLMORNINGSTAR'] + ')'

    lst = talib.CDLONNECK(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLONNECK(' + dic_cdc['CDLONNECK'] + ')'

    lst = talib.CDLPIERCING(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLPIERCING(' + dic_cdc['CDLPIERCING'] + ')'

    lst = talib.CDLRICKSHAWMAN(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLRICKSHAWMAN(' + dic_cdc['CDLRICKSHAWMAN'] + ')'

    lst = talib.CDLRISEFALL3METHODS(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLRISEFALL3METHODS(' + dic_cdc['CDLRISEFALL3METHODS'] + ')'

    lst = talib.CDLSEPARATINGLINES(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLSEPARATINGLINES(' + dic_cdc['CDLSEPARATINGLINES'] + ')'

    lst = talib.CDLSHOOTINGSTAR(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLSHOOTINGSTAR(' + dic_cdc['CDLSHOOTINGSTAR'] + ')'

    lst = talib.CDLSHORTLINE(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLSHORTLINE(' + dic_cdc['CDLSHORTLINE'] + ')'

    lst = talib.CDLSPINNINGTOP(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLSPINNINGTOP(' + dic_cdc['CDLSPINNINGTOP'] + ')'

    lst = talib.CDLSTALLEDPATTERN(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLSTALLEDPATTERN(' + dic_cdc['CDLSTALLEDPATTERN'] + ')'

    lst = talib.CDLSTICKSANDWICH(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLSTICKSANDWICH(' + dic_cdc['CDLSTICKSANDWICH'] + ')'

    lst = talib.CDLTAKURI(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLTAKURI(' + dic_cdc['CDLTAKURI'] + ')'

    lst = talib.CDLTASUKIGAP(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLTASUKIGAP(' + dic_cdc['CDLTASUKIGAP'] + ')'

    lst = talib.CDLTHRUSTING(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLTHRUSTING(' + dic_cdc['CDLTHRUSTING'] + ')'

    lst = talib.CDLTRISTAR(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLTRISTAR(' + dic_cdc['CDLTRISTAR'] + ')'

    lst = talib.CDLUNIQUE3RIVER(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLUNIQUE3RIVER(' + dic_cdc['CDLUNIQUE3RIVER'] + ')'

    lst = talib.CDLUPSIDEGAP2CROWS(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLUPSIDEGAP2CROWS(' + dic_cdc['CDLUPSIDEGAP2CROWS'] + ')'

    lst = talib.CDLXSIDEGAP3METHODS(high=df['high'], low=df['low'], open=df['open'], close=df['close'])
    if lst[posi] != 0:
        res += ', ' + 'CDLXSIDEGAP3METHODS(' + dic_cdc['CDLXSIDEGAP3METHODS'] + ')'

    if res != symbol.upper():
        res += ', ' + macd_trend(df, posi) # + ', ' + rsi_determine_buy_sell(df, posi)
    
    # 캔들스틱 패턴을 반환합니다.
    # 미완성 (마지막 날짜 Data 만 취합 해서 확인 할 수 있도록 수정 필요)
    return res

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
    print('업비트 원화마켓 캔들 패턴 추출 시간: ' + now.strftime('%Y-%m-%d %H:%M:%S'))
    print()
    if symbol.upper().startswith("ALL"):
        lst = pyupbit.get_tickers(fiat="KRW")
        lst.sort()

        for v in lst:
            time.sleep(0.1)
            ohlcv = get_ohlcv(v[4:], interval)
            patterns = get_candlestick_pattern(v[4:], ohlcv, posi)
            if patterns != v[4:].upper():
                print(patterns)

    else:
        # 캔들스틱 데이터를 가져옵니다.
        ohlcv = get_ohlcv(symbol, interval)

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

