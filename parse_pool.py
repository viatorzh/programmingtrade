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


def initial_pool():
   concept_df = ts.get_concept_classified()
   for idx in concept_df.index:
       if(concept_df['c_name'][idx] == "汽车电子"):
           a_concept_list.append(concept_df['code'][idx])
   
   print("汽车电子 concept is ")
   #concept_df.to_csv('concept.csv')
   
   industry_df = ts.get_industry_classified()
   for idx in industry_df.index:
       if(concept_df['c_name'][idx] == "电子器件"):
           a_concept_list.append(concept_df['code'][idx])
       if(concept_df['c_name'][idx] == "电子信息"):
           a_concept_list.append(concept_df['code'][idx])
   print(a_concept_list)
   # print(industry_df)
   #industry_df.to_csv('industry.csv')
   try:
       startup_df = ts.get_gem_classified()
       sm_df = ts.get_sme_classified()
       basic_df = ts.get_stock_basics()
   except:
       traceback.print_exc()
       pass
   print(startup_df)
   
   print("start to parse startup stocks\n") ;
   
   for idx in startup_df.index:
   	pe = basic_df['pe'][startup_df['code'][idx]]
   	if(pe < 80 and pe != 0):
                   startup_pool.append(startup_df['code'][idx])
   #                print(str(startup_df['code'][idx])+" pe is "+str(pe))
   
   print(startup_pool)
   print("start to parse small and middle stocks\n") ;
   for idx in sm_df.index:
   	pe = basic_df['pe'][sm_df['code'][idx]]
   	if(pe < 50 and pe != 0):
                   sm_pool.append(sm_df['code'][idx])
#                   print(str(sm_df['code'][idx])+" pe is "+str(pe))

def ene_select():
    for code in startup_pool:
        try:
            s = stock_study(code,20)
            s.initial_df(0,"D")
            print (str(code)+" stock is under parsing") 
            if(s.check_ene()):
                print("the stock " + str(code) +" ene is break, maybe we could do some investigate about it") 
                a_enelist.append(code)
        except:
            traceback.print_exc()
            pass
    
    print(a_enelist) 
    
    for code in sm_pool:
        try:
            s = stock_study(code,20)
            s.initial_df(0,"D")
            print (str(code)+" stock is under parsing") 
            if(s.check_ene()):
                print("the stock " + str(code) +" ene is break, maybe we could do some investigate about it") 
                a_enelist.append(code)
        except:
            traceback.print_exc()
            pass
    
    print(a_enelist) 

 

def wave_select():
    print("start to wave select stocks") 
    for code in startup_pool:
        try:
            print (str(code)+" stock is under parsing") 
            s = stock_study(code,20)
            s.initial_df(0,"D")
            s = stock_study(code,100)
            s.initial_df(0,"D")
            if(s.initial_extream_point(0) and s.macd_analysis(0) and s.check_vol()):
                print("the stock " + str(code) +" wave matches model and volume abnormal maybe we could do some investigate about it") 
                a_wavelist.append(code)
            else:
                if(s.find_trend):
                   a_wavelist.append(code)
        except:
            traceback.print_exc()
            pass
    
    for code in sm_pool:
        try:
            print (str(code)+" stock is under parsing") 
            s = stock_study(code,20)
            s.initial_df(0,"D")
            s = stock_study(code,100)
            s.initial_df(0,"D")
            if(s.initial_extream_point(0) and s.check_vol() and s.macd_analysis(0)):
                print("the stock " + str(code) +" wave matches model and volume abnormal maybe we could do some investigate about it") 
                a_wavelist.append(code)
        except:
            traceback.print_exc()
            pass
    for code in a_concept_list:
        try:
            print (str(code)+" stock is under parsing") 
            s = stock_study(code,20)
            s.initial_df(0,"D")
            s = stock_study(code,100)
            s.initial_df(0,"D")
            if(s.initial_extream_point(0) and s.macd_analysis(0) and s.check_vol()):
                print("the stock " + str(code) +" wave matches model and volume abnormal maybe we could do some investigate about it") 
                a_wavelist.append(code)
        except:
            traceback.print_exc()
            pass
    
    print(a_wavelist) 

def deep_study(code):
     s = stock_study(code,100)
     s.initial_df(1,"D") 
     print (str(code)+" stock is under wave analysis") 
     if s.initial_extream_point(1): 
       print (str(code)+" trend existed") 
     if s.find_trend: 
       print (str(code)+" trend found sub wave") 
     s.plot_trend() 
     print (str(code)+" stock is under macd analysis") 
     s.macd_analysis(1)
     print (str(code)+" stock is plotting itself") 
     s.show_plt()

def week_trend():
    print("start to week trend analyze stocks") 
    for code in startup_pool:
        try:
            print (str(code)+" stock is under parsing") 
            s = stock_study(code,300)
            s.initial_df(0,"W")
            s.initial_extream_point(0)
            if(s.check_week_k()):
                print("the stock " + str(code) +" wave matches model, we could do some investigate about it") 
                a_weektrend.append(code)
        except:
            traceback.print_exc()
            pass
    
    for code in sm_pool:
        try:
            print (str(code)+" stock is under parsing") 
            s = stock_study(code,300)
            s.initial_df(0,"W")
            s.initial_extream_point(0)
            if(s.check_week_k()):
                print("the stock " + str(code) +" wave matches model, we could do some investigate about it") 
                a_weektrend.append(code)
        except:
            traceback.print_exc()
            pass
    for code in a_concept_list:
        try:
            print (str(code)+" stock is under parsing") 
            s = stock_study(code,300)
            s.initial_df(0,"W")
            s.initial_extream_point(0)
            if(s.check_week_k()):
                print("the stock " + str(code) +" wave matches model, we could do some investigate about it") 
                a_weektrend.append(code)
        except:
            traceback.print_exc()
            pass
    
    print(a_weektrend) 

def buy_analysis():
    print("--------------------------------------------------------------------") 
    print("start to parse if the stock in the pool has the potential to be buy") 
    print("--------------------------------------------------------------------") 
    for code in stock_pool:
        try:
            print (str(code)+" stock is under parsing") 
            s = stock_study(code,300)
            s.initial_df(0,"D")
            s.initial_extream_point(0)
            if(s.check_ene()):
                print("the stock " + str(code) +" ene break, we could buy some positions") 
#                a_weektrend.append(code)
            
            s.initial_df(0,"W")
            s.initial_extream_point(0)
            if(s.check_week_k()):
                print("the stock " + str(code) +" week level k is at resistance place, we could buy some positions") 
                s.initial_df(1,"W")
                s.initial_extream_point(1)
                s.plot_trend()
                s.macd_analysis()
                s.show_plt()
        except:
            traceback.print_exc()
            pass
    
    for code in sm_pool:
        try:
            print (str(code)+" stock is under parsing") 
            s = stock_study(code,300)
            s.initial_df(0,"W")
            s.initial_extream_point(0)
            if(s.check_week_k()):
                print("the stock " + str(code) +" wave matches model, we could do some investigate about it") 
                a_weektrend.append(code)
        except:
            traceback.print_exc()
            pass
    for code in a_concept_list:
        try:
            print (str(code)+" stock is under parsing") 
            s = stock_study(code,300)
            s.initial_df(0,"W")
            s.initial_extream_point(0)
            if(s.check_week_k()):
                print("the stock " + str(code) +" wave matches model, we could do some investigate about it") 
                a_weektrend.append(code)
        except:
            traceback.print_exc()
            pass
    
    print(a_weektrend) 

portfolios_monitor = ['600895','002405','002594','300024','002230'      ,'601633',       '002185', '002456','300115','600016','600000','300059','600584']
portfolios_monitor = ['sh','600895','002405','002594','300024','002230'      ,'601633',       '002185', '002456','300115','600016','600000','300059','600584']
portfolios_monitor = ['sh','600895','002405','002456','300024','002230'      ,'601633',       '002185', '002594','300115','600016','600000','300059','600584']


if __name__=="__main__":
     for stock_code in portfolios_monitor:
        try:
           print (str(stock_code)+" stock is under deep parsing") 
           deep_study(stock_code)
        except:
           traceback.print_exc()
           pass
     startup_pool = []
     sm_pool= []
     a_enelist = []
     a_wavelist = []
     a_weektrend = []
     a_concept_list = []
     initial_pool() 
#     ene_select()
     wave_select()
     week_trend()

