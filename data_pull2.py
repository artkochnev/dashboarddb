from datetime import date
#import streamlit as st
import pandas as pd
import yfinance as yf
import logging
import re

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

link_unhcr_refugees = 'https://data.unhcr.org/population/?widget_id=354106&sv_id=54&population_group=5478'
link_unhcr_key_figures = r"https://proxy.hxlstandard.org/data.csv?tagger-match-all=on&tagger-01-header=total+population%28flash+appeal%29&tagger-01-tag=%23population%2Btotal&tagger-02-header=people+affected%28flash+appeal%29&tagger-02-tag=%23affected%2Btotal&tagger-03-header=people+affected+-+idps&tagger-03-tag=%23affected%2Bidps&tagger-04-header=people+in+need%28flash+appeal%29&tagger-04-tag=%23affected%2Bpin&tagger-05-header=pin+-+idps&tagger-05-tag=%23affected%2Bpin%2Bidps&tagger-06-header=people+targeted%28flash+appeal%29&tagger-06-tag=%23affected%2Bpin%2Bidps&tagger-07-header=people+targeted+-+idps&tagger-07-tag=%23targeted%2Bidps&tagger-11-header=refugees%28unhcr%29&tagger-11-tag=%23affected%2Brefugees&tagger-12-header=civilian+casualities%28unhcr%29+-+killed&tagger-12-tag=%23affected%2Bkilled&tagger-13-header=civilian+casualities%28unhcr%29+-+injured&tagger-13-tag=%23affected%2Binjured&tagger-14-header=date&tagger-14-tag=%23date&tagger-16-header=ukraine+flash+appeal+2022+-+required+%28us%24m%29&tagger-16-tag=%23value%2Bfunding%2Bflash%2Brequired%2Busd&tagger-17-header=ukraine+flash+appeal+2022+-+funded+%28us%24m%29&tagger-17-tag=%23value%2Bfunding%2Bflash%2Bfunded%2Busd&tagger-18-header=ukraine+flash+appeal+2022+-+%25+coverage&tagger-18-tag=%23value%2Bfunding%2Bflash%2Bpct&tagger-19-header=ukraine+humanitarian+response+plan+2022+-+required+%28us%24m%29&tagger-19-tag=%23value%2Bfunding%2Bhrp%2Brequired%2Busd&tagger-20-header=ukraine+humanitarian+response+plan+2022+-+funded+%28us%24m%29&tagger-20-tag=%23value%2Bfunding%2Bhrp%2Bfunded%2Busd&tagger-21-header=ukraine+humanitarian+response+plan+2022+-+%25+coverage&tagger-21-tag=%23value%2Bfunding%2Bhrp%2Bpct&tagger-22-header=ukraine+regional+refugee+response+plan+2022+-+required+%28us%24m%29&tagger-22-tag=%23value%2Bfunding%2Brrrp%2Brequired%2Busd&tagger-23-header=ukraine+regional+refugee+response+plan+2022+-+funded+%28us%24m%29&tagger-23-tag=%23value%2Bfunding%2Brrrp%2Bfunded%2Busd&tagger-24-header=ukraine+regional+refugee+response+plan+2022+-+%25+coverage&tagger-24-tag=%23value%2Bfunding%2Brrrp%2Bpct&tagger-25-header=cerf+-+contributions+%28us%24m%29&tagger-25-tag=%23value%2Bcerf%2Bcontributions&tagger-26-header=cerf+-+allocations+%28us%24m%29&tagger-26-tag=%23value%2Bcerf%2Ballocations&tagger-27-header=ukraine+humanitarian+fund+-+contributions+%28us%24m%29&tagger-27-tag=%23value%2Bfunding%2Buhf%2Bcontributions&tagger-28-header=ukraine+humanitarian+fund+-+allocations+%28us%24m%29&tagger-28-tag=%23value%2Bfunding%2Buhf%2Ballocations&url=https%3A%2F%2Fdocs.google.com%2Fspreadsheets%2Fd%2Fe%2F2PACX-1vQIdedbZz0ehRC0b4fsWiP14R7MdtU1mpmwAkuXUPElSah2AWCURKGALFDuHjvyJUL8vzZAt3R1B5qg%2Fpub%3Foutput%3Dcsv&header-row=2&dest=data_view&_gl=1*15fuvam*_ga*MTEzODI5NDY2My4xNjY3NDAzMjYw*_ga_E60ZNX2F68*MTY2NzQwMzI2MC4xLjEuMTY2NzQwMzQyMi4xNy4wLjA."
link_humdata_grain = r"https://docs.google.com/spreadsheets/d/e/2PACX-1vSmK-9MH9Z3SBLk7Y6a7jzAUmiyfXfSbDEpJWD-ZGxd8mm92bb0qJ5GaVqn4Lw-a-J0-UxbtGaEFtmh/pub?output=csv"
link_humdata_refugees = r"https://docs.google.com/spreadsheets/d/e/2PACX-1vRzvb2ZKLS95aToa_SBYfsZIFhcL_0rvfir5kSUNzl7KNY8UIAVH9AyBZ2I-d5yAZly4l6S15bCVM_d/pub?gid=2043074349&single=true&output=csv"
link_humdata_idps = r"https://docs.google.com/spreadsheets/d/e/2PACX-1vRzvb2ZKLS95aToa_SBYfsZIFhcL_0rvfir5kSUNzl7KNY8UIAVH9AyBZ2I-d5yAZly4l6S15bCVM_d/pub?gid=46569439&single=true&output=csv"
link_humdata_subnational = r"https://docs.google.com/spreadsheets/d/e/2PACX-1vRzvb2ZKLS95aToa_SBYfsZIFhcL_0rvfir5kSUNzl7KNY8UIAVH9AyBZ2I-d5yAZly4l6S15bCVM_d/pub?gid=611324163&single=true&output=csv"
link_humdata_national = r"https://docs.google.com/spreadsheets/d/e/2PACX-1vRzvb2ZKLS95aToa_SBYfsZIFhcL_0rvfir5kSUNzl7KNY8UIAVH9AyBZ2I-d5yAZly4l6S15bCVM_d/pub?gid=0&single=true&output=csv"
link_humdata_attacks_hc = r"https://docs.google.com/spreadsheets/d/e/2PACX-1vTDw_w3n9b0_frBtvJWtZTJGb5Bn72sZsjJSRXLhIxMa6I1ZECFjb1LTsTZ0PmIHiQOw4SEPCO4uIFv/pub?gid=1932484940&single=true&output=csv"
link_zhukov_events = r"https://github.com/zhukovyuri/VIINA/blob/master/Data/events_latest.zip"
link_zhukov_control = r"https://github.com/zhukovyuri/VIINA/blob/master/Data/control_latest.zip"
link_humdata_food_prices = r"https://data.humdata.org/dataset/9b95de1b-d4e9-4c81-b2bb-db35bd9620e8/resource/1730560f-8e9f-4999-bec8-72118ac0ee5f/download/wfp_food_prices_ukr.csv"
link_kiel_assistance = r"https://www.ifw-kiel.de/fileadmin/Dateiverwaltung/Subject_Dossiers_Topics/Ukraine/Ukraine_Support_Tracker/Ukraine_Support_Tracker.xlsx"
link_wb_damage = r"assets/world_bank_reconstruction.xlsx"

data_links = [
    link_unhcr_refugees,
    link_unhcr_key_figures,
    link_humdata_grain,
    link_humdata_refugees,
    link_humdata_idps,
    link_humdata_subnational,
    link_humdata_national,
    link_humdata_attacks_hc,
    link_humdata_food_prices,
    link_wb_damage
]

for d in data_links:
    try:
        df = pd.read_csv(d)
    except Exception as e:
        logging.info("Cannot read as csv, trying as excel", exc_info=True)
        df = pd.read_excel(d)
    finally:
        print(df)

# Data retrieval test
# Financial data
get_yf_data(currency_list, target)