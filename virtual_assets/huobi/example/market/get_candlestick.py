from huobi.client.market import MarketClient
from huobi.constant import *
from huobi.utils import *

market_client = MarketClient(init_log=True)
#interval = CandlestickInterval.MIN5
interval = CandlestickInterval.DAY1
# symbol = "ethusdt"
symbol = "rndrusdt"
list_obj = market_client.get_candlestick(symbol, interval, 1)
# LogInfo.output("---- {interval} candlestick for {symbol} ----".format(interval=interval, symbol=symbol))
# LogInfo.output_list(list_obj)

o = list_obj[0].open
h = list_obj[0].high
l = list_obj[0].low
c = list_obj[0].close
r = ((list_obj[0].close / list_obj[0].open) - 1.0) * 100.0
print(f'{symbol}, {o}, {h}, {l}, {c}, {r:3.3f}')

symbol = "axsusdt"
list_obj = market_client.get_candlestick(symbol, interval, 1)
# LogInfo.output("---- {interval} candlestick for {symbol} ----".format(interval=interval, symbol=symbol))
# LogInfo.output_list(list_obj)

o = list_obj[0].open
h = list_obj[0].high
l = list_obj[0].low
c = list_obj[0].close
r = ((list_obj[0].close / list_obj[0].open) - 1.0) * 100.0
print(f'{symbol}, {o}, {h}, {l}, {c}, {r:3.3f}')

