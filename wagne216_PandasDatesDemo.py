# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 23:11:42 2020

This code follows the tutorial for time series with Pandas, found at 
https://github.com/Environmental-Informatics/08-time-series-analysis-with-pandas-wagne216

Different dataset time series are analyzed: Arctic Oscillation, N. Atlantic Oscillation (AO, NAO)

@author: D
"""
#%%
# prepare modules: 
import pandas as pd
import numpy as np
from pandas import Series, DataFrame, Panel # imports specific commands so they won't need written out every time
# if using wget for the first time: 
# pip install wget
import wget # to download file
import datetime
import pylab as p

pd.set_option('display.max_rows',15) # this limit maximum numbers of rows

# check pandas version to see if things will work- this script is meant for pd >.8
pd.__version__

# % load datas

# save 'montlyAOdata' text file in this folder 
wget.download('https://www.cpc.ncep.noaa.gov/products/precip/CWlink/daily_ao_index/monthly.ao.index.b50.current.ascii',\
              r'..\08-time-series-analysis-with-pandas-wagne216-master')

# load file
ao = np.loadtxt('monthly.ao.index.b50.current.ascii')

# first 3 vals to demonstrate columns:
print(ao[0:2]) # col1 = year; col2 = month; col3 = value (units?)
# look at last row:
print(ao[-1])
# array shape (like size in matlab- row x col)
ao.shape

# % time-series

# generate time range based on first & last vals and existing shape; result = datetime w/ specified length:
dates = pd.date_range('1950-01', periods=ao.shape[0], freq='M') # M = month frequency; periods = # dp's

print(dates) # looks like
print(dates.shape) # size

# create AO time-series (ts) as pandas series
AO = Series(ao[:,2], index=dates) # uses dates as index column!!
print(AO)

# %% plot all of it: 
AO.plot()
p.savefig('Monthly Atlantic Oscillation (AO) plot.png',format='png') # 
# %% part of it (years): (if you run both of these, it highlights the 2nd plot in diff color)
AO['1980':'1990'].plot()
# smaller part (select months):
AO['1980-05':'1981-03'].plot()

# referencing time periods: 
print(AO[120]) # by number of 'period'
print()
print(AO['1960-01']) # by specific month- mult vals
print()
print(AO['1960']) # mult vals from a year
print()
print(AO[AO > 0]) # vals >0 w/ their indexes

# %% creating a dataframe by adding 2nd data
wget.download('https://www.cpc.ncep.noaa.gov/products/precip/CWlink/pna/norm.nao.monthly.b5001.current.ascii',\
              r'..\08-time-series-analysis-with-pandas-wagne216-master')

# load nao file
nao = np.loadtxt('norm.nao.monthly.b5001.current.ascii')

#check first & last, shape to see if same as ao:
print(nao[0])
print(nao[-1])
print(nao.shape) # luckily same length

# make date list & 2nd separate series also with times as index: 
dates_nao = pd.date_range('1950-01', periods=nao.shape[0], freq='M')
NAO = Series(nao[:,2], index=dates_nao)
NAO.index # check to see that the index is the nao datetime list. same as AO.index, yay

# create dataframe combining the 2: 
aonao = DataFrame({'AO' : AO, 'NAO' : NAO})

# %% working with the dataframe
# subplot the 2 datas: (automatically plots any additional columns in another subplot)
aonao.plot(subplots=True) 

# look at initial rows:
print(aonao.head()) # indexes still dates, then values as labeled columns

# ref column by 1. name (as a dataframe style:) or 2. as the variable
print(aonao['NAO'])
print(aonao.NAO)

# add column: diff of the 2 vals:
aonao['Diff'] = aonao['AO'] - aonao['NAO']
print(aonao.head())
# delete it: 
del aonao['Diff']

# preview end vals:
print(aonao.tail())

# look again at pieces of data: 
print(aonao['1981-01':'1981-03']) # jan to mar '81

# %% complicated filter combos: 
# bar plot of the result of filtering data as:
#    (1) positive AO vals (2) neg NAO vals (3) values afer 1/1/80 (4) vals before 1/1/89 (5) NAO vals
aonao.loc[(aonao.AO > 0) & (aonao.NAO < 0) 
        & (aonao.index > datetime.datetime(1980,1,1)) 
        & (aonao.index < datetime.datetime(1989,1,1)),
        'NAO'].plot(kind='barh')

# %% Stats
print(aonao.mean()) # for all data (each col)
print(aonao.max())
print(aonao.min())
print(aonao.mean(1)) # mean for each row
print(aonao.describe()) # count, mean, std, quartiles, max

# %% Resampling- to a diff time frequency

# from: AO to A mean
AO_mm = AO.resample("A").mean() # resamples to annual mean
print(AO_mm)
# looks like 
AO_mm.plot(style='g--')

# %% from: AO to A median
AO_mm = AO.resample("A").median() # resamples to annual med
print(AO_mm)
# add to same plot to see diff 
AO_mm.plot(style='b-')
p.savefig('Annual median values for AO.png',format='png') # 

# %%from: AO to 3 year A max
AO_mm = AO.resample("3A").apply(np.max) # resamples to 3-yr annual max
print(AO_mm)
# add again to same plot to see diff 
AO_mm.plot(style='y.')

# %% 3 methods in 1 pass:
AO_mm = AO.resample("A").apply(['mean', np.min, np.max]) # results in 3 columns
AO_mm['1900':'2020'].plot(subplots=True) # plot only 10 years of result as 3 subplots
AO_mm['1900':'2020'].plot() # all in 1 plot
print(AO_mm) # looks like

#%% Rolling stats (aka moving); window = # dp's include in mov mean
aonao.rolling(window=50, center=False).mean().plot() # don't specify style to get 2 auto colors
#% WRITE TO PNG
p.savefig('Rolling mean for both AO and NAO.png',format='png') # 

# %% Rolling correlation: # spec both var's differently
aonao.AO.rolling(window=120).corr(other=aonao.NAO).plot(style='-g')
# corr coefficients
print(aonao.corr())
