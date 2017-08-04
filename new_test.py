import datetime
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
from matplotlib import pyplot
from matplotlib.font_manager import FontProperties

dff = ts.get_hist_data("600000",start="2017-04-01")
df = dff[::-1]
fig = plt.figure()
fig.subplots_adjust(bottom=0.1)
fig.subplots_adjust(hspace=0)
gs = gridspec.GridSpec(2, 1, height_ratios=[4, 1])
ax0 = plt.subplot(gs[0])
ax1 = plt.subplot(gs[1], sharex=ax0)
candles = candlestick2_ohlc(ax0,df['open'], df['high'], df['low'], df['close'], width=1, colorup='r', colordown='g') ;
font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=15)
plt.title(u"这个是一个测试的浦发银行"+"600000",fontproperties=font_set)
plotlib.text.Text object at 0x00000289D07E2DD8>
plt.show()

