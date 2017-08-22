#!/usr/bin/env python
# coding=gbk

# -----------------------------------------------------------------------
# Viator studio all rights precents
# 
#
# description: visualize the China stock market data and calculate the macd
#              and display it another view
# 1.01 add the time of trend wave and volumn check code
# 1.02 add the time of trend wave and volumn check code
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
from stock_study import stock_study



def realtime_study(code,stock_name,path,save=1):
     if(str(code) == 'sh'):
       s = stock_study(code,200)
     else:
       s = stock_study(code,130)
     s.initial_df(1,"60",path) 
     print (str(code)+" stock is under wave analysis for 60min k line") 
     if s.initial_extream_point(1): 
       print (str(code)+" trend existed") 
     if s.find_trend: 
       print (str(code)+" trend found sub wave") 
     s.plot_trend() 
     print (str(code)+" stock is under macd analysis") 
     s.check_ene()
     s.macd_analysis(1)
     print (str(code)+" stock is plotting itself") 
     if(save == 1):
       s.save_plt(stock_name+"_1h",basic_df)
     s.show_plt(stock_name+"_1h",basic_df)

def deep_study(code,stock_name,path,save=1):
     if(str(code) == 'sh'):
       s = stock_study(code,200)
     else:
       s = stock_study(code,130)
     s.initial_df(1,"D",path) 
     print (str(code)+" stock is under wave analysis") 
     if s.initial_extream_point(1): 
       print (str(code)+" trend existed") 
     if s.find_trend: 
       print (str(code)+" trend found sub wave") 
     s.plot_trend() 
     print (str(code)+" stock is under macd analysis") 
     s.check_ene()
     s.macd_analysis(1)
     print (str(code)+" stock is plotting itself") 
     if(save == 1):
       s.save_plt(stock_name,basic_df)
     s.show_plt(stock_name,basic_df)


portfolios_monitor = ['600895','002405','002594','300024','002230'      ,'601633',       '002185', '002456','300115','600016','600000','300059','600584']
portfolios_monitor = ['sh','600895','002405','002594','300024','002230'      ,'601633',       '002185', '002456','300115','600016','600000','300059','600584']
portfolios_monitor = ['sh','600895','002405','002456','300024','002230'      ,'601633',       '002185', '002594','300115','600016','600000','300059','600584']
portfolios_monitor = ['600895','002405','002456','600000','300024','002230'      ,'601633',       '002185', '002594','300115','600016','300059','600584']
#portfolios_monitor = ['600584','601633','002636','002594','300059','600895']
portfolios_monitor = ['600000','002185','002594','601633']

#portfolios_finance = ['600030','600036','600109','601318','601328']
#portfolios_industry = ['600037','002223','601231','000050','002049','300077','600597','000049','000100','600690','002032','000651','600585']
portfolios_military = ['600150','600118','000768']

stock_pool = ['002007','002230','601238','600104','300077','002594','002405','300024','601633','002185','600584','601933','600887','600597','002462','002456','000100','300015','600016','600000','300059','600895']
stock_pool = ['002007','002230','601238','600104','300077','002594','002405','300024','601633','002185','600584','601933','600887','600597','002462','002456','300015','600016','600000','300059','600895','000100']

if __name__=="__main__":
     now = datetime.datetime.now()
     path = now.strftime('%Y-%m-%d') 
     if(not os.path.exists(path)):
        os.mkdir(path)
     basic_df = ts.get_stock_basics()
     deep_study('sh','上证综指',path)
     deep_study('sz','深证成指',path)
     deep_study('zxb','中小板',path)
     deep_study('cyb','创业板',path)
#     f.open("portfolios_analysis.csv",'w')
     print ("classic stock is under deep parsing     ------------------") 
     for stock_code in portfolios_monitor:
        try:
           stock_name = basic_df['name'][stock_code]
           print (str(stock_code)+" stock is under deep parsing" + str(stock_name)) 
           deep_study(stock_code,str(stock_name),path)
           realtime_study(stock_code,str(stock_name),path)
        except:
           traceback.print_exc()
           pass
