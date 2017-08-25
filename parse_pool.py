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
from stock_utils import pool_analysis 

#portfolios_finance = ['600030','600036','600109','601318','601328']
#portfolios_industry = ['600037','002223','601231','000050','002049','300077','600597','000049','000100','600690','002032','000651','600585']
#portfolios_military = ['600150','600118','000768']
#stock_pool = ['002007','002230','601238','600104','300077','002594','002405','300024','601633','002185','600584','601933','600887','600597','002462','002456','000100','300015','600016','600000','300059','600895']
stock_pool = ['002230','300024','601933','600887','600597','600016','600000','300059','600895','600030','002415']
#'000100'
#stock_pool_military = ['600862','600760','600677','600879','000768','600150','600685','600072','002190','600118']
stock_pool_military = ['600862','600879','000768','600150','002190','600118']
stock_pool_appliance= ['002032','600060','000651']
stock_pool_ee       = ['600703','002636','601231','600584','002185','600183','002049','300077','603986']
stock_pool_med      = ['300676','601607','000423','600056','002185','603168','002462','300015']
stock_pool_sw       = ['600756']
stock_pool_auto     = ['002594','600104','601633','601238','002405','600081','002232','002055','300270','601799','300304']
stock_pool_apple    = ['300115','002456','000050','000049','002635','000823','002241','300433']
stock_pool_ai = ['300496','300053','603019','603160']

parsed_list = []


if __name__=="__main__":
     now = datetime.datetime.now()
     path = now.strftime('%Y-%m-%d')+"-pool" 
     if(not os.path.exists(path)):
        os.mkdir(path)
     else:
        parsed_list = os.listdir(path)
#        print(parsed_list)

     basic_df = ts.get_stock_basics()
     print ("stock pool is under deep parsing     ------------------") 
     show = 1 

     if(len(sys.argv) > 1):
       if(sys.argv[1] == "ns"):
          show = 0 
#     for stock_code in stock_pool:
#        try:
#           stock_name = basic_df['name'][stock_code]
#           print (str(stock_code)+" in pool is under deep parsing" + str(stock_name)) 
#           deep_study(stock_code,str(stock_name),path)
#        except:
#           traceback.print_exc()
#           pass
     pool_analysis(stock_pool_ai,basic_df,path,parsed_list,"ai",show) 
     pool_analysis(stock_pool,basic_df,path,parsed_list,"sp",show) 
     pool_analysis(stock_pool_ee,basic_df,path,parsed_list,"ee",show) 
     pool_analysis(stock_pool_appliance,basic_df,path,parsed_list,"app",show) 
     pool_analysis(stock_pool_sw,basic_df,path,parsed_list,"sw",show) 
     pool_analysis(stock_pool_auto,basic_df,path,parsed_list,"auto",show) 
     pool_analysis(stock_pool_apple,basic_df,path,parsed_list,"apple",show) 
     pool_analysis(stock_pool_apple,basic_df,path,parsed_list,"med",show) 
     pool_analysis(stock_pool_military,basic_df,path,parsed_list,"mil",show) 
#     print ("solid indurstry stock is under deep parsing     ------------------") 
#     for stock_code in portfolios_industry:
#        try:
#           stock_name = basic_df['name'][stock_code]
#           print (str(stock_code)+" stock is under deep parsing" + str(stock_name)) 
#           deep_study(stock_code,str(stock_name))
#        except:
#           traceback.print_exc()
#           pass
#     print ("military related stock is under deep parsing     ------------------") 
#     for stock_code in portfolios_military:
#        try:
#           stock_name = basic_df['name'][stock_code]
#           print (str(stock_code)+" stock is under deep parsing" + str(stock_name)) 
#           deep_study(stock_code,str(stock_name))
#        except:
#           traceback.print_exc()
#           pass
#     startup_pool = []
#     sm_pool= []
#     a_enelist = []
#     a_wavelist = []
#     a_weektrend = []
#     a_concept_list = []
#     initial_pool() 
##     ene_select()
#     wave_select()
#     week_trend()

