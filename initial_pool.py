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
import tushare as ts
import pandas as pd
import numpy as np
import tushare as ts

#if __name__=="__main__":

# index_tech_analysis('sh','D') 
# index_tech_analysis('sh','W') 
# index_tech_analysis('sz','D') 

#now = datetime.datetime.now()
# now.strftime('%Y-%m-%d')
#delta = datetime.timedelta(days = 60)
#ndays = now - delta

industry_df = ts.get_industry_classified()
print(industry_df)
industry_df.to_csv('industry.csv')
concept_df = ts.get_concept_classified()
print(concept_df)
concept_df.to_csv('concept.csv')
area_df = ts.get_area_classified()
print(area_df)
area_df.to_csv('area.csv')
sm_df = ts.get_sme_classified()
print(sm_df)
sm_df.to_csv('sm.csv')
startup_df = ts.get_gem_classified()
print(startup_df)
startup_df.to_csv('startup.csv')
basic_df = ts.get_stock_basics()
basic_df.to_csv('basic.csv')

a_concept_list = []
for idx in concept_df.index:
    if(concept_df['c_name'][idx] == '汽车电子'):
        a_concept_list.append(concept_df['code'][idx])

print("汽车电子 concept is ")
print(a_concept_list)
