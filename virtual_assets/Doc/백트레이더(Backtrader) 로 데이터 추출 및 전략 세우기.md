# 백트레이더(Backtrader) 로 데이터 추출 및 전략 세우기

출처: [[python\] 백트레이더(Backtrader) 로 데이터 추출 및 전략 세우기 — 검은뿔테, 파랑체크 (tistory.com)](https://dragon1-honey1-wayfarer.tistory.com/entry/python-백트레이더Backtrader-로-데이터-추출-및-전략-세우기)



안녕하세요. 이번엔 백트레이더 (Backtrader) 를 활용해서 필요한 데이터를 추출하고 전략에 반영하는 걸 해보겠습니다. 

 

상대적체결강도 (RSI, 21일 기준) 와 26주 (130일) 지수이동평균선 (EMA) 을 활용하여

 

매수 : RSI < 30 이면서 EMA 의 기울기가 양수 혹은 RSI < 15

매도 : RSI > 70 이면서 EMA 의 기울기가 음수 혹은 RSI > 85

 

전략을 구현해보겠습니다. 

 

추가로 어떤 종목 매매시 어느날 각 지표값들이 어떤 상태인지를 출력하는 함수도 구현해보겠습니다.

 

여러종목 데이터를 얻어오는 부분은 앞의 포스팅을 참고해주세요

 

먼저 전체 코드 입니다.

 ``` py
 class MyStrategy(bt.Strategy):
     def __init__(self):
         self.rsi = dict()
         self.macd = dict()
         self.ema = dict()
         self.rsi_stdBuy = 30
         self.rsi_stdSell = 70
         self.rsi_overBuy = 15
         self.rsi_overSell = 85
         for i, d in enumerate(self.datas):
             self.rsi[d] = bt.indicators.RSI_EMA(d.close, period=21)
             # self.macd[d] = bt.indicators.MACDHisto()
             self.ema[d] = bt.indicators.EMA(d.close, period=130)
 
     def next(self):
         for i, d in enumerate(self.datas):      
             pos = self.getposition(d).size
             ema_grad = self.ema[d] - self.ema[d][-1] # EMA 기준으로 추세 상승(> 0) / 하강(< 0) 판단
             stock_name = d._name[:] # 종목이름 추출
             BS_date = d.datetime.date(0) # 매매 당시 날짜 추출
 
             if not pos: # no market / no orders , 매수한게 없을 경우,
                 # 초기 매수 시점.
                 if (self.rsi[d] < self.rsi_stdBuy and ema_grad > 0) or self.rsi[d] < self.rsi_overBuy:
                     self.order = self.buy(data=d)
                     dashboard(self.rsi[d][0], ema_grad, 0, stock_name, BS_date)
             else: # 산 이력이 있을 경우, 
                 # 추가매수. 내 수수료를 포함한 잔고가 사고자 하는 주식보다 많을 경우,
                 if self.rsi[d] < self.rsi_overBuy: 
                     self.order = self.buy(data=d)
                     dashboard(self.rsi[d][0], ema_grad, 0, stock_name, BS_date)
                 if (self.rsi[d] > self.rsi_stdSell and ema_grad < 0) or self.rsi[d] > self.rsi_overSell:
                     self.order = self.sell(data=d)
                     dashboard(self.rsi[d][0], ema_grad, 1, stock_name, BS_date)
 
 def dashboard(rsi, ema, buySell, stockName, date):
     if buySell == 0: # Buy
         print(f'Buy {stockName}, date : {date}, RSI : {rsi:,.1f}, EMA grad : {ema:,.1f}')
     else: # Sell
         print(f'Sell {stockName}, date : {date}, RSI : {rsi:,.1f}, EMA grad : {ema:,.1f}')
 ```



 

__init__ 함수에선 필요한 파라미터와 사용할 지수들에 대해 정의해줍니다. 

 

next 함수에서 

self.ema[d] 는 당일의 값이고, self.ema[d][-1] 은 하루 전날의 ema 값 입니다. 

기울기(추세) 는 당일에서 전날의 값을 뺀 값이 +/- 인지에 따라 알 수 있습니다. 

stock_name = d._name[:] 은 cerebro.adddata(data, name="") 당시의 이름 입니다.

전 name = ['현대자동차','현대모비스'] 로 하였습니다.

 

dashboard 함수는 매매시 관련 정보를 표출해주는 함수 입니다. 여기선 종목 이름, 매매날짜, RSI, EMA 변화량 (기울기) 를 표출하게 하였습니다. 

 

위 전략을 사용하여 잔고 200만원, 매매 수수료 0.14 % , 주식 매매단위 2주로 했을 때, 코드 및 백테스팅을 돌렸을 때 콘솔 화면과 그래프는 아래와 같이 나타납니다.

 

``` py
cerebro.broker.setcash(2000000)
cerebro.addstrategy(MyStrategy)
cerebro.broker.setcommission(commission=0.0014) # 수수료는 매수 / 매도 합치면 0.28% 정도 이므로, 그 절반인 0.14% 로 하자.
cerebro.addsizer(bt.sizers.SizerFix, stake=2) # 주식 매매단위 2주 설정. 보유한 현금에 비해 매수하려는 주식의 총 매수금액 (주가 X 매매 단위가 크면 매수가 이루어지지 않는다.)

KRW_initial = cerebro.broker.getvalue()
print(f'초기 포트폴리오 값 : {KRW_initial:,.0f} KRW')
cerebro.run() # Cerebro 클래스로 백테스트를 실행한다.
KRW_final = cerebro.broker.getvalue()
profit_ratio = (KRW_final - KRW_initial) / KRW_initial * 100
print(f'종료 포트폴리오 값 : {KRW_final:,.0f} KRW')
print(f'수익률 : {profit_ratio:,.1f} %')
cerebro.plot(style='candlestick') # 백테스트 결과를 캔들스틱 차트로 출력한다.
```



``` sh
초기 포트폴리오 값 : 2,000,000 KRW
Buy 현대자동차, date : 2020-03-12, RSI : 13.0, EMA grad : -430.8
Buy 현대자동차, date : 2020-03-13, RSI : 10.0, EMA grad : -543.3
Buy 현대모비스, date : 2020-03-13, RSI : 13.1, EMA grad : -964.8
Buy 현대자동차, date : 2020-03-16, RSI : 8.8, EMA grad : -600.6
Buy 현대모비스, date : 2020-03-16, RSI : 10.8, EMA grad : -1,102.8
Buy 현대자동차, date : 2020-03-17, RSI : 8.0, EMA grad : -634.2
Buy 현대모비스, date : 2020-03-17, RSI : 9.2, EMA grad : -1,223.3
Buy 현대자동차, date : 2020-03-18, RSI : 6.6, EMA grad : -725.3
Buy 현대모비스, date : 2020-03-18, RSI : 7.6, EMA grad : -1,380.2
Buy 현대자동차, date : 2020-03-19, RSI : 5.4, EMA grad : -830.3
Buy 현대모비스, date : 2020-03-19, RSI : 6.4, EMA grad : -1,542.4
Sell 현대모비스, date : 2020-05-26, RSI : 71.2, EMA grad : -97.5
Sell 현대자동차, date : 2020-08-06, RSI : 87.2, EMA grad : 552.5
Sell 현대자동차, date : 2020-08-07, RSI : 88.1, EMA grad : 582.2
Sell 현대자동차, date : 2020-08-10, RSI : 93.3, EMA grad : 924.5
Sell 현대자동차, date : 2020-08-11, RSI : 94.4, EMA grad : 1,047.7
Sell 현대자동차, date : 2021-01-08, RSI : 85.6, EMA grad : 1,213.5
Sell 현대모비스, date : 2021-01-08, RSI : 88.6, EMA grad : 1,900.0
Sell 현대자동차, date : 2021-01-11, RSI : 89.1, EMA grad : 1,523.2
Buy 현대자동차, date : 2021-03-26, RSI : 28.2, EMA grad : 137.2
Buy 현대자동차, date : 2021-08-20, RSI : 14.3, EMA grad : -333.6
종료 포트폴리오 값 : 4,001,087 KRW
수익률 : 100.1 %
C:\Users\hs205\AppData\Local\Programs\Python\Python39\lib\site-packages\matplotlib\backends\backend_agg.py:240: RuntimeWarning: Glyph 54788 missing from current font.
  font.set_text(s, 0.0, flags=flags)
C:\Users\hs205\AppData\Local\Programs\Python\Python39\lib\site-packages\matplotlib\backends\backend_agg.py:240: RuntimeWarning: Glyph 45824 missing from current font.
  font.set_text(s, 0.0, flags=flags)
C:\Users\hs205\AppData\Local\Programs\Python\Python39\lib\site-packages\matplotlib\backends\backend_agg.py:240: RuntimeWarning: Glyph 51088 missing from current font.     
  font.set_text(s, 0.0, flags=flags)
C:\Users\hs205\AppData\Local\Programs\Python\Python39\lib\site-packages\matplotlib\backends\backend_agg.py:240: RuntimeWarning: Glyph 46041 missing from current font.     
  font.set_text(s, 0.0, flags=flags)
C:\Users\hs205\AppData\Local\Programs\Python\Python39\lib\site-packages\matplotlib\backends\backend_agg.py:240: RuntimeWarning: Glyph 52264 missing from current font.     
  font.set_text(s, 0.0, flags=flags)
C:\Users\hs205\AppData\Local\Programs\Python\Python39\lib\site-packages\matplotlib\backends\backend_agg.py:240: RuntimeWarning: Glyph 47784 missing from current font.     
  font.set_text(s, 0.0, flags=flags)
C:\Users\hs205\AppData\Local\Programs\Python\Python39\lib\site-packages\matplotlib\backends\backend_agg.py:240: RuntimeWarning: Glyph 48708 missing from current font.     
  font.set_text(s, 0.0, flags=flags)
C:\Users\hs205\AppData\Local\Programs\Python\Python39\lib\site-packages\matplotlib\backends\backend_agg.py:240: RuntimeWarning: Glyph 49828 missing from current font.     
  font.set_text(s, 0.0, flags=flags)
C:\Users\hs205\AppData\Local\Programs\Python\Python39\lib\site-packages\matplotlib\backends\backend_agg.py:203: RuntimeWarning: Glyph 54788 missing from current font.     
  font.set_text(s, 0, flags=flags)
C:\Users\hs205\AppData\Local\Programs\Python\Python39\lib\site-packages\matplotlib\backends\backend_agg.py:203: RuntimeWarning: Glyph 45824 missing from current font.     
  font.set_text(s, 0, flags=flags)
C:\Users\hs205\AppData\Local\Programs\Python\Python39\lib\site-packages\matplotlib\backends\backend_agg.py:203: RuntimeWarning: Glyph 51088 missing from current font.     
  font.set_text(s, 0, flags=flags)
C:\Users\hs205\AppData\Local\Programs\Python\Python39\lib\site-packages\matplotlib\backends\backend_agg.py:203: RuntimeWarning: Glyph 46041 missing from current font.     
  font.set_text(s, 0, flags=flags)
C:\Users\hs205\AppData\Local\Programs\Python\Python39\lib\site-packages\matplotlib\backends\backend_agg.py:203: RuntimeWarning: Glyph 52264 missing from current font.     
  font.set_text(s, 0, flags=flags)
C:\Users\hs205\AppData\Local\Programs\Python\Python39\lib\site-packages\matplotlib\backends\backend_agg.py:203: RuntimeWarning: Glyph 47784 missing from current font.     
  font.set_text(s, 0, flags=flags)
C:\Users\hs205\AppData\Local\Programs\Python\Python39\lib\site-packages\matplotlib\backends\backend_agg.py:203: RuntimeWarning: Glyph 48708 missing from current font.     
  font.set_text(s, 0, flags=flags)
C:\Users\hs205\AppData\Local\Programs\Python\Python39\lib\site-packages\matplotlib\backends\backend_agg.py:203: RuntimeWarning: Glyph 49828 missing from current font.     
  font.set_text(s, 0, flags=flags)
```



수익률은 약 100% 가 나왔습니다. 다만 매수 시점이 2020년에 되서야 처음 나온걸 보면 종목변경이나 전략 수정이 필요할 것 같네요. 콘솔 및에 나온 warning 메시지는 한글 폰트가 깨져서 나온 메시지 입니다. 