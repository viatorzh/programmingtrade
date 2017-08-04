#!/usr/bin/env python

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
#from __future__ import unicode_literals
#import sys
#type = sys.getfilesystemencoding()
import datetime
import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')
import tushare as ts
import pandas as pd
import numpy as np
import talib as ta
import math
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator, MonthLocator, DayLocator
from matplotlib.finance import fetch_historical_yahoo, candlestick_ochl, candlestick2_ohlc, volume_overlay
from matplotlib import gridspec
from matplotlib.mlab import csv2rec
from matplotlib.dates import num2date, date2num, IndexDateFormatter
from matplotlib.ticker import  IndexLocator, FuncFormatter
from matplotlib.font_manager import FontProperties
#import urllib2

#with PdfPages('foo.pdf') as pdf

class stock_study:
    def __init__(self,code,period):
        self.code = code
        self.period = period
        self.find_trend = False
        self.title_str = ""
        self.path = "pic"
# -------------------------------------------------------------
# initial the data frame and and if plot enable the plot will be intialled
# -------------------------------------------------------------
    def initial_df(self,plot,k_type,path):
        self.path = path ;
        now = datetime.datetime.now()
        # now.strftime('%Y-%m-%d')
        delta = datetime.timedelta(days = self.period)
   #    delta = datetime.timedelta(days = 60)
        ndays = now - delta
   #    fuquan data        
        if(k_type == "D"):
           if(self.code == "sh" or self.code == "sz" or self.code == "zxb" or self.code == "cyb"):
#             dff = ts.get_hist_data(self.code,start=ndays.strftime('%Y-%m-%d'))
             dff = ts.get_hist_data(self.code,start=ndays.strftime('%Y-%m-%d'))
           else:
#             dff = ts.get_hist_data(self.code,start=ndays.strftime('%Y-%m-%d'))
             dff = ts.get_h_data(self.code,start=ndays.strftime('%Y-%m-%d'))
#             dff = ts.get_k_data(self.code,start=ndays.strftime('%Y-%m-%d'))
        else:
#        no fuquan data        
           if(k_type == "60"):
               dff = ts.get_hist_data(self.code,start=ndays.strftime('%Y-%m-%d'),ktype='60')
           else:
               dff = ts.get_hist_data(self.code,start=ndays.strftime('%Y-%m-%d'),ktype="W")
#           dff = ts.get_k_data(self.code,start=ndays.strftime('%Y-%m-%d'),ktype="W")
        self.df = dff[::-1] 
        if plot != 0:
             ma5  = ta.MA(np.array(self.df['close']),5,matype=0)
             ma10 = ta.MA(np.array(self.df['close']),10,matype=0)
             ma20 = ta.MA(np.array(self.df['close']),20,matype=0)
             if ma5[-1] > ma20[-1]:
                     if self.df['close'][-1] > ma5[-1]:
                        print(" the stock "+str(self.code)+" is bull! ") ;
                        self.title_str = str(self.code)+" is bull! " 
             if ma5[-1] < ma20[-1]:
                     if self.df['close'][-1] < ma5[-1]:
                        print(" the stock "+str(self.code)+" is bear! ") ;
                        self.title_str = str(self.code)+" is bear! " 
             fig = plt.figure()
             fig.subplots_adjust(bottom=0.1)
             fig.subplots_adjust(hspace=0)
             gs = gridspec.GridSpec(2, 1, height_ratios=[4, 1])
             self.ax0 = plt.subplot(gs[0])
             self.ax1 = plt.subplot(gs[1], sharex=self.ax0)
             candles = candlestick2_ohlc(self.ax0,self.df['open'], self.df['high'], self.df['low'], self.df['close'], width=1, colorup='r', colordown='g') ;
             self.ax0.plot(ma5, color = 'black',lw=2,)
             self.ax0.plot(ma20, color = 'yellow',lw=2)
             self.ax0.plot(ma10, color = 'green',lw=2)



    def initial_extream_point(self,plot):
#         print(self.df['close'].count()) ;
         total_cnt = self.df['close'].count() 
         if total_cnt < 20:
            return False
         maxidx = self.df['close'].idxmax(axis=1)
         minidx = self.df['close'].idxmin(axis=1)
         #now = datetime.datetime.now()
         # now.strftime('%Y-%m-%d')
         #detla = datetime.timedelta(days = 120)
         #ndays = now - delta
         #dff = ts.get_hist_data(self.code,start=ndays.strftime('%Y-%m-%d'),ktype=k_type)
         #dff = dff[::-1] 
         price_diff = self.df['close'][maxidx] - self.df['close'][minidx] 
         maxcnt = self.df['close'][:maxidx].count() 
         mincnt = self.df['close'][:minidx].count() 
	 # if it is up
         if maxidx > minidx :
            minidx2 = self.df['close'][maxidx:].idxmin(axis=1) ;
            maxidx2 = self.df['close'][:minidx].idxmax(axis=1) ;
#            print ("- min index 0 1 is "+str( self.df['close'][:minidx].count())+" "+str( self.df['close'][:minidx2].count())+" min price0/1 is "+"max idx 0 1 is "+(str(self.df['close'][:maxidx].count()))+" "+(str(self.df['close'][:maxidx2].count())))  
            idx_diff = maxcnt - mincnt + 1 
	    # in case the wave trend is very very narrow
            if maxcnt < total_cnt * 0.4:
                maxidx2 = self.df['close'][minidx2:].idxmax(axis=1) ;
#                print ("-- min index 0 1 is "+str( self.df['close'][:minidx].count())+" "+str( self.df['close'][:minidx2].count())+" min price0/1 is "+"max idx 0 1 is "+(str(self.df['close'][:maxidx].count()))+" "+(str(self.df['close'][:maxidx2].count())))  
            if mincnt >  total_cnt * 0.7:
                minidx2 = self.df['close'][:maxidx2].idxmax(axis=1) ;
#                print ("-- min index 0 1 is "+str( self.df['close'][:minidx].count())+" "+str( self.df['close'][:minidx2].count())+" min price0/1 is "+"max idx 0 1 is "+(str(self.df['close'][:maxidx].count()))+" "+(str(self.df['close'][:maxidx2].count())))  

            if price_diff > self.df['close'][-1] * 0.1:
                second_max_idx = minidx 
                second_min_idx = maxidx
               #for idx in range(minidx:maxidx):
	       # here i want to find the sub wave between the main wave which i can draw the trend line
                for idx in self.df.index[mincnt:maxcnt]:
                       if self.df['close'][idx] - self.df['close'][minidx] > price_diff * 0.3 and second_min_idx == maxidx :
                               second_max_idx = idx 
                       if self.df['close'][second_max_idx] - self.df['close'][idx] > price_diff * 0.3 :
                            if self.df['close'][second_min_idx] > self.df['close'][idx] :
                               second_min_idx = idx 
                       if second_min_idx != maxidx:
                               if self.df['close'][idx] > self.df['close'][second_max_idx]:
                                       maxidx2 = second_max_idx
                                       minidx2 = second_min_idx
                                       self.find_trend = True
#                                       print ("--- min index 0 1 is "+str( self.df['close'][:minidx].count())+" "+str( self.df['close'][:minidx2])+" min price0/1 is "+"max idx 0 1 is "+(str(self.df['close'][:maxidx].count()))+" "+(str(self.df['close'][:maxidx2].count())))  
#                                       break
            else:
               self.find_trend = False
#               return False
         # if down
         else:
            idx_diff = mincnt - maxcnt + 1 
            maxidx2 = self.df['close'][minidx:].idxmax(axis=1) ;
            minidx2 = self.df['close'][:maxidx].idxmin(axis=1) ;
#            print ("x min index 0 1 is "+str(self.df['close'][:minidx].count())+" "+str(self.df['close'][:minidx2].count())+" min price0/1 is "+"max idx 0 1 is "+(str(self.df['close'][:maxidx].count()))+" "+(str(self.df['close'][:maxidx2].count())))  
	    # in case
            if mincnt < total_cnt * 0.4:
                minidx2 = self.df['close'][maxidx2:].idxmin(axis=1) ;
#                print ("xx min index 0 1 is "+str( self.df['close'][:minidx].count())+" "+str( self.df['close'][:minidx2].count())+" min price0/1 is "+"max idx 0 1 is "+(str(self.df['close'][:maxidx].count()))+" "+(str(self.df['close'][:maxidx2].count())))  
            if maxcnt >  total_cnt * 0.7:
                maxidx2 = self.df['close'][:minidx2].idxmax(axis=1) ;
#                print ("xx min index 0 1 is "+str( self.df['close'][:minidx].count())+" "+str( self.df['close'][:minidx2].count())+" min price0/1 is "+"max idx 0 1 is "+(str(self.df['close'][:maxidx].count()))+" "+(str(self.df['close'][:maxidx2].count())))  
            if price_diff > self.df['close'][-1] * 0.1:
                second_max_idx = minidx 
                second_min_idx = maxidx
	       #for idx in range(maxidx:minidx):
                for idx in self.df.index[maxcnt:mincnt]:
                       if self.df['close'][maxidx] - self.df['close'][idx] > price_diff * 0.3 and second_max_idx == minidx:
                               second_min_idx = idx 
                       if self.df['close'][idx] - self.df['close'][second_min_idx] > price_diff * 0.3 :
                            if self.df['close'][second_max_idx] < self.df['close'][idx] :
                               second_max_idx = idx 
                       if second_max_idx != minidx:
                               if self.df['close'][idx] < self.df['close'][second_min_idx]:
                                       maxidx2 = second_max_idx
                                       minidx2 = second_min_idx
                                       self.find_trend = True
#                                       print ("xxx min index 0 1 is "+str( self.df['close'][:minidx].count())+" "+str( self.df['close'][:minidx2].count())+" min price0/1 is "+"max idx 0 1 is "+(str(self.df['close'][:maxidx].count()))+" "+(str(self.df['close'][:maxidx2].count())))  
#                                       break
            else:
               self.find_trend = False
         if plot != 0:
            self.ax0.plot([self.df['close'][:minidx].count(),self.df['close'].count()],[self.df['close'][maxidx]-price_diff*0.618,self.df['close'][maxidx]-price_diff*0.618],'b--') ;
            self.ax0.plot([self.df['close'][:minidx].count(),self.df['close'].count()],[self.df['close'][maxidx]-price_diff*0.382,self.df['close'][maxidx]-price_diff*0.382],'b--') ;
            self.ax0.plot([self.df['close'][:minidx].count(),self.df['close'][:maxidx].count()],[self.df['close'][minidx],self.df['close'][maxidx]],'r-') 
         
         self.maxidx = maxidx 
         self.minidx = minidx 
         self.maxidx2 = maxidx2 
         self.minidx2 = minidx2
        # if idx_diff > int(self.df['close'].count() * 0.3):
         if price_diff > self.df['close'][-1] * 0.1 and idx_diff > 10:
           return True
         else:
           return False

    
    def check_week_k(self):
       print("start weekly k parse"+str(self.df['close'].count())) 
       if(self.df['close'].count() < 20):
            return False 
       if(self.minidx < self.minidx2):
            y2 = self.df['close'][self.minidx2] 
            y1 = self.df['close'][self.minidx] 
            x2 = self.df['close'][:self.minidx2].count() 
            x1 = self.df['close'][:self.minidx].count() 
            a = (y2 - y1)/(x2 - x1) ;
            b = (y1*x2 - x1*y2)/(x2 - x1) ;
            yy = a * self.df['close'].count() + b ;
            if((self.df['low'][-1] < yy and self.df['high'][-1] > yy) or (self.df['low'][-2] < yy and self.df['high'][-2] > yy)):
                return True 
            return False 
	    

    def plot_trend(self):
#        if self.find_trend:
        y2 = self.df['close'][self.minidx2] 
        y1 = self.df['close'][self.minidx] 
        x2 = self.df['close'][:self.minidx2].count() 
        x1 = self.df['close'][:self.minidx].count() 
        a = (y2 - y1)/(x2 - x1) ;
        b = (y1*x2 - x1*y2)/(x2 - x1) ;
#        print ("min index 0 1 is "+str(x1)+" "+str(x2)+" min price0/1 is "+str(y1)+" "+str(y2)+"max idx 0 1 is "+(str(self.df['close'][:self.maxidx].count()))+" "+(str(self.df['close'][:self.maxidx2].count())))  
        self.ax0.plot([self.df['close'][:self.maxidx].count(),self.df['close'][:self.maxidx2].count()],[self.df['close'][self.maxidx],self.df['close'][self.maxidx2]],'--')
        self.ax0.plot([1,self.df['close'].count()],[a+b,a*self.df['close'].count()+b],'-') 

    def macd_analysis(self,plot):
        macd,macdsignal,macdhist = ta.MACD(np.array(self.df['close']), fastperiod = 12,slowperiod = 26 , signalperiod = 9)
        stdDev = ta.STDDEV(np.array(self.df['close']),timeperiod=20)
        macd[0:33] = np.zeros(33)
        macdsignal[0:33] = np.zeros(33)
        macdhist[0:33] = np.zeros(33)
        if macdhist[-1] < macdhist[-2] and macdhist[-2] < macdhist[-3]:
          print (str(self.code)+" macd is NOT friendly")
        if macdhist[-1] > macdhist[-2] and macdhist[-2] > macdhist[-3]:
          print (str(self.code)+" macd is friendly")
        if plot != 0:
            self.ax1.plot(macd,color='blue',lw=2) ;
            self.ax1.plot(macdsignal,color='red',lw=2) ;
            self.ax1.plot(stdDev,color='green',lw=3) ;
            self.ax1.plot(macdhist) # ,color='black',lw=3) ;
#        self.ax1.hist(macdhist) # ,color='black',lw=3) ;
        if self.find_trend:
            maxidx_cnt  = self.df['close'][:self.maxidx].count() 
            maxidx2_cnt = self.df['close'][:self.maxidx2].count() 
            minidx_cnt  = self.df['close'][:self.minidx].count() 
            minidx2_cnt = self.df['close'][:self.minidx2].count() 
#            print("maxidx is "+str(maxidx_cnt)+" macdhist is "+str(macdhist[maxidx_cnt]))
#            print("maxidx2 is "+str(maxidx2_cnt)+" macdhist 2 is "+str(macdhist[maxidx2_cnt]))
            if self.maxidx > self.minidx:
                 if macdhist[maxidx_cnt] < macdhist[maxidx2_cnt]:
                     print (str(self.code)+" macd top beili")
                 if self.df['volume'][self.maxidx] < self.df['volume'][self.maxidx2]:
                     print (str(self.code)+" macd top volume beili")
                 return False
            else:
                 if macdhist[minidx_cnt] > macdhist[minidx2_cnt]:
                     print (str(self.code)+" macd bottom beili")
                     return True
                 if self.df['volume'][self.minidx] < self.df['volume'][self.minidx2]:
                     print (str(self.code)+"macd bottom volume beili")
                 return False

    def save_plt(self,stock_name,basic_df):
        optional_str = ""
#        if(self.code != "sh" and self.code != "sz"):
        if(self.code != "sh" and self.code != "sz" and self.code != "cyb" and self.code != "zxb"):
            optional_str = "pe is:"+str(basic_df['pe'][self.code])+" change per"+str((self.df['close'][-1] - self.df['close'][-2])*100/self.df['close'][-2]) 
        font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=15)
        #title_string = str(self.code)+ " analysis "+str(stock_name)+self.title_str
        title_str= str(self.code)+ " analysis "+str(stock_name)+self.title_str+optional_str
        #plt.title(unicode("这个是一个测试的浦发银行").encode("utf-8")+"600000",fontproperties=font_set)
        plt.title(title_str)
        plt.savefig("./"+self.path+"/"+stock_name,c='k')

    def show_plt(self,stock_name,basic_df):
        optional_str = ""
        if(self.code != "sh" and self.code != "sz" and self.code != "cyb" and self.code != "zxb"):
            optional_str = "pe is:"+str(basic_df['pe'][self.code])+" change per"+str((self.df['close'][-1] - self.df['close'][-2])*100/self.df['close'][-2]) 
#        name = stock_name.decode('utf-8').encode(type) ;
        font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=15)
        title_str = str(self.code)+ " analysis "+str(stock_name)+self.title_str+optional_str
        #plt.title(u"中文".encode('utf-8'),fontproperties=font_set)
        #plt.title(str(self.code)+ " analysis "+str(stock_name)+self.title_str)
        plt.title(title_str)
        plt.show()
#        plt.savefig(str(self.code),c='k')
        #pdf.savefig()



#check if it is the real time k reverse
    def check_kpattern(self):
        N = 20
        volma = ta.MA(np.array(self.df['volume']),N,matype=0)
        threshold = volma[-1] * 1.5 
        if self.df['volume'].count() < 5:
           return False
        if self.df['close'][-1] < self.df['open'][-1]:
           if self.df['close'][-1] < self.df['open'][-2] and self.df['open'][-1] > self.df['close'][-2]:
              return -1
        if self.df['close'][-1] > self.df['open'][-1]:
           if self.df['close'][-1] > self.df['open'][-2] and self.df['open'][-1] < self.df['close'][-2]:
              return 1
        return False

    def check_vol(self):
        N = 20
        volma = ta.MA(np.array(self.df['volume']),N,matype=0)
        threshold = volma[-1] * 1.5 
        if self.df['volume'].count() < 5:
           return False
        if self.df['volume'][-1] > threshold:
           return True
        if self.df['volume'][-2] > threshold:
           return True
        if self.df['volume'][-3] > threshold:
           return True
        return False

#    def check_liquid(self):
#        stock_url = "http://data.eastmoney.com/zjlx/"+str(code)+".html" 
#        req = urllib2.Request(stock_url)
#        resp = urllib2.urlopen(stock_url)
#        respHtml = resp.read()
#        print("respHtml=",respHtml)

    def check_ene(self):
        M1 = 9
        N = 11
        M2 = 10
        ma = ta.MA(np.array(self.df['close']),N,matype=0) 
        ENEbotline = (1-M2/100) * ma 
        ENEtopline = (1+M1/100) * ma 
        if self.df['low'].count() < 3:
           return False 
        self.ax0.plot(ENEbotline, color = 'pink',lw=2)
        self.ax0.plot(ENEtopline, color = 'pink',lw=2)
        self.ax0.plot(ma, color = 'black',lw=2)
        if self.df['high'][-1] > ENEtopline[-1]:
      	    print("check ENE find ene high break for "+str(self.code)) 
#            self.title_str = self.title_str+"ENE high reached"
        if self.df['low'][-1] < ENEbotline[-1]:
      	    print("check ENE find ene low break for "+str(self.code)) 
#            self.title_str = self.title_str+"ENE low break" 
#      	    print("buy!!!") 
      	    return True
        elif self.df['low'][-2] < ENEbotline[-2]:
      	    print("check ENE find ene low break for "+str(self.code)) 
#            self.title_str = self.title_str+"ENE low break " 
#      	    print("buy!!!") 
      	    return True
        elif self.df['low'][-3] < ENEbotline[-3]:
      	    print("check ENE find ene low break for "+str(self.code)) 
#            self.title_str = self.title_str+"ENE low break " 
#            self.title_str = str(self.code)+" is bull! " 
#      	    print("buy!!!") 
      	    return True
#        elif self.df['high'][-1] > ENEtopline[-1]:
#      	    print("check ENE find ene top break for "+str(self.code)) 
##     	    print("sell !!!") 
#      	    return False
        else:
      	    return False
     
    def generate_training_data(self,basic_df):
# extend the period to generate the training data
        count = self.df['close'].count() 
        period = self.period + 50 
        now = datetime.datetime.now()
        delta = datetime.timedelta(days = period)
        ndays = now - delta
        print(ndays.strftime('%Y-%m-%d'))
        dff = ts.get_h_data(self.code,start=ndays.strftime('%Y-%m-%d'))
        #df = dff[::-1]
        #print(dff)
        df = dff[::-1] 
        ma5  = ta.MA(np.array(df['close']),5,matype=0)
        ma10 = ta.MA(np.array(df['close']),10,matype=0)
        ma20 = ta.MA(np.array(df['close']),20,matype=0)
        stdDev = ta.STDDEV(np.array(df['close']),timeperiod=20)
        buy_line = ma5
# may have issues because we cannot get enough data
        f = open("training_data_"+str(self.code)+".csv", 'w')
        j = 50 
        f.write("price,vol,ma5c,ma20,maxidx,minidx,maxprice,minprice,diff,pe,outstanding totals,stdv,Y\n") 
        for idx in df.index[50:]:
            price = df['close'][idx] 
            vol   = df['volume'][idx] 
            ma5c  = ma5[j] 
            ma20c  = ma20[j] 
            idxcnt = df['close'][:idx].count()
            maxidx = df['close'][idxcnt-50:idxcnt].idxmax(axis=1)
            minidx = df['close'][idxcnt-50:idxcnt].idxmin(axis=1)
            #minidx = df['close'][idx-50:idx].idxmin(axis=1)
            maxprice= df['close'][maxidx]
            minprice= df['close'][minidx]
            maxcnt  =  df['close'][:maxidx].count()
            mincnt  =  df['close'][:minidx].count()
            diff = maxcnt - mincnt 
            stdv    = stdDev[j]
# generate the Y , check if the next 20 days 10% up and no more than 3% down
            up_flag = 0 
            dn_flag = 0 
            j = j + 1
# may have issues because we cannot get enough data
            for i in range(1,22):
            #     if (idx + i) > count + 50:
            #          break 
                 #if(df['close'][idx+i]/df['close'][idx]  > 1.1):
                 if(df['close'][idxcnt+i]/df['close'][idx]  > 1.1):
                      up_flag = 1 
                 if(df['close'][idxcnt+i]/df['close'][idx]  < 0.97):
                      dn_flag = 1 
            if up_flag == 1 and dn_flag == 0 :
                 Y = 1 
            else:
                 Y = -1 
            if Y == 1:
      	         buy_line[j] = self.df['close'][idx] - 1 
      	         print("finally we found a Y = 1 sample!!!!!!!!!!!!!!!!!!"+str(self.code)+"\n") 
            else:
      	         buy_line[j] = 0 
            f.write(str(price)+","+str(vol)+","+str(ma5c)+","+str(ma20c)+","+str(maxcnt)+","+str(mincnt)+","+str(maxprice)+","+str(minprice)+","+str(diff)+","+str(basic_df['pe'][self.code])+","+str(basic_df['outstanding'][self.code])+","+str(stdv)+","+str(Y)+"\n") 
	    # regularity
            f.write(str(price)+","+str(vol)+","+str(ma5c/price)+","+str(ma20c/price)+","+str(maxcnt/10)+","+str(mincnt/10)+","+str(maxprice/price)+","+str(minprice/price)+","+str(diff/10)+","+str(basic_df['pe'][self.code]/10)+","+str(basic_df['outstanding'][self.code])+","+str(stdv)+","+str(Y)+"\n") 
        f.close()
        self.ax0.plot(buy_line, color = 'orange',lw=1,)
