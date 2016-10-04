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


import sys
import datetime
import time
import talib as ta
import tushare as ts
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator, MonthLocator, DayLocator
from matplotlib.finance import fetch_historical_yahoo, candlestick_ochl, candlestick2_ohlc, volume_overlay
from matplotlib import gridspec
from matplotlib.mlab import csv2rec
from matplotlib.dates import num2date, date2num, IndexDateFormatter
from matplotlib.ticker import  IndexLocator, FuncFormatter

from dateutil.parser import parse
from operator import itemgetter

#if __name__=="__main__":

def test_tsta():
  df = ts.get_h_data('600895',start='2016-03-04',end='2016-09-01') 
  #df = ts.get_hist_data('600895',start='2016-03-04',end='2016-09-01') 
  macd,macdsignal,macdhist = ta.MACD(np.array(df['close']), fastperiod = 12,slowperiod = 26 , signalperiod = 9)
  
  fig = plt.figure()
  fig.subplots_adjust(bottom=0.1)
  fig.subplots_adjust(hspace=0)
  
  gs = gridspec.GridSpec(2, 1, height_ratios=[4, 1])
  
  ax0 = plt.subplot(gs[0])
  
  candles = candlestick2_ohlc(ax0,np.array(df['open']), df['high'], df['low'], df['close'], width=1, colorup='r', colordown='g') ;
  
  M1 = 9
  N = 11
  M2 = 10
  ma = ta.MA(np.array(df['close']),N,matype=0) 
  ENEtopline = (1+M1/100) * ma ;
  ENEbotline = (1-M2/100) * ma ;
  ENEline = (ENEtopline + ENEbotline) /2 ;
  # ax0.plot(ENEtopline, color = 'black',lw=2,lable='ENE top')
  # ax0.plot(ENEbotline , color = 'black',lw=2,lable='ENE bottom')
  # ax0.plot(ENEline, color = 'yellow',lw=2,lable='ENE line')
  ax0.plot(ENEtopline, color = 'black',lw=2,)
  ax0.plot(ENEbotline , color = 'black',lw=2)
  ax0.plot(ENEline, color = 'yellow',lw=2)
  
  
  ax0.legend(loc='best', shadow=True, fancybox=True)
  ax0.set_ylabel('Price($)', fontsize=16)
  #ax0.set_title(ticker, fontsize=24, fontweight='bold')
  ax0.grid(True)
  
  ax1 = plt.subplot(gs[1], sharex=ax0)
  #ax1.plot(df['date'],macd,color=black,lw=2)
  #ax1.plot(df['date'],macdsignal,color=blue,lw=1)
  #vc = volume_overlay(ax1, df['open'],df['close'],df['volume'],colorup='r',width=1) ;
  ax1.plot(range(len(df.index)),macd,color='blue',lw=2) ;
  
  ax1.set_ylabel('MACD', fontsize=16)
  ax1.grid(True)
  plt.setp(ax0.get_xticklabels(), visible=False)
  
  plt.show()
  
  df_basic = ts.get_stock_basics()
  df_basic['totals']['600895']
  df_basic['pe']['600895']


# first use ene / pe /totals and industry to filter stock 

def stock_tech_analysis(code):
  print("stock techinical analysis start to parse the stock "+str(code))
  dff = ts.get_h_data(code,start='2016-07-04')
  df = dff[::-1]
  df
  macd,macdsignal,macdhist = ta.MACD(np.array(df['close']), fastperiod = 12,slowperiod = 26 , signalperiod = 9)
  ma5 = ta.MA(np.array(df['close']),5,matype=0)
  ma10 = ta.MA(np.array(df['close']),10,matype=0)
  ma20 = ta.MA(np.array(df['close']),20,matype=0)
#  ma20 = ta.MA(np.array(df['close'],20,mtype=0)
  print("the close[-1] is " + str(df['close'][-1]) + " and the ma5[-1] is " + str(ma5[-1]) + "and the ma20[-1] is " + str(ma20[-1])) ;
  if ma5[-1] > ma20[-1]:
	  if df['close'][-1] > ma5[-1]:
             print(" the stock "+str(code)+" is bull! ") ;
  if ma5[-1] < ma20[-1]:
	  if df['close'][-1] < ma5[-1]:
             print(" the stock "+str(code)+" is bear! ") ;
  fig = plt.figure()
  fig.subplots_adjust(bottom=0.1)
  fig.subplots_adjust(hspace=0)
  gs = gridspec.GridSpec(2, 1, height_ratios=[4, 1])
  ax0 = plt.subplot(gs[0])
  candles = candlestick2_ohlc(ax0,np.array(df['open']), df['high'], df['low'], df['close'], width=1, colorup='r', colordown='g') ;
  ax0.plot(ma5, color = 'black',lw=2,)
  ax0.plot(ma20, color = 'yellow',lw=2)
  ax0.plot(ma10, color = 'green',lw=2)
  # trying to plot the trending line of the stock
  maxidx = df['close'].idxmax(axis=1) ;
  minidx = df['close'].idxmin(axis=1) ;
#  dmax = time.strptime(maxidx,"%Y-%m-%d") ;
#  dmin = time.strptime(minidx,"%Y-%m-%d") ;
  if maxidx > minidx :
     maxidx2 = df['close'][:minidx].idxmax(axis=1) ;
     minidx2 = df['close'][maxidx:].idxmin(axis=1) ;
  else:
     maxidx2 = df['close'][minidx:].idxmax(axis=1) ;
     minidx2 = df['close'][:maxidx].idxmin(axis=1) ;
  ax0.plot([df['close'][:maxidx].count(),df['close'][:maxidx2].count()],[df['close'][maxidx],df['close'][maxidx2]]) ;
  ax0.plot([df['close'][:minidx].count(),df['close'][:minidx2].count()],[df['close'][minidx],df['close'][minidx2]]) ;
#  ax0.plot(minidx,df['close'][minidx],minidx2,df['close'][minidx2]) ;
  plt.show()

def index_tech_analysis(code):
  print("stock techinical analysis start to parse the stock "+str(code))
  dff = ts.get_hist_data(code,start='2016-06-04')
  df = dff[::-1]
  df
  macd,macdsignal,macdhist = ta.MACD(np.array(df['close']), fastperiod = 12,slowperiod = 26 , signalperiod = 9)
  ma5 = ta.MA(np.array(df['close']),5,matype=0)
  ma10 = ta.MA(np.array(df['close']),10,matype=0)
  ma20 = ta.MA(np.array(df['close']),20,matype=0)
#  ma20 = ta.MA(np.array(df['close'],20,mtype=0)
  print("the close[-1] is " + str(df['close'][-1]) + " and the ma5[-1] is " + str(ma5[-1]) + "and the ma20[-1] is " + str(ma20[-1])) ;
  if ma5[-1] > ma20[-1]:
      if df['close'][-1] > ma5[-1]:
         print(" the index "+str(code)+" is bull! ") 
      else:
         print(" the index "+str(code)+" is not bull! ") 
  else:# ma5[-1] < ma20[-1]:
      if df['close'][-1] < ma5[-1]:
         print(" the index "+str(code)+" is bear! ") 
      else:
         print(" the index "+str(code)+" is not bear! ") 
  fig = plt.figure()
  fig.subplots_adjust(bottom=0.1)
  fig.subplots_adjust(hspace=0)
  gs = gridspec.GridSpec(2, 1, height_ratios=[4, 1])
  ax0 = plt.subplot(gs[0])
  candles = candlestick2_ohlc(ax0,np.array(df['open']), df['high'], df['low'], df['close'], width=1, colorup='r', colordown='g') ;
  ax0.plot(ma5, color = 'black',lw=2,)
  ax0.plot(ma20, color = 'yellow',lw=2)
  ax0.plot(ma10, color = 'green',lw=2)
  maxidx = df['close'].idxmax(axis=1) ;
  minidx = df['close'].idxmin(axis=1) ;
#  dmax = time.strptime(maxidx,"%Y-%m-%d") ;
#  dmin = time.strptime(minidx,"%Y-%m-%d") ;
  if maxidx > minidx :
     maxidx2 = df['close'][:minidx].idxmax(axis=1) ;
     minidx2 = df['close'][maxidx:].idxmin(axis=1) ;
  else:
     maxidx2 = df['close'][minidx:].idxmax(axis=1) ;
     minidx2 = df['close'][:maxidx].idxmin(axis=1) ;
  ax0.plot([df['close'][:maxidx].count(),df['close'][:maxidx2].count()],[df['close'][maxidx],df['close'][maxidx2]]) ;
  ax0.plot([df['close'][:minidx].count(),df['close'][:minidx2].count()],[df['close'][minidx],df['close'][minidx2]]) ;
  plt.show()
index_tech_analysis('sh') 

portfolios = ['600895','002405']
for stock_code in portfolios:
  stock_tech_analysis(stock_code)
 
df = ts.get_index()
