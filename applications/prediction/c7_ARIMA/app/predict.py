#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 11:44:55 2019

@author: davidzhou
"""

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from statsmodels.tsa.arima_model import ARIMA
import time

scaler = MinMaxScaler(feature_range=(0, 1))

def predict(comstr):
    start = time.time()
    df = pd.read_json(comstr)
    #setting index as date
    df['Date'] = pd.to_datetime(df.index,format='%Y-%m-%d')
    df.index = df['Date']
    #creating dataframe with date and the target variable
    data = df.sort_index(ascending=True, axis=0)
    train=data[:]
    training=train['Close']
    model = ARIMA(training, order=(1,1,0))
    model_fit = model.fit(disp=0)
    result = model_fit.forecast(steps=1)
    end = time.time()
    print("ELASPSED TIME", end - start)
    return str(result)
#    forecast = pd.DataFrame(forecast,index = valid.index,columns=['Prediction'])
