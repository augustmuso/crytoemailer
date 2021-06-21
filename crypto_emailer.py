# -*- coding: utf-8 -*-
"""crypto emailer.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YOtKOH9EVYVT2kFZqiDss1D5URDB9_ff
"""

# !pip install pyportfolioopt
# !pip install bta-lib
# !pip install -U plotly
# !pip install python-binance==0.7.9
# !pip install chart_studio

# import talib as ta
import os
import pandas as pd
import numpy as np
import btalib as ba
import time as T
from binance.client import Client
from datetime import datetime
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException
from decimal import Decimal

# api key and the api secret

api_key='t4tXtY28ugkytdFlSKKHaRzt2IQtfe0jkujOpA0Yyt9QM9z4atPW1SS9LUz6qHtl'
api_secret='p7plNd2xy1H899B7ckCfxBUZ5xI2OtmUXnA5QzGmd26gVBJxDuS21PP67Ouf0DUe'

# puting key and secret into client

client = Client(api_key, api_secret)

# create a class containing my coins and a dictionary containg the instances:
class coin(object):
    def __init__(self, ticker, time_interval):
        self.ticker = ticker
        self.time_interval = time_interval
        self.direction = None

    def madebefore(self, from_date):
        # return if from_date is greater(more current) than coinbirth
        coinbirth = client._get_earliest_valid_timestamp(self.ticker, self.time_interval)
        coinbirth = datetime.fromtimestamp(coinbirth/1000)
        return from_date > coinbirth, 'you want data from ' + str(from_date.date()) +' and coin made in ' + str(coinbirth.date())


    def coindata(self, from_date, CciPeriod):
        df = pd.DataFrame()

        bars = np.array(client.get_historical_klines(self.ticker, interval = self.time_interval,  start_str = str(from_date)))
        

        if (self.madebefore(from_date)[0]) & (np.size(bars) > 100):
            
            bars = np.delete(bars,np.s_[5:],1)
            columns=['date', 'open', 'high', 'low', 'close']

            df = pd.DataFrame(bars, columns = columns)
            df.set_index('date', inplace=True)
            df = df.apply(pd.to_numeric)
            df.index = pd.to_datetime(df.index, unit='ms')
            
            df['cci'] = ba.cci(df.high, df.low, df.close, period= CciPeriod).df 
        

        return df
        
    def currentprice(self):
        # gets current price and converts it to float
        return float(client.get_symbol_ticker(symbol=self.ticker)['price'])
    


symbols = ['BNBUSDT', 'BCCUSDT', 'NEOUSDT', 'LTCUSDT', 'QTUMUSDT', 'ADAUSDT', 'XRPUSDT', 'EOSUSDT', 'TUSDUSDT', 'IOTAUSDT',
           'XLMUSDT', 'ONTUSDT', 'TRXUSDT', 'ETCUSDT', 'ICXUSDT', 'VENUSDT', 'NULSUSDT', 'VETUSDT','BCHABCUSDT', 'BCHSVUSDT',
           'LINKUSDT', 'WAVESUSDT', 'BTTUSDT', 'ONGUSDT', 'HOTUSDT', 'ZILUSDT', 'ZRXUSDT', 'FETUSDT', 'BATUSDT', 
           'XMRUSDT', 'ZECUSDT', 'IOSTUSDT', 'CELRUSDT', 'DASHUSDT', 'NANOUSDT', 'OMGUSDT', 'THETAUSDT', 'ENJUSDT', 'MITHUSDT',
           'MATICUSDT', 'ATOMUSDT', 'TFUELUSDT', 'ONEUSDT', 'FTMUSDT', 'ALGOUSDT', 'USDSBUSDT', 'GTOUSDT', 'ERDUSDT', 
           'DOGEUSDT', 'DUSKUSDT', 'ANKRUSDT', 'WINUSDT', 'COSUSDT', 'NPXSUSDT', 'COCOSUSDT', 'MTLUSDT', 'TOMOUSDT', 'PERLUSDT',
           'DENTUSDT', 'MFTUSDT', 'KEYUSDT', 'STORMUSDT', 'DOCKUSDT', 'WANUSDT', 'FUNUSDT', 'CVCUSDT', 'CHZUSDT', 'BANDUSDT',
           'BEAMUSDT', 'XTZUSDT', 'RENUSDT', 'RVNUSDT', 'HCUSDT', 'HBARUSDT', 'NKNUSDT', 'STXUSDT', 'KAVAUSDT', 'ARPAUSDT',
           'IOTXUSDT', 'RLCUSDT', 'MCOUSDT', 'CTXCUSDT', 'BCHUSDT', 'TROYUSDT', 'VITEUSDT', 'FTTUSDT', 'BUSDTRY', 'OGNUSDT',
           'DREPUSDT', 'BULLUSDT', 'BEARUSDT',  'TCTUSDT', 'WRXUSDT', 'BTSUSDT', 'LSKUSDT', 'BNTUSDT', 'LTOUSDT', 
           'AIONUSDT', 'MBLUSDT', 'COTIUSDT',  'STPTUSDT', 'USDTZAR', 'WTCUSDT', 'DATAUSDT', 'XZCUSDT', 'SOLUSDT', 'USDTIDRT', 
           'CTSIUSDT', 'HIVEUSDT',  'GXSUSDT', 'ARDRUSDT', 'MDTUSDT', 'STMXUSDT', 'KNCUSDT', 'REPUSDT', 'LRCUSDT',
           'PNTUSDT', 'COMPUSDT',  'BKRWUSDT', 'SCUSDT', 'ZENUSDT', 'SNXUSDT', 'VTHOUSDT', 'DGBUSDT', 'SXPUSDT', 'MKRUSDT', 
           'DAIUSDT', 'DCRUSDT', 'STORJUSDT', 'USDTBKRW', 'MANAUSDT', 'YFIUSDT', 'BALUSDT', 'BLZUSDT','IRISUSDT', 'KMDUSDT',
           'JSTUSDT', 'SRMUSDT', 'ANTUSDT', 'CRVUSDT', 'SANDUSDT', 'OCEANUSDT', 'NMRUSDT', 'DOTUSDT', 'LUNAUSDT', 'RSRUSDT',
           'WNXMUSDT', 'TRBUSDT', 'BZRXUSDT', 'SUSHIUSDT', 'YFIIUSDT', 'KSMUSDT', 'EGLDUSDT', 'RUNEUSDT', 'FIOUSDT', 'UMAUSDT', 
           'USDTNGN', 'BELUSDT', 'WINGUSDT', 'UNIUSDT', 'NBSUSDT', 'OXTUSDT', 'SUNUSDT', 'AVAXUSDT', 'HNTUSDT', 'FLMUSDT', 
           'ORNUSDT', 'UTKUSDT', 'XVSUSDT', 'ALPHAUSDT', 'USDTBRL', 'AAVEUSDT', 'NEARUSDT', 'FILUSDT', 'INJUSDT', 'AUDIOUSDT',
           'CTKUSDT', 'AKROUSDT', 'AXSUSDT', 'HARDUSDT', 'DNTUSDT', 'STRAXUSDT', 'UNFIUSDT', 'ROSEUSDT', 'AVAUSDT', 'XEMUSDT', 
           'SKLUSDT', 'SUSDUSDT', 'GRTUSDT', 'JUVUSDT', 'PSGUSDT', '1INCHUSDT', 'REEFUSDT', 'OGUSDT', 'ATMUSDT', 'ASRUSDT',
           'CELOUSDT', 'RIFUSDT', 'BTCSTUSDT', 'TRUUSDT', 'CKBUSDT', 'TWTUSDT', 'FIROUSDT', 'LITUSDT', 'SFPUSDT', 'DODOUSDT',
           'CAKEUSDT', 'ACMUSDT', 'BADGERUSDT', 'FISUSDT', 'OMUSDT', 'PONDUSDT', 'DEGOUSDT', 'ALICEUSDT', 'LINAUSDT','PERPUSDT',
           'RAMPUSDT', 'SUPERUSDT', 'CFXUSDT', 'EPSUSDT', 'AUTOUSDT', 'TKOUSDT', 'PUNDIXUSDT', 'TLMUSDT', 'BTGUSDT', 'MIRUSDT',
           'BARUSDT', 'FORTHUSDT', 'BAKEUSDT', 'BURGERUSDT', 'SLPUSDT','SHIBUSDT', 'ICPUSDT', 'USDTGYEN', 'ARUSDT', 'POLSUSDT',
           'MDXUSDT', 'MASKUSDT', 'LPTUSDT', 'NUUSDT']

# create a dictionary of the files(instance) of each coin in the universe
symbolclass = {}
for c in symbols:
    symbolclass[c] = coin(c, '4h')

# pick a start date( %yyyy%mm%dd)
start = datetime(2021, 3, 1, 0, 0)

# function to pick form the universe of coins 
def select(from_date):
  # current price of every coin is between 0.05 and 1.5 and was made before the selected date
    cheapcoins = [c for c in symbolclass if 0.05 < symbolclass[c].currentprice() < 1.5 and symbolclass[c].madebefore(from_date)[0]]

    # get close price of the cheapcoins into the same data frame
    df = pd.DataFrame()
    for i in set(cheapcoins):

        symboldf = symbolclass[i].coindata(from_date, 100)
        if not symboldf.empty:

            #  getting only the close 
            df[i] = symboldf['close']

            bef_2 = symboldf['cci'].shift(2).fillna(0).astype(int)
            bef_1 = symboldf['cci'].shift(1).fillna(0).astype(int)
            now =  symboldf['cci'].fillna(0).astype(int)

            conditions = [
                    ((bef_1 > 0) & (bef_2 < 0) & (now  > bef_1)),
                    ((bef_1 < 0) & (bef_2 > 0) & (now  < bef_1))
            ]

            choices = ['BUY','SELL']

            symboldf['direction'] = np.select(conditions, choices, default = 'FLAT')

            symbolclass[i].direction = symboldf['direction'].iloc[-1]

    nowtime = df.index[-1]

    topgainers = df.pct_change().iloc[-1].sort_values(ascending = False).head(5) # gets coins with highest per% change in close price

    toplosers = df.pct_change().iloc[-1].sort_values(ascending = False).tail(5) # gets coins with lowest per% change in close price

    ccibuys = [c for c in symbolclass if symbolclass[c].direction == 'BUY'] # gets coins with buy direction

    ccisells = [c for c in symbolclass if symbolclass[c].direction == 'SELL'] # gets coins with sell direction



    return topgainers, toplosers, ccibuys, ccisells, nowtime


def messagemaker(func):
    topgainers, toplosers, ccibuys, ccisells, nowtime = func
    message = \
    '''
    Date: {:%a, %b %d %Y %I:%M %p}

    This are the top gainers:-
    {}: +{}%
    {}: +{}%
    {}: +{}%
    {}: +{}%
    {}: +{}%

    This are the top loser:-
    {}: {}%
    {}: {}%
    {}: {}%
    {}: {}%
    {}: {}%

    These coins have gained momentum :-
    {}

    These coins have lost momentum :-
    {}
      
    '''.format(# date
              nowtime,\

                # gainers
                topgainers.index[0],np.round(topgainers[topgainers.index[0]] * 100, 2),\
              topgainers.index[1],np.round(topgainers[topgainers.index[1]] * 100, 2),\
              topgainers.index[2],np.round(topgainers[topgainers.index[2]] * 100, 2),\
              topgainers.index[3],np.round(topgainers[topgainers.index[3]] * 100, 2),\
              topgainers.index[4],np.round(topgainers[topgainers.index[4]] * 100, 2),\

                # losers
              toplosers.index[4],np.round(toplosers[toplosers.index[4]] * 100, 2),\
              toplosers.index[3],np.round(toplosers[toplosers.index[3]] * 100, 2),\
              toplosers.index[2],np.round(toplosers[toplosers.index[2]] * 100, 2),\
              toplosers.index[1],np.round(toplosers[toplosers.index[1]] * 100, 2),\
              toplosers.index[0],np.round(toplosers[toplosers.index[0]] * 100, 2),\
              
              # momentum gainers
              ccibuys,\

              # momentum losers
              ccisells)
    return message
