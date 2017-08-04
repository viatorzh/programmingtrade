#!/usr/bin/env python
# coding=gbk

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
import traceback
from stock_study import stock_study


if __name__=="__main__":
      a_enelist = []
      a_wavelist = []
      a_enestrlist = []
      a_wavestrlist = []
      for line in open("blue_pool.csv"):
           code, name, industry, pe,outstanding,price= line.split(",")
#           print(str(code)+","+str(name)+","+str(industry)+","+str(pe)+","+str(outstanding)+","+str(price))
#           print(str(code)+","+str(name)+","+str(industry)+","+str(pe)+","+str(outstanding)+","+str(price))
           try:
               s = stock_study(code,20)
               s.initial_df(0,"D")
               print (str(code)+" stock is under parsing") 
               if(s.check_ene()):
                   print("the stock " + str(code) +" ene is break, maybe we could do some investigate about it") 
                   a_enelist.append(code)
                   a_enestrlist.append(line)
               s = stock_study(code,100)
               s.initial_df(0,"D")
               if(s.initial_extream_point(0) and s.macd_analysis(0) and s.check_vol()):
                   print("the stock " + str(code) +" wave matches model and volume abnormal maybe we could do some investigate about it") 
                   a_wavelist.append(code)
               else:
                   if(s.find_trend):
                      a_wavelist.append(code)
                      a_wavestrlist.append(line)
           except:
               traceback.print_exc()
               pass
           
      print("ene break list is:") 
      print(a_enelist) 
      for line in a_enestrlist:
          print(line) 
          code, name, industry, pe,outstanding,price= line.split(",")
      print("wave resistance list is:") 
      print(a_wavelist) 
      print(a_wavestrlist) 
      for line in a_wavestrlist:
          print(line) 
