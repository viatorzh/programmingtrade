#!/usr/bin/env python

# -----------------------------------------------------------------------
# Viator studio all rights precents
# 
#
# description: visualize the China stock market data and calculate the macd
#              and display it another view
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
    def __init__(self,code):
        self.code = code
        self.period = 100

    def initial_df(self,plot,k_type):
        now = datetime.datetime.now()
        # now.strftime('%Y-%m-%d')
        delta = datetime.timedelta(days = self.period)
#        delta = datetime.timedelta(days = 60)
        ndays = now - delta
        dff = ts.get_hist_data(self.code,start=ndays.strftime('%Y-%m-%d'),ktype=k_type)
        self.df = dff[::-1] 
        ma5  = ta.MA(np.array(self.df['close']),5,matype=0)
        ma10 = ta.MA(np.array(self.df['close']),10,matype=0)
        ma20 = ta.MA(np.array(self.df['close']),20,matype=0)
        if ma5[-1] > ma20[-1]:
                if self.df['close'][-1] > ma5[-1]:
                   print(" the stock "+str(self.code)+" is bull! ") ;
        if ma5[-1] < ma20[-1]:
                if self.df['close'][-1] < ma5[-1]:
                   print(" the stock "+str(self.code)+" is bear! ") ;
        if plot != 0:
             fig = plt.figure()
             fig.subplots_adjust(bottom=0.1)
             fig.subplots_adjust(hspace=0)
             gs = gridspec.GridSpec(2, 1, height_ratios=[4, 1])
             self.ax0 = plt.subplot(gs[0])
             candles = candlestick2_ohlc(self.ax0,self.df['open'], self.df['high'], self.df['low'], self.df['close'], width=1, colorup='r', colordown='g') ;
             self.ax0.plot(ma5, color = 'black',lw=2,)
             self.ax0.plot(ma20, color = 'yellow',lw=2)
             self.ax0.plot(ma10, color = 'green',lw=2)



    def initial_extream_point(self,plot):
         maxidx = self.df['close'].idxmax(axis=1)
         minidx = self.df['close'].idxmin(axis=1)
         #now = datetime.datetime.now()
         # now.strftime('%Y-%m-%d')
         #detla = datetime.timedelta(days = 120)
         #ndays = now - delta
         #dff = ts.get_hist_data(self.code,start=ndays.strftime('%Y-%m-%d'),ktype=k_type)
         #dff = dff[::-1] 
         price_diff = self.df['close'][maxidx] - self.df['close'][minidx] 
	 
         if maxidx > minidx :
            minidx2 = self.df['close'][maxidx:].idxmin(axis=1) ;
            maxidx2 = self.df['close'][:minidx].idxmax(axis=1) ;
            if price_diff > self.df['close'][-1] * 0.1:
                second_max_idx = minidx 
                second_min_idx = maxidx
               #for idx in range(minidx:maxidx):
                for idx in self.df.index[self.df['close'][:minidx].count():self.df['close'][:maxidx].count()]:
                       if self.df['close'][idx] - self.df['close'][minidx] > price_diff * 0.2 :
                               second_max_idx = idx 
                       if self.df['close'][second_max_idx] - self.df['close'][idx] > price_diff * 0.2 :
                               second_min_idx = idx 
                       if second_min_idx != maxidx:
                               if self.df['close'][idx] > self.df['close'][second_max_idx]:
                                       maxidx2 = second_max_idx
                                       minidx2 = second_min_idx
                                       break
         else:
            maxidx2 = self.df['close'][minidx:].idxmax(axis=1) ;
            minidx2 = self.df['close'][:maxidx].idxmin(axis=1) ;
            if price_diff > self.df['close'][-1] * 0.1:
                second_max_idx = minidx 
                second_min_idx = maxidx
	       #for idx in range(maxidx:minidx):
                for idx in self.df.index[self.df['close'][:maxidx].count():self.df['close'][:minidx].count()]:
                       if self.df['close'][idx] - self.df['close'][second_min_idx] > price_diff * 0.2 :
                               second_max_idx = idx 
                       if self.df['close'][maxidx] - self.df['close'][idx] > price_diff * 0.2 :
                               second_min_idx = idx 
                       if second_max_idx != minidx:
                               if self.df['close'][idx] < self.df['close'][second_min_idx]:
                                       maxidx2 = second_max_idx
                                       minidx2 = second_min_idx
                                       break
         if plot != 0:
              self.ax0.plot([self.df['close'][:minidx].count(),self.df['close'].count()],[self.df['close'][maxidx]-price_diff*0.618,self.df['close'][maxidx]-price_diff*0.618],'b--') ;
              self.ax0.plot([self.df['close'][:minidx].count(),self.df['close'].count()],[self.df['close'][maxidx]-price_diff*0.382,self.df['close'][maxidx]-price_diff*0.382],'b--') ;
         
         self.maxidx = maxidx 
         self.minidx = minidx 
         self.maxidx2 = maxidx2 
         self.minidx2 = minidx2
    

    def plot_trend(self):
        self.ax0.plot([self.df['close'][:self.maxidx].count(),self.df['close'][:self.maxidx2].count()],[self.df['close'][self.maxidx],self.df['close'][self.maxidx2]],'--')
        self.ax0.plot([self.df['close'][:self.minidx].count(),self.df['close'][:self.minidx2].count()],[self.df['close'][self.minidx],self.df['close'][self.minidx2]],'--') 
        self.ax0.plot([self.df['close'][:self.minidx].count(),self.df['close'][:self.maxidx].count()],[self.df['close'][self.minidx],self.df['close'][self.maxidx]],'r-') 


    def show_plt(self):
        plt.show()

    def check_ene(self):
        M1 = 9
        N = 11
        M2 = 10
        ma = ta.MA(self.df['close'],N,matype=0) 
        ENEbotline = (1-M2/100) * ma 
        if self.df['low'][-1] < ENEbotline[-1]:
      	  #  print("check ENE find ene low break for "+str(code)) 
      	    return True
        else:
      	    return False
