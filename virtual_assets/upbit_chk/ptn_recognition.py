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
        res += ', ' + macd_trend(df, posi) # + ', ' + rsi_determine_buy_sell(df, posi)

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
            ohlcv = get_ohlcv(v[4:], interval)
            patterns, point = get_cdl_patterns(v[4:], ohlcv, posi)
            if patterns != v[4:].upper():
                # print(patterns, point)
                ptn_score_list.append([v[4:], point])
        
        ptn_score_list.sort(key=lambda x: x[1])
        for i in ptn_score_list:
            print(i)

    else:
        # 캔들스틱 데이터를 가져옵니다.
        ohlcv = get_ohlcv(symbol, interval)

        # 캔들스틱 패턴을 인식합니다.
        patterns, point = get_cdl_patterns(symbol, ohlcv, posi)

        # 캔들스틱 패턴을 출력합니다.
        print(patterns, point)

    # ptns = talib.get_functions()

    # for ptn in ptns:
    #     if not ptn.startswith("CDL"):
    #         print(ptn)

if __name__ == "__main__":
    main(sys.argv)

