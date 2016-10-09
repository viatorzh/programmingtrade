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
from stock_study import stock_study

#if __name__=="__main__":

# index_tech_analysis('sh','D') 
# index_tech_analysis('sh','W') 
# index_tech_analysis('sz','D') 

#now = datetime.datetime.now()
# now.strftime('%Y-%m-%d')
#delta = datetime.timedelta(days = 60)
#ndays = now - delta

portfolios = ['600895','002405']
for stock_code in portfolios:
   s = stock_study(stock_code)
   s.initial_df(1,"D")
   s.initial_extream_point(1)
   s.plot_trend()
   print("max 1 is "+str(s.maxidx)+" max2 is "+str(s.maxidx2))
   print("min 1 is "+str(s.minidx)+" min2 is "+str(s.minidx2))
   s.show_plt()

# for code in stock_basics.index:
# 	if check_ene(code):
# 		if stock_basics['pe'][code] < 50:
# 			if stock_basics['pe'][code] != 0:
#               			print (str(code)+" stock pe is low") 
# 		if stock_basics['outstanding'][code] < 20000:
# 			print (str(code)+" stock fluent totals is not big") ;
# 
