#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 11:41:21 2023

@author: glenn
"""

import yfinance as yf

tickers = ["MSFT","AAPL","GOOG"]
ohlcv_data = {}

for ticker in tickers:
    temp = yf.download(ticker,period='1mo',interval='15m')
    temp.dropna(how="any",inplace=True)
    ohlcv_data[ticker] = temp
    
def MACD(dataFrame, fastMovingDuration, slowMovingDuration, macDDuration):
    df = dataFrame.copy()
    df["ma_fast"] = df["Adj Close"].ewm(span=fastMovingDuration, min_periods=fastMovingDuration).mean()
    df["ma_slow"] = df["Adj Close"].ewm(span=slowMovingDuration, min_periods=slowMovingDuration).mean()
    df["macd"] = df["ma_fast"] - df["ma_slow"]
    df["signal"] = df["macd"].ewm(span=macDDuration, min_periods=macDDuration).mean()
    return df.loc[:,["macd","signal"]]

for ticker in ohlcv_data:
    ohlcv_data[ticker][["MACD","SIGNAL"]] = MACD(ohlcv_data[ticker], 12 ,26, 9)
