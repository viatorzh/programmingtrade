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
import matplotlib.pyplot as plt



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
     if s.check_kpattern_neg() == -1:
        print (" !!!!!!!!!!!!!!!!!  the stock "+str(code) + " K is getting worse, please consider short the position !!!!!!") ;
     print (str(code)+" stock is plotting itself") 
     if(save == 1):
       s.save_plt(stock_name+"_1h",basic_df)
#     s.show_plt(stock_name+"_1h",basic_df)

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
     if(s.check_kpattern == -1):
        print ("!!!!!!!!!!!!!!!!"+str(code)+" stock k reversed should be cleared!!!!!!!!!!!!!!!!!!!!!!!") 
     print (str(code)+" stock is plotting itself") 
     if(save == 1):
       s.save_plt(stock_name,basic_df)
#     s.show_plt(stock_name,basic_df)
     return s.df['close'][-1] 


portfolios_monitor = ['600895','002405','002594','300024','002230'      ,'601633',       '002185', '002456','300115','600016','600000','300059','600584']
portfolios_monitor = ['sh','600895','002405','002594','300024','002230'      ,'601633',       '002185', '002456','300115','600016','600000','300059','600584']
portfolios_monitor = ['sh','600895','002405','002456','300024','002230'      ,'601633',       '002185', '002594','300115','600016','600000','300059','600584']
portfolios_monitor = ['600895','002405','002456','600000','300024','002230'      ,'601633',       '002185', '002594','300115','600016','300059','600584']
#portfolios_monitor = ['600584','601633','002636','002594','300059','600895']
portfolios_monitor = ['600000','002185','002594','601633','603160','600663']
portfolios_monitor = ['600000','002185','002594','601633','603160','600663']
#tel = {'jack': 4098, 'sape': 4139}
#portfolios = {'002185': 3100 ,'002635':1000 , '300059':2400, '300077':1200,'600487':300,'600663':400,'601633':4100}
portfolios = [ ['002185',3100,'2017-12-10',7.951],['600597',1100,'2018-3-5',12.905],['300059',3500,'2017-12-30',14.289],['600663',400,'2017-11-8',20.003],['601633',2100,'2017-10-15',11.888],['600000',2100,'2018-3-5',12.603]]
portfolios_arr = np.array(portfolios)

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
     num = portfolios_arr.shape[0]
     deep_study('sh','上证综指',path)
     deep_study('sz','深证成指',path)
     deep_study('zxb','中小板',path)
     deep_study('cyb','创业板',path)
#     f.open("portfolios_analysis.csv",'w')
     print ("classic stock is under deep parsing     ------------------") 
#     for stock_code in portfolios_monitor:
     #for stock_code, amount in portfolios.items():
     count = 0 ;
     total_value = 0 ;
     total_cost = 0 ;
     price = 0 ;
     labels = []
     percentage = []
     print(portfolios_arr[:,:1]) ;
#     portfolios= [['002185', '23870.0','78'],['002635', '21780.0','66'],['300059','33432.0','58'],['300077','9804.0','73'],['600487','11385.0','83'],['600663', '7780.0' ,'110'],['601633','52234.0','134'],['600000','14003.0','0']] 
#     portfolios_arr = np.array(portfolios)
#     print(portfolios_arr)
     while count < num :
        try:
           stock_code = portfolios_arr[count,0]
           stock_name = basic_df['name'][stock_code]
           print (str(stock_code)+" stock is under deep parsing" + str(stock_name)) 
           price = deep_study(stock_code,str(stock_name),path)
           cost = float(portfolios_arr[count,3])
#           portfolios[stock_code] = price*amount 
           amount = (portfolios_arr[count,1])
           portfolios_arr[count,1] = float(price)*float(amount)
           total_value = float(price)*float(amount) + total_value 
           total_cost = float(cost)*float(amount) + total_cost
           datestr = portfolios_arr[count,2]
           date_time = datetime.datetime.strptime(datestr,'%Y-%m-%d')
           delta     = now - date_time ;
           if(int(delta.days) > 30):
             print ("!!!!!!!!!!!!!!!!"+str(stock_code)+" holding time exceed 30 days, please notice that !!!!!!!!!!!!!!!!!!!!!!!") 
           portfolios_arr[count,2] = delta.days
           realtime_study(stock_code,str(stock_name),path)
           labels.append(stock_code)
           percentage.append(float(price)*float(amount))
        except:
           traceback.print_exc()
           pass
        count = count + 1 
     print (portfolios_arr)
     print (percentage)
     print (labels)
     print (total_value)
     print (total_cost)
#     percentage = percentage 
     explode = (0, 0, 0, 0,0,0)  # only "explode" the 2nd slice (i.e. 'Hogs')
     fig1, ax1 = plt.subplots()
     ax1.pie(percentage, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
     ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
#     plt.show()
     plt.savefig("portion_pie",c='k')
