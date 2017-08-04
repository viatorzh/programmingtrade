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
#   concept_df.to_csv('concept_new.csv')
   industry_df = ts.get_industry_classified()
   industry_df.to_csv('industry_new.csv')
   # small and chuangye
   try:
#       startup_df = ts.get_gem_classified()
#       sm_df = ts.get_sme_classified()
       basic_df = ts.get_stock_basics()
   except:
       traceback.print_exc()
       pass
#   print(startup_df)
   
#   print("start to parse startup stocks\n") ;
   fhw = open('filew.txt','w')
   
   for idx in industry_df.index:
     try:
        code = industry_df['code'][idx]
        print(code)
        pe     = basic_df['pe'][code]
        totals = basic_df['totals'][code]
        outstanding = basic_df['outstanding'][code]
        gpr = basic_df['gpr'][code]
        if(pe < 50 and pe != 0 and outstanding < 200000 and gpr >= 10):
#        if(pe < 50 and pe != 0 and outstanding < 200000 and outstanding/totals < 0.8 and gpr >= 10):
                   industry_pool.append(code)
                   industry = basic_df['industry'][code]
                   name = basic_df['name'][code]
                   price = basic_df['pb'][code] * basic_df['bvps'][code] 
                   write_line = str(code)+","+str(name)+","+str(industry)+","+str(pe)+","+str(outstanding)+","+str(price)+"\n"
                   fhw.write(write_line)
   #                print(str(startup_df['code'][idx])+" pe is "+str(pe))
     except:
       traceback.print_exc()
       pass
   fhw.write(write_line)

   for idx in concept_df.index:
     try:
        code = concept_df['code'][idx]
        print(code)
        pe     = basic_df['pe'][code]
        totals = basic_df['totals'][code]
        outstanding = basic_df['outstanding'][code]
        gpr = basic_df['gpr'][code]
        if(pe < 50 and pe != 0 and outstanding < 200000 and gpr >= 10):
#        if(pe < 50 and pe != 0 and outstanding < 200000 and outstanding/totals < 0.8 and gpr >= 10):
                   industry = basic_df['industry'][code]
                   concept = concept_df['c_name'][idx]
                   name = basic_df['name'][code]
                   price = basic_df['pb'][code] * basic_df['bvps'][code] 
                   write_line = str(code)+","+str(name)+","+str(industry)+","+str(pe)+","+str(outstanding)+","+str(concept)+","+str(price)+"\n"
                   fhw.write(write_line)
   #                print(str(startup_df['code'][idx])+" pe is "+str(pe))
     except:
       traceback.print_exc()
       pass
   
   print(industry_pool)
#   industry_pool.to_csv(pool.csv)


if __name__=="__main__":
     industry_pool = []
     initial_pool() 

