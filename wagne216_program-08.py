# -*- coding: utf-8 -*-
"""
Assignment 8: Time Series Analysis with Pandas

Running this script will: 
    
    1. Read WabashRiver_DailyDischarge_20150317-20160324.txt
    2. Plot streamflow and write to pdf output
    3. Plot 10 highest stremflow events and write to pdf output
    4. Plot monthly avg streamflow and write to pdf output
    
@author: wagne216

"""
# %%
# prepare modules: 
import pandas as pd
import numpy as np
import matplotlib.pyplot as m
from pandas import Series, DataFrame, Panel # imports specific commands so they won't need written out every time
#import datetime
import pylab as p

# import data file provided: (3/17/15-3/24/16 daily Wabash discharge (ft^3))
file = r'WabashRiver_DailyDischarge_20150317-20160324.txt'
wd = pd.read_table(file,parse_dates=True,skiprows=11,header=13,index_col=2) # headers auto assigned; specify index as date col
# drop row of nondata that gets imported
wd = wd.drop(['20d'])
# use timezone column to specify dates timezone
wd.index.tz = wd['tz_cd']
# make it easier to reference the values as the discharge unts: cfps (ft^3/s): 
wd = wd.rename(columns={'01_00060':'cfps'})
# create series for discharge; convert cfps from str to num, and time-str col to datetime col:
WD = Series(pd.to_numeric(wd.cfps),index=pd.to_datetime(wd.index))
#%% PLOTS

# Daily mean streamflow
WD_dailymean = WD.resample("D").mean() # resamples to annual mean
print(WD_dailymean)
# looks like 
WD_dailymean.plot(style='g--')
m.title('Wabash Daily Mean Streamflow')
m.ylabel('Discharge (ft$^{3}$/s)')
# save as pdf: 
p.savefig('Daily Mean Streamflow.pdf',format='pdf') # 

# %% 10 highest streamflows vs Daily streamflow: 
WD_topten = WD_dailymean.sort_values(ascending=False)[0:9]
WD.plot(style='orange',legend=True,label='Daily Discharge')
WD_topten.plot(style='b^',marker='^',legend=True,label='Top 10 Mean Daily') # specify marker to show up in legend
m.title('Wabash Top 10 Days of Mean Streamflow vs Daily Flow')
m.ylabel('Discharge (ft$^{3}$/s)')
m.show
# save as pdf:
p.savefig('Top 10 Mean Streamflow.pdf',format='pdf') # 

#%% Monthly mean streamflow
WD_monthlymean = WD.resample("M").mean() # resamples to annual mean
print(WD_dailymean)
# looks like 
WD_monthlymean.plot(style='m')
m.title('Wabash Monthly Mean Streamflow')
m.ylabel('Discharge (ft$^{3}$/s)')
# save as pdf: 
p.savefig('Monthly Mean Streamflow.pdf',format='pdf') # 

