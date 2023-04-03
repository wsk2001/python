import pybithumb

def bull_market(ticker):
    df = pybithumb.get_ohlcv(ticker)
    ma5 = df['close'].rolling(window=5).mean()
    price = pybithumb.get_current_price(ticker)
    last_ma5 = ma5[-2]

    if price > last_ma5:
        return True
    else:
        return False


tickers = pybithumb.get_tickers()
plus_cnt = 0
minus_cnt = 0;
for ticker in tickers:
    is_bull = bull_market(ticker)
    if is_bull:
        print(ticker, " 상승장")
        plus_cnt = plus_cnt + 1
    else:
        print(ticker, " 하락장")
        minus_cnt = minus_cnt + 1

print('')
print('total =', str(plus_cnt+minus_cnt), 'plus =', str(plus_cnt), 'minus =', str(minus_cnt))
