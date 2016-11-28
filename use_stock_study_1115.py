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
portfolios = ['600895','002405','000596']
for stock_code in portfolios:
   s = stock_study(stock_code,100)
   s.initial_df(1,"D")
   s.initial_extream_point(1)
   s.plot_trend()
   s.macd_analysis(1)
   s.check_ene()
#   print("max 1 is "+str(s.maxidx)+" max2 is "+str(s.maxidx2))
#   print("min 1 is "+str(s.minidx)+" min2 is "+str(s.minidx2))
   s.show_plt()
stock_basics = ts.get_stock_basics() 

# ---------------------------------------------------------
# parse the our stocks
# -------------------------------------
portfolios_monitor = ['600895','002405','002594','300024','002230'      ,'601633',       '002185', '002456','300115','600016','600000','300059','600584']

for stock_code in portfolios_monitor:
     s = stock_study(stock_code,60)
     s.initial_df(0,"D")
     if(s.initial_extream_point(0)):
         s.initial_df(1,"D") 
         s.initial_extream_point(1) 
         s.macd_analysis(1)
         s.show_plt()
#     s.macd_analysis()
     if(s.check_ene()):
          print("the stock " + str(stock_code) +" ene is break, maybe we could do some investigate about it") 
     if(s.check_vol()):
          print("the stock " + str(stock_code) +" volume break maybe we could do some investigate about it") 
	# ene and macd beili
	# fib
# for code in stock_basics.index:
# 	if check_ene(code):
# 		if stock_basics['pe'][code] < 50:
# 			if stock_basics['pe'][code] != 0:
#               			print (str(code)+" stock pe is low") 
# 		if stock_basics['outstanding'][code] < 20000:
# 			print (str(code)+" stock fluent totals is not big") ;
# 
# -----------------------------------------------------------------
#  trend and macd beili filter
# -----------------------------------------------------------------
a_macdtrendlist = []
for code in stock_basics.index:
        print (str(code)+" stock is under parsing") 
        s = stock_study(code,100)
        s.initial_df(0,"D")
        if(s.initial_extream_point(0)):
           if(s.macd_analysis(0)):
               a_enelist.append(code)
               if stock_basics['pe'][code] < 50:
                   if stock_basics['pe'][code] != 0:
                       print (str(code)+" stock pe is low") 
                   if stock_basics['outstanding'][code] < 20000:
                       print (str(code)+" stock fluent totals is not big") ;
print(a_macdtrendlist) 


# -----------------------------------------------------------------
#  ene filter
# -----------------------------------------------------------------
a_enelist = []
for code in stock_basics.index:
        s = stock_study(code,20)
        s.initial_df(0,"D")
        print (str(code)+" stock is under parsing") 
        if(s.check_ene()):
            print("the stock " + str(code) +" ene is break, maybe we could do some investigate about it") 
            a_enelist.append(code)
            if stock_basics['pe'][code] < 50:
                if stock_basics['pe'][code] != 0:
                    print (str(code)+" stock pe is low") 
                if stock_basics['outstanding'][code] < 20000:
                    print (str(code)+" stock fluent totals is not big") ;

print(a_enelist) 
