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
import os
import tushare as ts
import pandas as pd
import numpy as np
import talib as ta
import traceback
import sys
from stock_study import stock_study
from stock_utils import deep_study 

if __name__=="__main__":
     now = datetime.datetime.now()
     path = now.strftime('%Y-%m-%d')+"-pool" 
     if(not os.path.exists(path)):
        os.mkdir(path)
     basic_df = ts.get_stock_basics()
     print ("stock pool is under deep parsing     ------------------") 
     show = 1 
     if(len(sys.argv) > 1):
        stock_code = sys.argv[1]
        try:
           stock_name = basic_df['name'][stock_code]
           print (str(stock_code)+" in pool is under deep parsing" + str(stock_name)) 
           deep_study(stock_code,str(stock_name),basic_df,path,"",1,1)
        except:
           traceback.print_exc()
           pass
