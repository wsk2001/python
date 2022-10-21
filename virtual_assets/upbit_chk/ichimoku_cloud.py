import pandas as pd
import datetime
import requests
import pandas as pd
import time, sys
import webbrowser
import argparse
from common.utils import market_code
import talib as ta
import pyupbit


def ich(ticker, count):
    url = "https://api.upbit.com/v1/candles/days"
    
    querystring = {"market":f'KRW-{ticker}',"count":f"{count}"}
    
    response = requests.request("GET", url, params=querystring)
    
    data = response.json()
    
    df = pd.DataFrame(data)
    if len(df) < 50:
        return
    
    df = df.iloc[::-1]

    high_prices = df['high_price']
    close_prices = df['trade_price']
    low_prices = df['low_price']
    dates = df.index
    
    nine_period_high = df['high_price'].rolling(window=9).max()
    nine_period_low = df['low_price'].rolling(window=9).min()
    df['tenkan_sen'] = (nine_period_high + nine_period_low) /2
    
    period26_high = high_prices.rolling(window=26).max()
    period26_low = low_prices.rolling(window=26).min()
    df['kijun_sen'] = (period26_high + period26_low) / 2
    
    df['senkou_span_a'] = ((df['tenkan_sen'] + df['kijun_sen']) / 2).shift(26)
    
    
    period52_high = high_prices.rolling(window=52).max()
    period52_low = low_prices.rolling(window=52).min()
    df['senkou_span_b'] = ((period52_high + period52_low) / 2).shift(26)
    
    
    df['chikou_span'] = close_prices.shift(-26)
    
    print('symbol:', ticker)
    print('전환선: ', round(df['tenkan_sen'].iloc[-1],2))
    print('기준선: ', round(df['kijun_sen'].iloc[-1],2))
    print('후행스팬: ', round(df['chikou_span'].iloc[-27],2))
    print('선행스팬1: ', round(df['senkou_span_a'].iloc[-1],2))
    print('선행스팬2: ', round(df['senkou_span_b'].iloc[-1],2))
    print('')



def main(argv):
    parser = argparse.ArgumentParser(description='옵션 지정 방법')
    parser.add_argument('--count', required=False, default=100, help='data gettering size (default=100)')
    parser.add_argument('--interval', required=False, default='day',
                        help='candle 종류 (day, week, month, minute1, ...)')

    args = parser.parse_args()
    count = int(args.count)
    interval = args.interval

    print('symbol, macd, signal, remark')
    try:
        code_list, _, _ = market_code()
        code_list.sort()
        for t in code_list:
            ich(t[4:], count)
            time.sleep(0.3)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main(sys.argv)
