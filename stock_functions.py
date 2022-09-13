# -*- coding: utf-8 -*-
"""
Created on Thu May  7 20:31:53 2020

@author: remib
"""
import numpy as np
from datetime import datetime as dt1
import datetime as dt2
import yahooquery as yq
import matplotlib.pyplot as plt
import matplotlib.patches
import talib as ta
import math
from pandas.plotting import register_matplotlib_converters
import pandas as pd
import dateutil.relativedelta
from yahoo_fin import stock_info as si 
import urllib.request as urllib2
from urllib.error import HTTPError

register_matplotlib_converters()

class Equity: 
    def __init__(self, ticker):
        self.ticker = ticker
        self.tickerData = yq.Ticker(ticker)
        
        #Or error (fix for github version)
        url = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/"+self.ticker+"?modules=financialData&formatted=false&lang=en-US&region=US&corsDomain=finance.yahoo.com"
        try:
            urllib2.urlopen(url, timeout=2)
            self.current_price = self.tickerData.financial_data[ticker]["currentPrice"]
        except HTTPError as err:
            self.current_price = si.get_live_price(self.ticker)   
        except Exception as e:
            print("error", e)
            self.current_price = self.tickerData.financial_data[ticker]["currentPrice"]
        
        if ticker == "^GSPC" or ticker=="vusa.l":
            self.company_name = "S&P"
        else:
            stock_quote_type = self.tickerData.quote_type[ticker]
            self.company_name = stock_quote_type["longName"]
            
        #Get Earnings date
    
        url = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/"+self.ticker+"?modules=calendarEvents&formatted=false&lang=en-US&region=US&corsDomain=finance.yahoo.com"
        next_earning_date = 0
        try:
            urllib2.urlopen(url, timeout=4)
            earnings_date_array = self.tickerData.calendar_events[self.ticker]["earnings"]["earningsDate"]
            
            for earnings_date in earnings_date_array:
                date = dt1.utcfromtimestamp(earnings_date)
                if date > dt1.today():
                    next_earning_date = date
                    break
        except HTTPError as err:
            print(err)
            
        self.next_earning_date = next_earning_date
        
    def get_history(self, start_date="", end_date=dt1.today().strftime('%Y-%m-%d'), period="1d", show_plot=0): 
        tickerData = self.tickerData
        
        if start_date == "":
            start_date = dt1.today() - dt2.timedelta(days=365)
            start_date_ta = start_date - dt2.timedelta(days=100)
        else:
            start_date_ta = dt1.strptime(start_date, '%Y-%m-%d') - dt2.timedelta(days=100)
        
        print("end", end_date)
        
        tickerDf = tickerData.history(period=period, start=start_date, end=end_date)
        print(start_date)
        df = tickerDf[["close"]]
        df.reset_index(level=0, inplace=True)
        df.columns=['ds','y']
        price_array = df.y
        date_array = df.ds
            
        tickerDf_ta = tickerData.history(period=period, start=start_date_ta, end=end_date)
        df_ta = tickerDf_ta[["close"]]
        df_ta.reset_index(level=0, inplace=True)
        df_ta.columns=['ds_ta','y_ta']
        price_array_ta = df_ta.y_ta
        date_array_ta = df_ta.ds_ta

        idx = 0
        for price in price_array_ta:

            if date_array_ta[idx] == date_array[0]:
                #print(price, date_array_ta[idx])
                ta_start_idx = idx
                
            
            idx+=1
            
        
        self.tickerDf = tickerDf
        self.price_array = price_array
        self.date_array = date_array
        self.volume_array = tickerDf["volume"]
        self.ta_start_idx = ta_start_idx
        self.price_array_ta = price_array_ta
        self.date_array_ta = date_array_ta
        self.start_date = start_date
        self.end_date = end_date
        
        return tickerDf
    
    def get_ma_signal(self, show_plot=0):
        #Start date needs to be 50 days before any crossovers you want to see (could use start date of company)
        price_array = self.price_array
        date_array = self.date_array
        company_name = self.company_name
        ta_start_idx = self.ta_start_idx
        price_array_ta = self.price_array_ta
        
        #Get EMA and crossing points
        
        ema_50 = ta.EMA(price_array_ta, timeperiod = 50)
        ema_10 = ta.EMA(price_array_ta, timeperiod = 10)
        ema_50 = ema_50[ta_start_idx:]
        ema_10 = ema_10[ta_start_idx:]
        ema_10 = ema_10.reset_index(drop=True)
        ema_50 = ema_50.reset_index(drop=True)
        
        diff_array = ema_10 - ema_50
        
        
        exp10 = price_array_ta.ewm(span=10, adjust=False).mean()
        exp50 = price_array_ta.ewm(span=50, adjust=False).mean()
        exp10 = exp10[ta_start_idx:]
        exp50 = exp10[ta_start_idx:]
        exp10 = exp10.reset_index(drop=True)
        exp50 = exp10.reset_index(drop=True)
        exp10 = price_array.ewm(span=10, adjust=False).mean()
        exp50 = price_array.ewm(span=50, adjust=False).mean()
        diff_exp_array = exp10 - exp50
        
        """
        if self.ticker == "bas.de" or self.ticker=="rr.l":
            fig, ax = plt.subplots()
            plt.title(company_name+" exp")
            plt.xlabel("Date")
            plt.ylabel("Price")
            plt.grid(b=True, which="both", axis="both")
            plt.plot(date_array, price_array, color="blue", label="price")
            plt.plot(date_array, exp50, color="black", label="50-day EMA")
            plt.plot(date_array, exp10, color="red", label="10-day EMA")
            plt.legend(loc="best")
            fig.autofmt_xdate()
            plt.show()
        """
        
        idx = 0
        crossover_array = []
        crossover_idx_array = []
        diff_percentage_array = []
        
        for diff in diff_exp_array:
            #print(diff)
            
            if math.isnan(diff):
                diff_percentage_array = np.append(diff_percentage_array, 0)
            else:
                diff_percentage = (diff/exp10[idx])*100
                diff_percentage_array = np.append(diff_percentage_array, diff_percentage)
                
                if idx > 0:
                    if diff > 0 and diff_exp_array[idx-1] < 0:
                        crossover_array = np.append(crossover_array, "bullish")
                        #print("bullish")
                        crossover_idx_array = np.append(crossover_idx_array, idx)
                    elif diff < 0 and diff_exp_array[idx-1] > 0:
                        crossover_array = np.append(crossover_array, "bearish")
                        #print("bearish")
                        crossover_idx_array = np.append(crossover_idx_array, idx)
                    
            idx += 1
        
        try:
            ma_signal = crossover_array[-1] #here
            ma_crossover = date_array[crossover_idx_array[-1]]
        except IndexError as err:
            print(err)
            ma_signal = ""
            print(crossover_array)
            ma_crossover = ""
            
        
        
        if ma_crossover == dt1.today():
            print("Moving Average crossover today")
        
        #EMA trend
        if diff_exp_array[np.size(diff_exp_array)-1] > diff_exp_array[np.size(diff_exp_array)-2]:
            ma_trend = "diverging"
        elif diff_exp_array[np.size(diff_exp_array)-1] < diff_exp_array[np.size(diff_exp_array)-2]:
            ma_trend= "converging"
            
        
        #Current diff
        ma_seperation = np.abs((diff_exp_array[np.size(diff_exp_array)-1]/exp10[np.size(exp10)-1])*100)
        
        #Show graph 
        if show_plot == 1:
            fig, ax = plt.subplots()
            plt.title(company_name+" EMA")
            plt.xlabel("Date")
            plt.ylabel("Price")
            plt.grid(b=True, which="both", axis="both")
            plt.plot(date_array, price_array, color="blue", label="price")
            plt.plot(date_array, exp50, color="black", label="50-day EMA")
            plt.plot(date_array, exp10, color="red", label="10-day EMA")
            #plt.axvline(x=date_array[crossover_idx_array[-1]], linestyle="--", color="black")

            """
            for crossover_idx in crossover_idx_array:
                plt.axvline(x=date_array[crossover_idx], color="green", linestyle="--")
            """
            plt.legend(loc="best")
            fig.autofmt_xdate()
            plt.show()
            
            fig, ax = plt.subplots()
            plt.title(company_name+" EMA difference")
            plt.grid(b=True, which="both", axis="both")
            plt.xlabel("Date")
            plt.ylabel("Price")
            plt.plot(date_array, diff_percentage_array)
            plt.axhline(y=2.5, color="black", linestyle="--")
            plt.axhline(y=-2.5,color="black", linestyle="--")
            fig.autofmt_xdate()
            plt.show()
            
        return_dict = {
                "ma_signal": ma_signal,
                "ma_crossover": ma_crossover,
                "ma_trend": ma_trend,
                "ma_seperation": ma_seperation
                }
        
        return return_dict

            
    def get_macd_signal(self, show_plot=0):
        date_array = self.date_array
        price_array = self.price_array
        ticker = self.ticker
        company_name = self.company_name
        ta_start_idx = self.ta_start_idx
        price_array_ta = self.price_array_ta
        
        #Get MACD and crossing points
        macd, macdsignal, macdhistory = ta.MACD(price_array_ta, fastperiod=12, slowperiod=26, signalperiod=9)
        macd, macdsignal, macdhistory = macd[ta_start_idx:], macdsignal[ta_start_idx:], macdhistory[ta_start_idx:]
        macd, macdsignal, macdhistory = macd.reset_index(drop=True), macdsignal.reset_index(drop=True), macdhistory.reset_index(drop=True)
        
        diff_array = macd-macdsignal
        idx = 0
        root_idx_array = []
        crossover_array = []
        last_crossover_array = []
        crossover_date_array = []
        
        for diff in diff_array:
            #print(diff)
            
            if idx > 0: 
                
                #Crossed above MACD
                if diff > 0 and diff_array[idx-1] < 0:
                    root_idx_array = np.append(root_idx_array, idx)
                    crossover_array = np.append(crossover_array, "bullish")
                    #print(date_array[int(idx)])
                    #print("bullish")
                #Crossed below MACD
                elif diff < 0  and diff_array[idx-1] > 0:
                    root_idx_array = np.append(root_idx_array, idx)
                    #print(date_array[int(idx)])
                    crossover_array = np.append(crossover_array, "bearish")
                    #print("bearish")
                
            idx+=1
        
        last_crossover = crossover_array[-1]
        
        key = int(root_idx_array[-1]+1)
        
        if key >= np.size(date_array):
            key = key -1 
        
        crossover_date = date_array[key]
        
        today_date = dt1.today()
        idx = 0
        while idx < 7:
            idx += 1
            test_date = today_date - dt2.timedelta(days = idx)
            test_date_calc = test_date.strftime("%Y-%m-%d")
            crossover_date_calc = crossover_date.strftime("%Y-%m-%d")
            #print(test_date_calc, crossover_date_calc)
            
            #If crossover in last 7 days
            if test_date_calc == crossover_date_calc:
                print("MACD crossover:", crossover_date)
            
        
            
        
        last_crossover_array = np.append(last_crossover_array, last_crossover)
        crossover_date_array = np.append(crossover_date_array, crossover_date)
        
        latest_diff = diff_array[np.size(diff)-1]
        latest_macd = macd[np.size(diff)-1]
        latest_diff_percentage = np.abs((latest_diff/latest_macd)*100)
        
        if show_plot == 1:
            fig, ax = plt.subplots()
            plt.title(company_name+" MACD")
            plt.grid(b=True, which="both", axis="both")
            plt.ylabel("price")
            plt.xlabel("date")
            plt.plot(date_array, macd, label=ticker+"MACD", color = 'red')
            plt.plot(date_array, macdsignal, label='Signal Line', color='black')
            """
            for root in root_idx_array:
                plt.axvline(x=date_array[int(root)], color="black", linestyle="--")
            """
            plt.legend(loc='upper left')
            fig.autofmt_xdate()
            plt.show()
        
        return_dict = {
                "macd": macd,
                "macdsignal": macdsignal,
                "macdhistory": macdhistory,
                "last_crossover": last_crossover,
                "crossover_date": crossover_date,
                "latest_diff_percentage": latest_diff_percentage
                }
        
        return return_dict
    
    
    def get_obv_signal(self, show_plot=0):
        date_array = self.date_array
        price_array = self.price_array
        volume_array = self.volume_array
        company_name = self.company_name
        
        
        obv_array = ta.OBV(price_array, volume_array)
        
        #Identify obv peaks
        idx = 0
        max_idx_array = []
        min_idx_array = []

        for obv in obv_array:
            if idx > 1:
                if (obv_array[idx-1] - obv_array[idx - 2]) > 0 and obv < obv_array[idx-1]:
                    max_idx_array = np.append(max_idx_array, idx)
                elif (obv_array[idx -1] - obv_array[idx - 2]) < 0 and obv > obv_array[idx-1]:
                    min_idx_array = np.append(min_idx_array, idx)
            
            idx +=1
        
        max_latest = max_idx_array[-1]
        min_latest = min_idx_array[-1]
        obv_min = obv_array[int(min_latest)-1]
        obv_max = obv_array[int(max_latest)-1]
        date_min = date_array[min_latest-1]
        date_max = date_array[max_latest-1]
        
        latest_obv = obv_array[np.size(obv_array)-1]
        obv_gradient = latest_obv - obv_array[np.size(obv_array)-2]
        
        if obv_gradient < 0:
            obv_gradient_type = "decreasing"
        elif obv_gradient > 0:
            obv_gradient_type = "increasing"
        elif obv_gradient == 0:
            obv_gradient_type = "flat"
        
        if latest_obv < obv_min:
            obv_type = "bearish"
            diff = obv_array - obv_min
            date_diff = (dt1.today() - date_min).days
            diff_latest = diff[np.size(diff)-1]
            diff_percentage = np.abs(diff_latest/latest_obv *100)
        elif latest_obv > obv_max:
            obv_type = "bullish"
            diff = obv_array - obv_max
            date_diff = (dt1.today() - date_max).days
            diff_latest = diff[np.size(diff)-1]
            diff_percentage = np.abs(diff_latest/latest_obv *100)
        else:
            diff = ""
            obv_type = "neutral"
            diff_percentage = ""
            date_diff = ""

        if show_plot == 1:
            fig, ax = plt.subplots()
            plt.title(company_name+" OBV")
            plt.grid(b=True, which="both", axis="both")
            plt.ylabel("volume")
            plt.xlabel("date")
            plt.plot(date_array, obv_array, label=self.ticker)
            #plt.axvline(date_min, linestyle="--", color="green")
            #plt.axvline(date_max, linestyle="--", color="red")
            plt.axhline(y=obv_min, linestyle="--", color="red")
            plt.axhline(y=obv_max, linestyle="--", color="green")
            fig.autofmt_xdate()
            plt.show()
        
        
        
        return_dict = {
                "obv_type": obv_type,
                "diff_percentage": diff_percentage,
                "obv_gradient_type": obv_gradient_type,
                "date_diff": date_diff
                }
        
        return return_dict
        
    def get_rsi_signal(self, show_plot=0):
        date_array = self.date_array
        price_array = self.price_array
        price_array_ta = self.price_array_ta
        ta_start_idx = self.ta_start_idx
        company_name = self.company_name
        
        rsi_data = ta.RSI(price_array_ta, timeperiod=14)
        rsi_data = rsi_data[ta_start_idx:]
        rsi_data = rsi_data.reset_index(drop=True)
        
        idx = 0
        overbought_crossover_array = []
        oversold_crossover_array = []
        rsi_data_array = []
        
        for rsi in rsi_data:
            if math.isnan(rsi):
                rsi = 0
            else:
                rsi = int(rsi)
            rsi_data_array = np.append(rsi_data_array, rsi)
        
        idx = 0
        
        #print(rsi_data_array[2])
    
        
        for rsi in rsi_data_array:
            if idx > 0:
                if rsi_data_array[idx] >= 70 and rsi_data_array[idx-1] < 70:
                    overbought_crossover_array = np.append(overbought_crossover_array, idx)
                elif rsi_data_array[idx] <= 30 and rsi_data_array[idx-1] > 30:
                    oversold_crossover_array = np.append(oversold_crossover_array, idx)
            idx+=1 
        
        latest_rsi = rsi_data[np.size(rsi_data)-1]
        rsi_gradient = latest_rsi - rsi_data[np.size(rsi_data)-2]
        
        if rsi_gradient < 0:
            rsi_gradient_type = "decreasing"
        elif rsi_gradient > 0:
            rsi_gradient_type = "increasing"
        elif rsi_gradient == 0:
            rsi_gradient_type = "flat"
        
        if latest_rsi > 70:
            rsi_signal = "overbought"
            rsi_crossover = date_array[int(overbought_crossover_array[-1])]
        elif latest_rsi < 30:
            rsi_signal = "oversold"
            rsi_crossover = date_array[int(oversold_crossover_array[-1])]
        else:
            rsi_signal = "neutral"
            rsi_crossover = ""
        
        if show_plot == 1:
            fig, ax = plt.subplots()
            plt.grid(b=True, which="both", axis="both")
            plt.title(company_name+" RSI")
            plt.plot(date_array, rsi_data, label='RSI')
            plt.fill_between(date_array, y1=30, y2=70, color = 'green', alpha='0.3')
            if rsi_signal != "neutral":
                plt.axvline(x=rsi_crossover, linestyle="--", color="red")
            plt.xlabel('Date')
            plt.ylabel('RSI')
            plt.ylim(0,100)
            fig.autofmt_xdate()
            plt.show()
            
        today_date = dt1.today()
        
        return_dict = {
                "rsi_data": rsi_data,
                "rsi_signal": rsi_signal,
                "rsi_value": latest_rsi,
                "rsi_crossover": rsi_crossover,
                "rsi_trend": rsi_gradient_type
                }
        
        return return_dict
    
    def get_bollinger_band_signal(self, show_plot=0):
        price_array = self.price_array
        date_array = self.date_array
        start_date = self.start_date
        end_date = self.end_date
        company_name = self.company_name
        ta_start_idx = self.ta_start_idx
        price_array_ta = self.price_array_ta
  
        #Get bands
        upper_band, middle_band, lower_band = ta.BBANDS(price_array_ta, timeperiod =20)
        upper_band, middle_band, lower_band = upper_band[ta_start_idx:], middle_band[ta_start_idx:], lower_band[ta_start_idx:]
        upper_band, middle_band, lower_band = upper_band.reset_index(drop=True), middle_band.reset_index(drop=True), lower_band.reset_index(drop=True)
        
        #Get latest price
        latest_price = price_array[np.size(price_array)-1]
        
        #Find most recent price gradient
        gradient = latest_price - price_array[np.size(price_array)-2]
        if gradient > 0:
            bb_trend = "increasing"
        elif gradient < 0:
            bb_trend = "decreasing"
        elif gradient == 0:
            bb_trend = "flat"
            
        #find bb crossovers and bb width
        idx = 0
        bb_upper_crossover_array = []
        bb_lower_crossover_array = []
        bb_width_array = []
        sma_20 = ta.SMA(price_array, timeperiod = 20)
        
        
        start_date_calc, end_date_calc = start_date, end_date
        
        if isinstance(start_date, str):
            start_date_calc = dt1.strptime(start_date, '%Y-%m-%d')
            
        if isinstance(end_date, str):
            end_date_calc = dt1.strptime(end_date, '%Y-%m-%d')   
            
        date_diff = end_date_calc - start_date_calc
        date_diff = date_diff.days
        
        if date_diff > 180: 
            bb_start_date = end_date_calc  - dt2.timedelta(days=180)
            #print("end", end_date, "start_bb", bb_start_date)
            #print("bb_start", bb_start_date, "start", start_date, "end_date", end_date)
        
            
            #print(date_array[1].year+"-"+date_array[1].month,date_array[1].day)
            idx = 0
            for date in date_array:
                idx += 1
                if date.year == bb_start_date.year:
                    if date.month == bb_start_date.month:
                        if date.day == bb_start_date.day:
                            start_bb_idx = idx
        else:
            start_bb_idx = 0
                            
                
        idx = 0
        
        #Find bb crossovers
        for price in price_array:
            #print(price)
            
            if idx > 0:
                #Price crossed above upper band
                if price > upper_band[idx] and price_array[idx-1] < upper_band[idx-1]:
                    bb_upper_crossover_array = np.append(bb_upper_crossover_array, idx)
                #Price crossed below lower band
                elif price < lower_band[idx] and price_array[idx-1] > lower_band[idx-1]:
                    bb_lower_crossover_array = np.append(bb_lower_crossover_array, idx)
                    
                bb_width = (upper_band[idx] - lower_band[idx])/sma_20[idx]
                bb_width_array = np.append(bb_width_array, bb_width)
            
            idx += 1
        
        #Find bb width
        idx = 0
        bb_width_sum = 0
        bb_width_clean = []
        
        for bb_width in bb_width_array:
            #print(bb_width)
            
            if math.isnan(bb_width):
                pass
            else:
                bb_width_sum += bb_width
                idx += 1
                bb_width_clean = np.append(bb_width_clean, bb_width)
            
        bb_width_min = bb_width_clean[np.argmin(bb_width_clean)]
        bb_width_average = bb_width_sum/idx
        bb_width = bb_width_array[-1]
            
        
        #Determine bb signal
        if latest_price > upper_band[np.size(upper_band)-1]:
            bb_signal = "bearish"
            bb_crossover = date_array[bb_upper_crossover_array[-1]]
        elif latest_price < lower_band[np.size(lower_band)-1]:
            bb_signal = "bullish"
            bb_crossover = date_array[bb_lower_crossover_array[-1]]
        else:
            bb_signal = "neutral"
            bb_crossover = ""

        
        #Show graph
        if show_plot == 1:
            fig, ax = plt.subplots()
            plt.title(company_name+" Bollinger Bands")
            plt.grid(b=True, which="both", axis="both")
            plt.xlabel("Date")
            plt.ylabel("Price")
            plt.plot(date_array, upper_band, color="orange")
            plt.plot(date_array, middle_band, color="darkorange")
            plt.plot(date_array, lower_band, color="orange")
            plt.plot(date_array, price_array, color="blue")
            if bb_signal != "neutral":
                plt.axvline(x=bb_crossover, color="red", linestyle="--")
            plt.fill_between(date_array, y1=lower_band, y2=upper_band, color = 'orange', alpha='0.3')
            fig.autofmt_xdate()
            plt.show()
            
        return_dict = {
                "bb_signal": bb_signal,
                "bb_crossover": bb_crossover,
                "bb_trend": bb_trend,
                "bb_width_min": bb_width_min,
                "bb_width_average": bb_width_average,
                "bb_width": bb_width
                }
        
        return return_dict
        
        
     
            
       
        