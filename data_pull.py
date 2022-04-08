from datetime import date
import streamlit as st
import pandas as pd
import investpy as ipy
import plotly.express as px
import plotly.graph_objects as go
import pydeck as pdk
import logging
import re

@st.cache
def get_text(link_text=str, label_col = 'label', paragraph_col = 'paragraph', label_val = str):
    df = pd.read_excel(link_text)
    texts = df.loc[df[label_col]==label_val]
    texts = texts[paragraph_col].to_list()
    texts_len = len(texts)

    if texts_len > 1:
        logging.info(f"Multiple matches in DataFrame {df} for label {label_col}. Returning the first value")

    try:
        text = texts[0]
    except Exception as e:
        logging.info(f"No text found in DataFrame {df} for label {label_col}")
        text = ""
    return text


# FUNCTIONS
def strip_ipy_df(df = pd.DataFrame(), instrument = str, rename = False):
    df = df[['Close']]
    df['instrument'] = instrument
    if rename == True:
        df = df.rename(columns={"Close": instrument})
    return df

def get_fx(fx, start_date=date, to_date=date, link_local = str):
    try:
        df = ipy.get_currency_cross_historical_data(currency_cross=fx, 
                                                    from_date=start_date, 
                                                    to_date=to_date)
        df = strip_ipy_df(df, fx)
        return df
    except Exception as e:
        logging.warning("Unable to retrieve the currency pair {fx}", exc_info=True)            

def get_commodity(commodity, start_date=date, to_date=date, market='United Kingdom', link_local = str):
    try:
        df = ipy.commodities.get_commodity_historical_data(commodity=commodity, 
                                                            from_date=start_date, 
                                                            to_date=to_date,
                                                            country=market)
        df = strip_ipy_df(df, commodity)
        return df
    except Exception as e:
        logging.warning("Unable to retrieve prices for commodity {commodity}", exc_info=True)

def get_bond(country=str, tenor = 10, start_date=date, to_date=date, link_local = str):
    try:
        country_bond_name = str(country) + " " + str(tenor) + "Y"
        df = ipy.bonds.get_bond_historical_data(bond=country_bond_name,
                                                from_date=start_date,
                                                to_date=to_date)
        df = strip_ipy_df(df, country)
        return df
    except Exception as e:
        logging.warning("Unable to retrieve bonds for country {country}", exc_info=True)


def get_spread(country_bond = str, bench_bond = "Germany", start_date=date, to_date=date, tenor = 10):
    df_country_bond = get_bond(country=country_bond, tenor = tenor, start_date=start_date, to_date=to_date)
    df_bench_bond = get_bond(country=bench_bond, tenor = tenor, start_date=start_date, to_date=to_date)
    spread_name = str(country_bond) + " vs " + str(bench_bond) + ": " + str(tenor) + "Y"
    df = pd.merge(df_country_bond, df_bench_bond, left_index=True, right_index=True)
    df['Close'] = df['Close_x'] - df['Close_y']
    df = strip_ipy_df(df, spread_name)
    return df

@st.cache
def get_data(bonds = list, 
            fxs = list, 
            commodities = list, 
            spreads = list, 
            tenor_bonds = 10, 
            tenor_spreads = 10, 
            bench_bond = "Germany",
            market = "United Kingdom",
            start_date = date, 
            to_date = date):
    
    df = pd.DataFrame()    
        
    for bond in bonds:
        df = df.append(get_bond(bond, tenor=tenor_bonds, start_date=start_date, to_date=to_date))

    for fx in fxs:
        df = df.append(get_fx(fx, start_date=start_date, to_date=to_date))

    for commodity in commodities:
        df = df.append(get_commodity(commodity, start_date=start_date, to_date=to_date, market=market))

    for spread in spreads:
        df = df.append(get_spread(country_bond=spread, bench_bond=bench_bond, tenor = tenor_spreads, start_date=start_date, to_date=to_date))

    return df

def get_key(df = pd.DataFrame(), key=str, start_date = date, to_date = date, bench_date = date):
    try:
        df = df.loc[df['instrument'] == key]
        df = df[["Close"]]
        df = df.rename(columns={"Close": key})
        min = df[key].min()
        max = df[key].max()
        sd = df[key].std()
        pre_crisis = df[key][bench_date]
        last = df[key][len(df)-1]
        lvl_delta = round(last - pre_crisis, 2)
        pct_delta = "{:.0%}".format(round(lvl_delta/pre_crisis, 2))
        output = {'data': df, 'last': last, 'lvl_delta': lvl_delta, 'pct_delta': pct_delta, 'min': min, 'max': max, 'sd': sd}
        return output
    except Exception as e:
        logging.warning(f"Unable to retrieve key {key} from df {df}", exc_info=True)

@st.cache
def get_cbr_forecasts(link_local = str, link=str):
    df = pd.DataFrame()
    try:
        df = pd.read_excel(link_local, skiprows=4, usecols='C:J')
    except Exception as e:
        logging.warning(f'Cannot read the CBR data from {link}', exc_info=True)
        #df.to_excel(link_local)
    finally:
        col_names = df.columns
        new_col_names = ['Stat', 'Year']
        for name in col_names:
            check = bool(re.search("Unnamed", name))
            if check != True:
                new_name = name.replace("\n", " ")
                new_name = re.sub('\s+',' ', new_name)
                new_col_names.append(new_name)

        df.columns = new_col_names
        df = df.fillna(method='ffill')
        return df

@st.cache
def get_refugees(link=str, link_local=str):
    df = pd.DataFrame()
    try:
        df = pd.read_json(link)
        df = pd.json_normalize(df['data'])
        df.to_excel(link_local)
    except:
        logging.warning(f'Cannot retrieve UNHCR data from {link}', exc_info=True)
        df = pd.read_excel(link_local)
    finally:
        df = df[['geomaster_name', 'individuals']]
        df['individuals'] = pd.to_numeric(df['individuals'])
        df = df.sort_values(by='individuals', ascending=True)
        total_refugees = df['individuals'].sum()
        output = {'data': df, 'total': total_refugees}
        return output

@st.cache
def get_reg_idps(link_regdata=str, link_local=str):
    df = pd.DataFrame()
    try:
        df = pd.read_excel(link_regdata, sheet_name = "Dataset")
        df.to_excel(link_local)
    except Exception as e:
        logging.warning("Unable to retrieve IDP data from {link_survey} or {link_regdata}", exc_info=True)
        df = pd.read_excel(link_local)
    finally:
        num_cols = ['X Longitude', 'Y Latitude', 'IDP estimation', 'Population']
        for c in num_cols:
            df[c] = pd.to_numeric(df[c])
        df = df.groupby(['admin1Name_eng']).sum()
        df = df.sort_values(by='IDP estimation', ascending=True)
        df['IDP share'] = df['IDP estimation'] / df['IDP estimation'].sum()
        df = df[num_cols]
        df.columns = ['long', 'lat', 'idp', 'population']
        output = {'data': df}
        return output

@st.cache
def get_survey_idps(link_survey=str, link_local=str):
    df = pd.DataFrame()
    try:
        df = pd.read_excel(link_survey, sheet_name="Current location of IDPs", skiprows=1, usecols="A:C")
        df.to_excel(link_local)
    except Exception as e:
        logging.warning("Unable to retrieve UNHCR data on casualties from {link}", exc_info=True)
        df = pd.read_excel(link_local)
    finally:
        df = df.dropna()
        df = df.sort_values(by='# est. IDPs presence per macro-region', ascending=True)
        idps = df['# est. IDPs presence per macro-region'].sum()
        output = {'data': df, 'total': idps}
    return output

@st.cache
def get_casualties(link=str, local_link=str):
    try:
        df = pd.read_csv(link, skiprows=1)
        df.to_excel(local_link)
    except Exception as e:
        logging.warning("Unable to retrieve UNHCR data on casualties from {link}", exc_info=True)
        df = pd.read_excel(local_link)
    finally:
        num_columns = ['Date', 
                    'Civilian casualities(OHCHR) - Killed', 
                    'Civilian casualities(OHCHR) - Injured', 
                    'Refugees(UNHCR)', 'Attacks on Education Facilities', 
                    'Attacks on Health Care']
        df = df[num_columns]
        df = df.fillna(method='bfill', axis=0)
        df = df.fillna(method='ffill', axis=0)
        for col in num_columns:
            if col != 'Date':
                df[col] = pd.to_numeric(df[col])
            else:
                df[col] = pd.to_datetime(df[col])
        n = len(df)-1
        last_killed = df['Civilian casualities(OHCHR) - Killed'][n]
        last_injured = df['Civilian casualities(OHCHR) - Injured'][n]
        last_refugees = df['Refugees(UNHCR)'][n] 
        last_attacks_education = df['Attacks on Education Facilities'][n]
        last_attacks_healthcare = df['Attacks on Health Care'][n]  
        delta_killed = df['Civilian casualities(OHCHR) - Killed'][n] - df['Civilian casualities(OHCHR) - Killed'][n-1]
        delta_injured = df['Civilian casualities(OHCHR) - Injured'][n] - df['Civilian casualities(OHCHR) - Injured'][n-1]
        delta_refugees = round((df['Refugees(UNHCR)'][n] - df['Refugees(UNHCR)'][n-2])/10**6,1)
        delta_attacks_education = int(df['Attacks on Education Facilities'][n]) - int(df['Attacks on Education Facilities'][n-1])
        delta_attacks_healthcare = int(df['Attacks on Health Care'][n]) - int(df['Attacks on Health Care'][n-1])
        output = {'df': df, 
                "Injured": int(last_injured), 
                'Killed': int(last_killed), 
                'Refugees': int(last_refugees),
                'Attacks Schools': int(last_attacks_education),
                'Attacks Healthcare': int(last_attacks_healthcare), 
                'Delta injured': int(delta_injured), 
                'Delta killed': int(delta_killed), 
                'Delta refugees': int(delta_refugees),
                'Delta attacks schools': int(delta_attacks_education),
                'Delta attacks healthcare': int(delta_attacks_healthcare)
                }
        return output

@st.cache
def get_fts_needs(link=str, local_link=str):
    try:
        df = pd.read_csv(link)
        df.to_excel(local_link)
    except Exception as e:
        logging.warning("Unable to retrieve UNHCR data on casualties from {link}", exc_info=True)
        df = pd.read_excel(local_link)
    finally:        
        df = df.loc[(df['code'] == 'FUKR22') & (df['countryCode'] == 'UKR')]
        df = df[(df['requirements'].isnull() == False) | ((df['requirements'].isnull() == True) & (df['cluster'].isin(['Not specified', 'Multiple clusters/sectors (shared)']) == True))]
        df['requirements'] = pd.to_numeric(df['requirements'], errors='coerce')
        df['funding'] = pd.to_numeric(df['funding'], errors='coerce')
        df = df.sort_values(['requirements'], ascending=False)
        funded_needs = df['funding'].sum()
        total_needs = df['requirements'].sum()
        ratio_funded_total = funded_needs / total_needs
        ratio_funded_total = "{:.0%}".format(ratio_funded_total)
        funded_needs = round(funded_needs/10**9, 2)
        total_needs = round(total_needs/10**9, 2)
        output = {'df': df, 'Funded': funded_needs, 'Total': total_needs, 'Requirements met': ratio_funded_total}
        return output

def main():
    pass

if __name__ == '__main__':
    main()