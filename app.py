from datetime import date
import streamlit as st
import pandas as pd
import investpy as ipy
import plotly.express as px
import streamlit.components.v1 as components
import plotly.graph_objects as go
import pydeck as pdk
import logging
import re
import data_pull as dp
import figure_pull as fp

def main():
    # LINKS AND PARAMETERS
    START_DATE = '01/12/2021'
    CUT_OFF_DATE = '18/02/2022'
    DATE_NOW = date.today()
    DATE_NOW = DATE_NOW.strftime("%d/%m/%Y")
    LINK_EXT_VOTE = "https://www.economist.com/sites/default/files/images/print-edition/20220305_FBM981.png"
    LINK_LOCAL_IMAGE = "assets/UN_vote.png" #
    LINK_LOCAL_TEXTS = "assets/text.xlsx"
    LINK_EXT_REFUGEES = "https://data2.unhcr.org/population/get/sublocation?widget_id=283559&sv_id=54&population_group=5459,5460&forcesublocation=0&fromDate=1900-01-01"
    LINK_LOCAL_REFUGEES = "assets/last_refugees.xlsx"
    LINK_EXT_FUNDS = "https://data.humdata.org/dataset/3ade4119-fa7c-476b-94a9-f001c6c8e7ba/resource/ad246b9d-dcc2-44bf-9863-a57a745e6fcb/download/fts_requirements_funding_globalcluster_ukr.csv"
    LINK_LOCAL_FUNDS = "assets/last_funds.xlsx"
    LINK_EXT_CASUALTIES = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQIdedbZz0ehRC0b4fsWiP14R7MdtU1mpmwAkuXUPElSah2AWCURKGALFDuHjvyJUL8vzZAt3R1B5qg/pub?output=csv"
    LINK_LOCAL_CASUALTIES = "assets/last_casualties.xlsx"
    LINK_EXT_REG_IDPS = "https://data.humdata.org/dataset/697c4fb9-1b76-4a66-808a-9a8fb5ffff1a/resource/013ffdf6-1b14-4a25-a194-4acf82251c75/download/idp_estimation_08_03_2022-unhcr-protection-cluster_.xlsx"
    LINK_EXT_SURVEY_IDPS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRZLuDJYqm22MRR7Njef34Nit6EX7CdYKL5afGM6jgMmBSTrNA5wW-SNxFpGnjE5OZys09ejB5r_1j0/pub?output=xlsx"
    LINK_LOCAL_REG_IDPS = "assets/last_reg_idps.xlsx"
    LINK_LOCAL_SURVEY_IDPS = "assets/last_survey_idps.xlsx"
    LINK_EXT_CBR = "http://www.cbr.ru/Collection/Collection/File/40867/full_032022.xlsx"
    LINK_LOCAL_CBR = "assets/full_032022.xlsx"
    LINK_LOCAL_INVESTING_DATA = "assets/last_investing_data.xlsx"
    BONDS = ['Russia']
    COMMODITIES = ['Gold', 'Brent Oil', 'Natural Gas', 'London Wheat', 'Nickel', 'Copper', 'London Sugar']
    FXS = ['EUR/RUB', 'EUR/UAH', 'EUR/USD', "USD/HUF", "USD/PLN", "USD/CZK", "USD/RSD", "USD/TRY", "USD/RON"]
    CEE_CURRENCIES = ["USD/HUF", "USD/PLN", "USD/CZK", "USD/RSD", "USD/TRY", "USD/RON"]

    # DATA AND FIGURES
    df_cbr_fcast = dp.get_cbr_forecasts(link_local = LINK_LOCAL_CBR)
    logging.info("CBR data pulled")
    df_fts_needs = dp.get_fts_needs(LINK_EXT_FUNDS, LINK_LOCAL_FUNDS)
    logging.info("FTS data pulled")
    df_unhcr_refugees = dp.get_refugees(LINK_EXT_REFUGEES, LINK_LOCAL_REFUGEES)
    logging.info("UNHCR refugee data pulled")
    df_unhcr_casualties = dp.get_casualties(LINK_EXT_CASUALTIES, LINK_LOCAL_CASUALTIES)
    logging.info("UNHCR casualties data pulled")
    #df_unhcr_reg_idps = dp.get_reg_idps(LINK_EXT_REG_IDPS, LINK_LOCAL_REG_IDPS)
    #logging.info("UNHCR registered idps data pulled")
    df_unhcr_survey_idps = dp.get_survey_idps(LINK_EXT_SURVEY_IDPS, LINK_LOCAL_SURVEY_IDPS)
    logging.info("Survey idps data pulled")
    df_investing_data = dp.get_data(
        bonds = BONDS, 
        fxs = FXS, 
        commodities = COMMODITIES, 
        spreads = BONDS, 
        tenor_bonds = 10, 
        tenor_spreads = 10, 
        bench_bond = "Germany",
        market = "United Kingdom",
        start_date = START_DATE, 
        to_date = DATE_NOW,
        link_local=LINK_LOCAL_INVESTING_DATA)
    logging.info("Investing data pulled")

    # FIGURES
    fig_unhcr_casualties = fp.fig_unhcr_casualties(df_unhcr_casualties, key='Civilian casualities(OHCHR) - Killed', height = 400, width = 400)
    #fig_unhcr_injured = fp.fig_unhcr_casualties(df_unhcr_casualties, key='Civilian casualities(OHCHR) - Injured', height = 300, width = 300)
    fig_unhcr_refugees = fp.fig_unhcr_casualties(df_unhcr_casualties, key='Refugees(UNHCR)', height = 400, width = 400)
    fig_cbr_gdp = fp.fig_cbr_forecast(df_cbr_fcast, 'Year', "GDP (%, YoY)", "90th percentile", "10th percentile", "Median", height = 200, width = 400)
    fig_cbr_fx = fp.fig_cbr_forecast(df_cbr_fcast, 'Year', "USD / RUB rate (RUB per USD, average for the year)", "90th percentile", "10th percentile", "Median", height = 200, width = 400)
    fig_cbr_cpi = fp.fig_cbr_forecast(df_cbr_fcast, 'Year', "CPI (in% Dec to Dec of the previous year)", "90th percentile", "10th percentile", "Median", height = 200, width = 400)
    fig_cbr_krt = fp.fig_cbr_forecast(df_cbr_fcast, 'Year', "Key rate (% per annum, average for the year)", "90th percentile", "10th percentile", "Median", height = 200, width = 400)
    fig_fx_rub = fp.fig_investing_data(df_investing_data,'EUR/RUB', width=400, height=400, bench_date=CUT_OFF_DATE)
    fig_spread_ru = fp.fig_investing_data(df_investing_data,'Russia vs Germany: 10Y', width=400, height=400, bench_date=CUT_OFF_DATE)
    fig_refugees = fp.fig_unhcr_refugees(df_unhcr_refugees)
    fig_survey_idps = fp.fig_survey_idps(df_unhcr_survey_idps)
    fig_fts_needs = fp.fig_fts_needs(df_fts_needs)
    fig_brent_oil = fp.fig_investing_data(df_investing_data,'Brent Oil', width=400, height=400, bench_date=CUT_OFF_DATE)
    fig_natural_gas = fp.fig_investing_data(df_investing_data,'Natural Gas', width=400, height=400, bench_date=CUT_OFF_DATE)
    fig_gold = fp.fig_investing_data(df_investing_data,'Gold', width=400, height=400, bench_date=CUT_OFF_DATE)
    fig_copper = fp.fig_investing_data(df_investing_data, 'Copper', width=400, height=400, bench_date=CUT_OFF_DATE)
    fig_brent_oil = fp.fig_investing_data(df_investing_data,'Brent Oil', width=400, height=400, bench_date=CUT_OFF_DATE)
    fig_london_wheat = fp.fig_investing_data(df_investing_data,'London Wheat', width=400, height=400, bench_date=CUT_OFF_DATE)
    fig_london_sugar = fp.fig_investing_data(df_investing_data,'London Sugar', width=400, height=400, bench_date=CUT_OFF_DATE)
    #map_reg_idps = fp.map_reg_idps(df_unhcr_reg_idps)

    # FINAL REPORT
    st.title('Tracking the Costs and Consequences of the Russian Invasion of Ukraine')
    st.subheader("Humanitarian needs in Ukraine: Latest Estimation")
    st.write(dp.get_text(LINK_LOCAL_TEXTS, label_val='summary_short_effects'))
    cmet11, cmet12, cmet13, cmet14 = st.columns(4)
    cmet21, cmet22, cmet23, cmet24 = st.columns(4)
    st.write(dp.get_text(LINK_LOCAL_TEXTS, label_val='summary_long_effects'))
    cmet11.metric("Refugees, mn people", round(df_unhcr_casualties['Refugees']/10**6,1))
    cmet21.metric("IDPs, mn people", round(df_unhcr_casualties['IDPs']/10**6,1))
    cmet12.metric("Civilians, fatalities", df_unhcr_casualties['Killed'], df_unhcr_casualties['Delta killed'], delta_color='inverse')
    cmet22.metric("Civilians, injuries", df_unhcr_casualties['Injured'], df_unhcr_casualties['Delta injured'], delta_color='inverse')
    cmet13.metric("Total needs, $ BN", df_fts_needs['Total'])
    cmet23.metric("Funded needs $ BN", df_fts_needs['Funded'])
    cmet14.metric("Education facil. damaged", df_unhcr_casualties['Attacks Schools'], df_unhcr_casualties['Delta attacks schools'], delta_color='inverse')
    cmet24.metric("Healthcare facil. damaged", df_unhcr_casualties['Attacks Healthcare'], df_unhcr_casualties['Delta attacks healthcare'], delta_color='inverse')
    intro_fig1, intro_fig2 = st.columns(2)
    fp.plot_figure(intro_fig1.plotly_chart(fig_unhcr_casualties, height = 400, width = 400))
    #fp.plot_figure(intro_fig3.plotly_chart(fig_unhcr_injured, height = 300, width = 300))
    fp.plot_figure(intro_fig2.plotly_chart(fig_unhcr_refugees, height = 400, width = 400))
    st.markdown('---')
    st.header('Damage to Ukraine')
    st.write(dp.get_text(LINK_LOCAL_TEXTS, label_val='key_damage'))
    cfig01, cfig02 = st.columns(2)
    fp.plot_figure(cfig01.plotly_chart(fig_refugees))
    fp.plot_figure(cfig02.plotly_chart(fig_survey_idps))
    #fp.plot_figure(st.pydeck_chart(map_reg_idps))
    st.write(dp.get_text(LINK_LOCAL_TEXTS, label_val='ukraine_costs'))
    fp.plot_figure(st.plotly_chart(fig_fts_needs))
    st.write(dp.get_text(LINK_LOCAL_TEXTS, label_val='ukraine_macro'))
    st.header('Economic Fallout in Russia')
    st.write(dp.get_text(LINK_LOCAL_TEXTS, label_val='russia_economy'))
    st.markdown("**Forecasts of the Key Macro Indicators By Professional Forecasters**")
    st.markdown("*Source*: Central Bank of Russia")
    cfig_ru_11, cfig_ru_12 = st.columns(2)
    fp.plot_figure(cfig_ru_11.plotly_chart(fig_cbr_gdp))
    fp.plot_figure(cfig_ru_12.plotly_chart(fig_cbr_cpi))    
    cfig_ru_21, cfig_ru_22 = st.columns(2)
    fp.plot_figure(cfig_ru_21.plotly_chart(fig_cbr_fx))
    fp.plot_figure(cfig_ru_22.plotly_chart(fig_cbr_krt))
    st.markdown("**Impact on the Russian Financial Market**")
    cfig_ru_31, cfig_ru_32 = st.columns(2)
    fp.plot_figure(cfig_ru_31.plotly_chart(fig_fx_rub))
    fp.plot_figure(cfig_ru_32.plotly_chart(fig_spread_ru))
    st.write(dp.get_text(LINK_LOCAL_TEXTS, label_val='russia_policies'))
    fp.plot_figure(components.iframe("https://datawrapper.dwcdn.net/EQ9IF/3/", height=800, scrolling=True))
    fp.plot_figure(components.iframe("https://datawrapper.dwcdn.net/ZVnMA/4/", height=800, scrolling=True))
    #fp.plot_figure(components.iframe("https://datawrapper.dwcdn.net/17yDJ/2/", height=800, scrolling=True))
    st.write(dp.get_text(LINK_LOCAL_TEXTS, label_val='russia_sanctions'))
    st.header('Spillovers to Europe and Global Markets')
    st.write(dp.get_text(LINK_LOCAL_TEXTS, label_val='inflation'))
    st.write(dp.get_text(LINK_LOCAL_TEXTS, label_val='europe_finance'))

    # fx_select = st.selectbox(
    #     'Choose a currency pair',
    #     ("USD/HUF", "USD/PLN", "USD/CZK", "USD/RSD", "USD/TRY", "USD/RON"))
    
    # fig_cee_currency = fp.fig_investing_data(df_investing_data, fx_select, bench_date=CUT_OFF_DATE, height=400, width=400)
    # fp.plot_figure(st.plotly_chart(fig_cee_currency))

    fx_selects = st.multiselect(
        'Select the currency pair for comparison',
        CEE_CURRENCIES,
        CEE_CURRENCIES[:2])

    fig_cee_currencies = fp.fig_investing_data_multi(df_investing_data, fx_selects, title = "Selected CEE currency pairs")    
    fp.plot_figure(st.plotly_chart(fig_cee_currencies))

    st.write(dp.get_text(LINK_LOCAL_TEXTS, label_val='europe_energy'))
    col_comm11, col_comm12 = st.columns([1,1])
    fp.plot_figure(col_comm11.plotly_chart(fig_brent_oil))
    fp.plot_figure(col_comm12.plotly_chart(fig_natural_gas))
    col_comm21, col_comm22 = st.columns([1,1])
    fp.plot_figure(col_comm21.plotly_chart(fig_gold))
    fp.plot_figure(col_comm22.plotly_chart(fig_copper))
    col_comm31, col_comm32 = st.columns([1,1])
    fp.plot_figure(col_comm31.plotly_chart(fig_london_wheat))
    fp.plot_figure(col_comm32.plotly_chart(fig_london_sugar))
    st.write(dp.get_text(LINK_LOCAL_TEXTS, label_val='europe_trade_exposure'))
    st.write(dp.get_text(LINK_LOCAL_TEXTS, label_val='europe_refugees'))

    st.header("What Happens Next")
    st.image(LINK_LOCAL_IMAGE, caption="Votes in favor of the UN Resolution condemning Russian invastion in Ukraine. Source: The Economist")
    st.subheader('Ukraine')
    st.write(dp.get_text(LINK_LOCAL_TEXTS, label_val='outlook_ukraine'))
    st.subheader('Russia')
    st.write(dp.get_text(LINK_LOCAL_TEXTS, label_val='outlook_russia'))
    st.subheader('European Union')
    st.write(dp.get_text(LINK_LOCAL_TEXTS, label_val='outlook_eu'))
    st.write(dp.get_text(LINK_LOCAL_TEXTS, label_val='policies'))

if __name__ == '__main__':
    main()
