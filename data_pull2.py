from datetime import datetime
#import streamlit as st
import zipfile
from urllib.request import urlopen
import pandas as pd
import numpy as np
import yfinance as yf
import logging
import re
import ssl
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

# --- YAHOO FINANCE
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

# --- MANUAL DATA
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
            df_return.to_csv(f'{target_folder}/src_{dfunction}.csv', index=False)      
            print(f"Data for {dfunction} retrieved at {current_time}") 

# --- UNLOCK FOR PRODUCTION
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 150)

# --- TEST FUNCTIONS
def log_data_transform():
    now = datetime.now()
    current_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    logging.info(f'Grain data stored: {current_time}')

def read_data(source, source_type):
    df = pd.DataFrame()
    if source_type == 'csv':
        df = pd.read_csv(f'assets/{source}')
    elif source_type == 'xlsx':
        df = pd.read_excel(source)
    else:
        pass
    print(df)
    return df

# --- GRAIN FUNCTIONS
def transform_grain_data(source, output='assets/tf_grain_data.csv'):
    df = pd.read_csv(f'assets/{source}', thousands=r',')
    df['Income group'] = df['Income group'].fillna('mixed')
    df = df.groupby(['Country', 'Income group']).sum('total metric tons')
    df = df.sort_values(by=['total metric tons'], ascending=False)
    df = df.reset_index()
    df.columns = ['Country', 'Income group', 'Tons received']
    df.to_csv(output)
    log_data_transform()

def plot_grain(source):
    df = pd.read_csv(f'assets/{source}')
    fig = px.bar(df, x = 'Tons received', y='Income group', color = 'Country', orientation='h',
        hover_data={'Tons received': ':.0f'},
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    return fig

# --- HUMANITARIAN DATA
def transform_hum_data(source, output='assets/tf_hum_data.csv'):
    df = pd.read_csv(f'assets/{source}')
    df = df[df.iloc[:, 0] != '#population+total']
    df = df[['People Affected(Flash Appeal)', 'IDPs', 'Refugees(UNHCR)', 'Civilian casualities(OHCHR) - Killed', 'Civilian casualities(OHCHR) - Injured', 'Attacks on Education Facilities', 'Attacks on Health Care', 'Date']]
    df.columns = ['People affected', 'Internally Displaced', 'Refugees', 'Civilian deaths, confirmed', 'Civilians injured, confirmed', 'Attacks on Education Facilities', 'Attacks on Health Care', 'Date']
    df = df.fillna(method='ffill')
    df.to_csv(output)
    log_data_transform()

def plot_refugees(source):
    df = pd.read_csv(f'assets/{source}')
    fig = px.area(df, y = 'Refugees', x = 'Date')
    return fig

def plot_idps(source):
    df = pd.read_csv(f'assets/{source}')
    fig = px.area(df, y = 'Internally Displaced', x = 'Date')
    return fig

def plot_deaths(source):
    df = pd.read_csv(f'assets/{source}')
    fig = px.area(df, y = 'Civilian deaths, confirmed', x = 'Date')
    return fig

def plot_casualties(source):
    df = pd.read_csv(f'assets/{source}')
    fig = px.area(df, y = 'Civilians injured, confirmed', x = 'Date')
    return fig

# --- RECONSTRUCTION & DAMAGE & REGIONS
def transform_reconstruction_regions(source, output='assets/tf_reconstruction_regions.csv'):
    df = pd.read_csv(f'assets/{source}')
    df = df[df['Oblast'].isin(['Support regions, subtotal','Backline regions, subtotal','Regions where government has regained control, subtotal'])!=True]
    df.to_csv(output)
    log_data_transform()

def plot_damage(source):
    df = pd.read_csv(f'assets/{source}.csv')
    fig = px.treemap(df, path=[px.Constant("All"), 'Sector Type', 'Sector'], values='Damage',
        color_discrete_sequence=px.colors.qualitative.Pastel,
        title="Damage assessment as of August 2022")
    return fig

def plot_needs(source):
    df = pd.read_csv(f'assets/{source}.csv')
    fig = px.treemap(df, path=[px.Constant("All"), 'Sector Type', 'Sector'], values='Needs',
        color_discrete_sequence=px.colors.qualitative.Pastel,
        title="Reconstruction needs as of August 2022")
    return fig

def plot_regional_damage(source):
    df = pd.read_csv(f'assets/{source}')
    fig = px.bar(df, x = 'Damage', y='Oblast', orientation='h', color = 'Oblast type',
        hover_data={'Damage': ':.1f'},
        color_discrete_sequence=px.colors.qualitative.Pastel,
        title="Damage by regions as of August 2022"
    )
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    return fig

# --- UKRAINE SUPPORT
def transform_support_data(source, output='assets/tf_ukraine_support.csv'):
    df = pd.read_csv(f'assets/{source}')
    df = df[['countries',	
        'Announcement Date',	
        'Type of Aid General',
        'Value committed (own estimate, in USD)',	
        'Value delivered (own estimate, in USD)',	
        'Converted Value in EUR',
        'Total monetary value delivered in EUR']]
    df = df.replace('.', np.nan)
    df['Value committed'] = df['Converted Value in EUR']
    df.loc[df['Value committed'].isna() == True, 'Value committed'] = df['Value committed (own estimate, in USD)']
    df['Value delivered'] = df['Total monetary value delivered in EUR']
    df.loc[df['Value delivered'].isna() == True, 'Value delivered'] = df['Value delivered (own estimate, in USD)']
    df.loc[df['Value delivered'].isna() == True, 'Value delivered'] = 0
    df = df[(df['Value committed'] != 'No price')]
    df = df[(df['Value delivered'] != 'No price')]
    df['Value committed'] = df['Value committed'].astype(float) / 10**9 #bn USD
    df['Value delivered'] = df['Value delivered'].astype(float) / 10**9 #bn USD
    df = df.groupby(['countries', 'Type of Aid General']).agg({'Value committed':'sum','Value delivered':'sum'})
    df['Ratio: Delivered to committed'] = df['Value delivered']/df['Value committed']
    df = df.reset_index()
    df.to_csv(output)
    log_data_transform()

def plot_support_committed(source):
    df = pd.read_csv(f'assets/{source}')
    fig = px.treemap(df, path=[px.Constant("All"), 'Type of Aid General', 'countries'], values='Value committed',
                hover_data={'Value committed': ':.2f'},
                color_discrete_sequence=px.colors.qualitative.Pastel,
            )
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    return fig

def plot_support_delivered(source):
    df = pd.read_csv(f'assets/{source}')
    fig = px.treemap(df, path=[px.Constant("All"), 'Type of Aid General', 'countries'], values='Value delievered',
                hover_data={'Value delivered': ':.2f'},
                color_discrete_sequence=px.colors.qualitative.Pastel,
            )
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    return fig

def plot_delivery_rate(source):
    df = pd.read_csv(f'assets/{source}')
    df = df.groupby(['countries']).agg({'Value committed': 'sum', 'Value delivered': 'sum'}).reset_index()
    df['Ratio: Delivered to committed'] = df['Value delivered'] / df['Value committed']
    fig = px.bar(df, y="countries", 
                    x="Value committed",
                    color='Ratio: Delivered to committed', 
                    orientation='h', 
                    text_auto='.2s',
                    hover_data={'Ratio: Delivered to committed': ':.1f'},
                    color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    return fig

# --- FISCAL AND FINANCIAL DATA
def transform_fiscal_income(source, output='assets/tf_fiscal_income.csv'):
    df = pd.read_csv(f'assets/{source}')
    df = df.reset_index()
    df.to_csv(output)
    log_data_transform()

def transform_fiscal_expenses(source, output='assets/tf_fiscal_expenses.csv'):
    df = pd.read_csv(f'assets/{source}')
    df = df.reset_index()
    df.to_csv(output)
    log_data_transform()

def transform_fiscal_finance(source, output='assets/tf_fiscal_finance.csv'):
    df = pd.read_csv(f'assets/{source}')
    df = df.reset_index()
    df.to_csv(output)
    log_data_transform()

def transform_cpi_headline(source, output='assets/tf_cpi_headline.csv'):
    df = pd.read_csv(f'assets/{source}')
    df = df.reset_index()
    df.to_csv(output)
    log_data_transform()

def transform_international_reserves(source, output='assets/tf_international_reserves.csv'):
    df = pd.read_csv(f'assets/{source}')
    df = df.reset_index()
    df.to_csv(output)
    log_data_transform()

def transform_bond_yields(source, output='assets/tf_bond_yields.csv'):
    df = pd.read_csv(f'assets/{source}')
    df = df.reset_index()
    df.to_csv(output)
    log_data_transform()

def transform_policy_rate(source, output='assets/tf_policy_rate.csv'):
    df = pd.read_csv(f'assets/{source}')
    df = df.reset_index()
    df.to_csv(output)
    log_data_transform()

def transform_interest_rates(source, output='assets/tf_interest_rates.csv'):
    df = pd.read_csv(f'assets/{source}')
    df = df.reset_index()
    df.to_csv(output)
    log_data_transform()

def transform_financial_soundness(source, output='assets/tf_financial_soundness.csv'):
    df = pd.read_csv(f'assets/{source}')
    df = df.reset_index()
    df.to_csv(output)
    log_data_transform()

# --- FUNCTIONAL TEST ---
# Data retrieval
get_ua_data(link_data_sources, target_folder='assets')

# Data transform
# transform_hum_data('src_hum_data.csv')
# transform_grain_data('src_grain_destinations.csv')
# transform_reconstruction_regions('src_reconstruction_regions.csv')
# transform_support_data('src_ukraine_support.csv')

# plot_refugees('tf_hum_data.csv').show()
# plot_idps('tf_hum_data.csv').show()
# plot_deaths('tf_hum_data.csv').show()
# plot_casualties('tf_hum_data.csv').show()
# plot_damage('src_reconstruction_sectors').show()
# plot_needs('src_reconstruction_sectors').show()
# plot_regional_damage('tf_reconstruction_regions.csv').show()
# plot_delivery_rate('tf_ukraine_support.csv').show()

# Data retrieval test
# Financial data
# get_yf_data(currency_list, target)

# ToDos
# Refugee Plot: cut data before August (later correct for inconsistency)
# IDP: OK, although bar chart might be more useful
# Casualties: OK, might add a secondary with the Mariupol estimations
# Civilians injured: as above, might add a correction for Mariupol
# Damage: also good
# Needs: very good
# Regional damage good
# Delivery rate: ratio delivered to committed: change to %
# Add sources everywhere
# Another idea: Commitment to GDP