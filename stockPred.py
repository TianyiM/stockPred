# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 19:28:48 2020

@author: matia
"""

import pandas as pd
import datetime
import matplotlib.pyplot as plt
import statsmodels.tsa.api as smt
import statsmodels.api as sm
import pandas_datareader as web
import warnings
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
from sklearn.model_selection import train_test_split
import seaborn as sns
sns.set()

warnings.filterwarnings('ignore')

#Method 1； Use dataweb to get the data from yahoo directly
start = datetime.datetime(2016, 1, 1)
end = datetime.datetime(2019, 1, 30)
aapl = web.DataReader('AAPL', 'yahoo', start, end)
vol = aapl['High']
vol.plot()

#Method 2:Download CSV file directly, so we can set date not as index
amdPred = pd.read_csv('Dataset/AMD.csv',parse_dates=[0])
muPred = pd.read_csv('Dataset/MU.csv',parse_dates=[0])
tslaPred = pd.read_csv('Dataset/TSLA.csv',parse_dates=[0])

amdPred.columns = [x.strip() for x in amdPred.columns]
amdPred.columns = [x.replace(' ', '_') for x in amdPred.columns]
#这个地方直接通过shift算结果，但是你说的方法是对的，就是不应该这样写，RF还是主要用作分类
X = amdPred[[x for x in amdPred.columns if valid(x)]].iloc[:-20]
y = amdPred.Close.shift(-20).dropna()
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
rf_model = RandomForestRegressor()
rf_model.fit(X_train, y_train)
type(y_test)
res = rf_model.score(X_test, y_test)


