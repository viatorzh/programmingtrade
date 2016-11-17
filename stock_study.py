#!/usr/bin/env python

# -----------------------------------------------------------------------
# Viator studio all rights precents
# 
#
# description: visualize the China stock market data and calculate the macd
#              and display it another view
# 1.01 add the time of trend wave and volumn check code
# -----------------------------------------------------------------------

# beili
# trending line
# relative strong with index
# fib
# ene/bolling line
# different timing frames
import datetime
import tushare as ts
import pandas as pd
import numpy as np
import talib as ta
import math
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator, MonthLocator, DayLocator
from matplotlib.finance import fetch_historical_yahoo, candlestick_ochl, candlestick2_ohlc, volume_overlay
from matplotlib import gridspec
from matplotlib.mlab import csv2rec
from matplotlib.dates import num2date, date2num, IndexDateFormatter
from matplotlib.ticker import  IndexLocator, FuncFormatter

class stock_study:
    def __init__(self,code,period):
        self.code = code
        self.period = period
        self.find_trend = False
# -------------------------------------------------------------
# initial the data frame and and if plot enable the plot will be intialled
# -------------------------------------------------------------
    def initial_df(self,plot,k_type):
        now = datetime.datetime.now()
        # now.strftime('%Y-%m-%d')
        delta = datetime.timedelta(days = self.period)
#        delta = datetime.timedelta(days = 60)
        ndays = now - delta
#       fuquan data        
        dff = ts.get_h_data(self.code,start=ndays.strftime('%Y-%m-%d'))
#        no fuquan data        
        #dff = ts.get_hist_data(self.code,start=ndays.strftime('%Y-%m-%d'),ktype=k_type)
        self.df = dff[::-1] 
        if plot != 0:
             ma5  = ta.MA(np.array(self.df['close']),5,matype=0)
             ma10 = ta.MA(np.array(self.df['close']),10,matype=0)
             ma20 = ta.MA(np.array(self.df['close']),20,matype=0)
             if ma5[-1] > ma20[-1]:
                     if self.df['close'][-1] > ma5[-1]:
                        print(" the stock "+str(self.code)+" is bull! ") ;
             if ma5[-1] < ma20[-1]:
                     if self.df['close'][-1] < ma5[-1]:
                        print(" the stock "+str(self.code)+" is bear! ") ;
             fig = plt.figure()
             fig.subplots_adjust(bottom=0.1)
             fig.subplots_adjust(hspace=0)
             gs = gridspec.GridSpec(2, 1, height_ratios=[4, 1])
             self.ax0 = plt.subplot(gs[0])
             self.ax1 = plt.subplot(gs[1], sharex=self.ax0)
             candles = candlestick2_ohlc(self.ax0,self.df['open'], self.df['high'], self.df['low'], self.df['close'], width=1, colorup='r', colordown='g') ;
             self.ax0.plot(ma5, color = 'black',lw=2,)
             self.ax0.plot(ma20, color = 'yellow',lw=2)
             self.ax0.plot(ma10, color = 'green',lw=2)



    def initial_extream_point(self,plot):
#         print(self.df['close'].count()) ;
         if self.df['close'].count() < 40:
            return False
         maxidx = self.df['close'][30:].idxmax(axis=1)
         minidx = self.df['close'][30:].idxmin(axis=1)
         #now = datetime.datetime.now()
         # now.strftime('%Y-%m-%d')
         #detla = datetime.timedelta(days = 120)
         #ndays = now - delta
         #dff = ts.get_hist_data(self.code,start=ndays.strftime('%Y-%m-%d'),ktype=k_type)
         #dff = dff[::-1] 
         price_diff = self.df['close'][maxidx] - self.df['close'][minidx] 
         maxcnt = self.df['close'][:maxidx].count() 
         mincnt = self.df['close'][:minidx].count() 
	 # if it is up
         if maxidx > minidx :
            minidx2 = self.df['close'][maxidx:].idxmin(axis=1) ;
            maxidx2 = self.df['close'][:minidx].idxmax(axis=1) ;
            idx_diff = maxcnt - mincnt + 1 
            if price_diff > self.df['close'][-1] * 0.1:
                second_max_idx = minidx 
                second_min_idx = maxidx
               #for idx in range(minidx:maxidx):
	       # here i want to find the sub wave between the main wave which i can draw the trend line
                for idx in self.df.index[mincnt:maxcnt]:
                       if self.df['close'][idx] - self.df['close'][minidx] > price_diff * 0.2 :
                               second_max_idx = idx 
                       if self.df['close'][second_max_idx] - self.df['close'][idx] > price_diff * 0.2 :
                               second_min_idx = idx 
                       if second_min_idx != maxidx:
                               if self.df['close'][idx] > self.df['close'][second_max_idx]:
                                       maxidx2 = second_max_idx
                                       minidx2 = second_min_idx
                                       self.find_trend = True
                                       break
         # if down
         else:
            idx_diff = mincnt - maxcnt + 1 
            maxidx2 = self.df['close'][minidx:].idxmax(axis=1) ;
            minidx2 = self.df['close'][:maxidx].idxmin(axis=1) ;
            if price_diff > self.df['close'][-1] * 0.1:
                second_max_idx = minidx 
                second_min_idx = maxidx
	       #for idx in range(maxidx:minidx):
                for idx in self.df.index[maxcnt:mincnt]:
                       if self.df['close'][idx] - self.df['close'][second_min_idx] > price_diff * 0.2 :
                               second_max_idx = idx 
                       if self.df['close'][maxidx] - self.df['close'][idx] > price_diff * 0.2 :
                               second_min_idx = idx 
                       if second_max_idx != minidx:
                               if self.df['close'][idx] < self.df['close'][second_min_idx]:
                                       maxidx2 = second_max_idx
                                       minidx2 = second_min_idx
                                       self.find_trend = True
                                       break
         if plot != 0:
              self.ax0.plot([self.df['close'][:minidx].count(),self.df['close'].count()],[self.df['close'][maxidx]-price_diff*0.618,self.df['close'][maxidx]-price_diff*0.618],'b--') ;
              self.ax0.plot([self.df['close'][:minidx].count(),self.df['close'].count()],[self.df['close'][maxidx]-price_diff*0.382,self.df['close'][maxidx]-price_diff*0.382],'b--') ;
         
         self.maxidx = maxidx 
         self.minidx = minidx 
         self.maxidx2 = maxidx2 
         self.minidx2 = minidx2
         if idx_diff > int(self.df['close'].count() * 0.3):
           return True
         else:
           return False

    

    def plot_trend(self):
#        if self.find_trend:
        self.ax0.plot([self.df['close'][:self.maxidx].count(),self.df['close'][:self.maxidx2].count()],[self.df['close'][self.maxidx],self.df['close'][self.maxidx2]],'--')
        self.ax0.plot([self.df['close'][:self.minidx].count(),self.df['close'][:self.minidx2].count()],[self.df['close'][self.minidx],self.df['close'][self.minidx2]],'--') 
        self.ax0.plot([self.df['close'][:self.minidx].count(),self.df['close'][:self.maxidx].count()],[self.df['close'][self.minidx],self.df['close'][self.maxidx]],'r-') 

    def macd_analysis(self,plot):
        macd,macdsignal,macdhist = ta.MACD(np.array(self.df['close']), fastperiod = 12,slowperiod = 26 , signalperiod = 9)
        macd[0:33] = np.zeros(33)
        macdsignal[0:33] = np.zeros(33)
        macdhist[0:33] = np.zeros(33)
        if plot != 0:
            self.ax1.plot(macd,color='blue',lw=2) ;
            self.ax1.plot(macdsignal,color='red',lw=2) ;
            self.ax1.plot(macdhist) # ,color='black',lw=3) ;
#        self.ax1.hist(macdhist) # ,color='black',lw=3) ;
        if self.find_trend:
            maxidx_cnt  = self.df['close'][:self.maxidx].count() 
            maxidx2_cnt = self.df['close'][:self.maxidx2].count() 
            minidx_cnt  = self.df['close'][:self.minidx].count() 
            minidx2_cnt = self.df['close'][:self.minidx2].count() 
#            print("maxidx is "+str(maxidx_cnt)+" macdhist is "+str(macdhist[maxidx_cnt]))
#            print("maxidx2 is "+str(maxidx2_cnt)+" macdhist 2 is "+str(macdhist[maxidx2_cnt]))
            if self.maxidx > self.minidx:
                 if macdhist[maxidx_cnt] < macdhist[maxidx2_cnt]:
                     print (str(self.code)+" macd top beili")
                 if self.df['volume'][self.maxidx] < self.df['volume'][self.maxidx2]:
                     print (str(self.code)+" macd top volume beili")
                 return False
            else:
                 if macdhist[minidx_cnt] > macdhist[minidx2_cnt]:
                     print (str(self.code)+" macd bottom beili")
                     return True
                 if self.df['volume'][self.minidx] < self.df['volume'][self.minidx2]:
                     print (str(self.code)+"macd bottom volume beili")
                 return False

    def show_plt(self):
        plt.title(str(self.code)+ " analysis")
        plt.show()


    def check_vol(self):
        N = 20
        volma = ta.MA(np.array(self.df['volume']),N,matype=0)
        threshold = volma[-1] * 1.5 
        if self.df['volume'].count() < 5:
           return False
        if self.df['volume'][-1] > threshold:
           return True
        if self.df['volume'][-2] > threshold:
           return True
        if self.df['volume'][-3] > threshold:
           return True
        return False

    def check_ene(self):
        M1 = 9
        N = 11
        M2 = 10
        ma = ta.MA(np.array(self.df['close']),N,matype=0) 
        ENEbotline = (1-M2/100) * ma 
#        ENEtopline = (1+M1/100) * ma 
        if self.df['low'].count() < 3:
           return False 
#        self.ax0.plot(ENEbotline, color = 'pink',lw=2)
#        self.ax0.plot(ENEtopline, color = 'pink',lw=2)
        if self.df['low'][-1] < ENEbotline[-1]:
      	    print("check ENE find ene low break for "+str(self.code)) 
#      	    print("buy!!!") 
      	    return True
        elif self.df['low'][-2] < ENEbotline[-2]:
      	    print("check ENE find ene low break for "+str(self.code)) 
#      	    print("buy!!!") 
      	    return True
        elif self.df['low'][-3] < ENEbotline[-3]:
      	    print("check ENE find ene low break for "+str(self.code)) 
#      	    print("buy!!!") 
      	    return True
#        elif self.df['high'][-1] > ENEtopline[-1]:
#      	    print("check ENE find ene top break for "+str(self.code)) 
##     	    print("sell !!!") 
#      	    return False
        else:
      	    return False
