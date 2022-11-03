from datetime import datetime
#import streamlit as st
import zipfile
from urllib.request import urlopen
import io
import pandas as pd
import yfinance as yf
import logging
import re
import ssl
import requests
import plotly.express as px

# SSL Error fix for IFW Kiel
ssl._create_default_https_context = ssl._create_unverified_context

link_data_sources ='assets/data_sources.xlsx'
instrument = "UAH=X"
start_date = "2021-01-12"
end_date = "2022-11-02"
target = "yf_data.csv"
alias = "UAH/USD"
currency_list = {
    'code': ['UAH=X', 'RUB=X'],
    'label': ['UAH/USD', 'RUB/USD'],
    'type': ['FX rate', 'FX rate']
}

# Yahoo Finance data
def get_yf_instrument(instrument, alias, type, start_date, end_date):
    try:
        df = yf.download(instrument, start=start_date, end=end_date)
        df = df[["Adj Close"]]
        df["date"] = df.index
        if alias is None:
            df["instrument"] = instrument
        else:    
            df["instrument"] = alias
        df["type"] = type
        df["value"] = df["Adj Close"]
        df = df[["date", "type", "instrument", "value"]]
        return df
    except Exception as e:
        logging.warning("Unable to retrieve the currency pair {fx}", exc_info=True)   

def get_yf_data(currency_list, target):
    length = len(currency_list['code'])
    df = pd.DataFrame()
    for c in range(0,length):
        df_temp = get_yf_instrument(currency_list['code'][c], currency_list['label'][c], currency_list['type'][c], start_date, end_date)
        print(df_temp)
        df = df.append(df_temp)   
    df.to_csv(target, index=False)

def get_ua_data(link_data_sources, target_folder):
    # Parse list of data sources
    df = pd.read_excel(link_data_sources)
    #  Parse and store the files
    for ind in df.index:
        dactive = df['active'][ind]   
        if dactive == 1:
            dext = df['extension'][ind]
            dlink = df['link'][ind]
            dsheet = str(df['sheet'][ind])
            dskip = df['row skip'][ind]
            dfunction = df['function'][ind]
            if dext == 'csv':
                df_return = pd.read_csv(dlink)
            elif dext == 'xlsx':
                df_return = pd.read_excel(dlink, sheet_name=dsheet)
            elif dext == 'zip':
                df_return = pd.read_csv(dlink, compression='zip')
            else:
                pass
            if dskip > 0:
                df_return = df_return.iloc[dskip: , :]
            now = datetime.now()
            current_time = now.strftime("%m/%d/%Y, %H:%M:%S")
            df_return['retrieved'] = current_time
            df_return.to_csv(f'{target_folder}/{dfunction}.csv', index=False)      
            print(f"Data for {dfunction} retrieved at {current_time}") 

# --- UNLOCK FOR PRODUCTION ---
# get_ua_data(link_data_sources, target_folder='assets')
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 150)

# --- GRAIN FUNCTIONS ---
def get_grain_data(source):
    df = pd.read_csv('assets/grain_destinations.csv', thousands=r',')
    df['Income group'] = df['Income group'].fillna('mixed')
    df = df.groupby(['Country', 'Income group']).sum('total metric tons')
    df = df.sort_values(by=['total metric tons'], ascending=False)
    df = df.reset_index()
    df.columns = ['Country', 'Income group', 'Tons received']
    return df

def plot_grain(df):
    fig = px.bar(df, x = 'Tons received', y='Income group', color = 'Country', orientation='h',
        hover_data={'Tons received': ':.0f'},
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    return fig

# --- FUNCTIONAL TEST ---

df_grain = get_grain_data('assets/grain_destinations.csv')
fig_grain = plot_grain(df_grain)
fig_grain.show()

# Data retrieval test
# Financial data
# get_yf_data(currency_list, target)