from datetime import date
import streamlit as st
import pandas as pd
import investpy as ipy
import plotly.express as px
import plotly.graph_objects as go
import pydeck as pdk
import logging
import data_pull as dp

def fig_unhcr_casualties(df, key = str, data_key = 'data', date_key = 'Date', source = 'UNHCR', width = 0, height = 0):
    df = df[data_key]
    ymin = 0
    ymax = df[key].max() + df[key].std()
    #fig = px.area(df, y = key)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df[date_key], y=df[key], fill = 'tozeroy', mode='none'))
    #fig.add_trace(go.Scatter(x=df.index, y=df[key],  fill = 'tonexty', mode='none'))

    fig = fig.update_layout(
        title = f"{key}<br><sup>Source: {source}</sup>",
        yaxis_range = [ymin, ymax])

    if width > 0 & height > 0:
        fig = fig.update_layout(
            width = width,
            height = height)
    elif width > 0 & height == 0:
        fig = fig.update_layout(
            width = width)
    elif width == 0 & height > 0:
        fig = fig.update_layout(
            height = height)
        
    return fig


def fig_yahoo_data(df, key = str, data_key = 'data', source = 'Yahoo Finance', width = 0, height = 0, bench_date = date, impact_date = "2022-02-24"):
    df = dp.get_key(df, key=key, bench_date=bench_date)[data_key]
    ymin = df[key].min() - df[key].std()
    ymax = df[key].max() + df[key].std()
    #fig = px.area(df, y = key)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df[key], fill = 'tozeroy', mode='none'))
    #fig.add_trace(go.Scatter(x=df.index, y=df[key],  fill = 'tonexty', mode='none'))

    fig = fig.update_layout(
        title = f"{key}<br><sup>Source: {source}</sup>",
        yaxis_range = [ymin, ymax])
    fig = fig.add_vline(x=impact_date, line_width=1.5, line_dash="dash", line_color="red")

    if width > 0 & height > 0:
        fig = fig.update_layout(
            width = width,
            height = height)
    elif width > 0 & height == 0:
        fig = fig.update_layout(
            width = width)
    elif width == 0 & height > 0:
        fig = fig.update_layout(
            height = height)
        
    return fig

def fig_yahoo_data_multi(df, keys = list, ref_date = '2021-12-01', source = 'Yahoo Finance', width = 0, height = 0, title = str):
    df_plot = df[df['instrument'].isin(keys)]
    df_ref = df_plot.loc[df_plot.index == ref_date]
    df_plot['Date'] = df_plot.index
    df_plot = pd.merge(df_plot, df_ref,  how='inner', left_on='instrument', right_on = 'instrument')
    df_plot['Close_x'] = df_plot['Close_x'] / df_plot['Close_y']
    if width > 0 & height > 0:
        fig = px.line(
                df_plot,
                x = 'Date',
                y='Close_x',
                color = 'instrument',
                width = width,
                height = height
                )
    elif width > 0 & height == 0:
        fig = px.line(
            df_plot,
            x = 'Date',
            y='Close_x',
            color = 'instrument',
            width = width)
    elif width == 0 & height > 0:
        fig = px.line(
            df_plot,
            x = 'Date',
            y='Close_x',
            color = 'instrument', 
            height = height)
    else:
        fig = px.line(
            df_plot,
            x = 'Date',
            y='Close_x',
            color = 'instrument',
            )

    fig = fig.add_vline(x="2022-02-24", line_width=1.5, line_dash="dash", line_color="red")
    title = title
    fig = fig.update_layout(title = f"{title}<br><sup>Source: {source}</sup>", 
                            yaxis_title='Value-to-Date to Value as of December 1st')

    fig.update_layout(showlegend = True)
        
    return fig

# Graphs for CBR forecasts
def fig_cbr_forecast(df_data, date_var = str, plot_var = str, ubound_filter = str, lbound_filter = str, median_filter = str, filter_var = 'Stat', width = 0, height = 0):
    df = df_data

    if width > 0 & height > 0:
        fig = go.Figure(layout=go.Layout(
            width = width,
            height = height
            )
        )
    elif width > 0 & height == 0:
        fig = go.Figure(layout=go.Layout(
            width = width
            )
        )
    elif width == 0 & height > 0:
        fig = go.Figure(layout=go.Layout(
            height = height
            )
        )
    else:
        fig = go.Figure(layout=go.Layout(
            )
        )    

    fig = fig.update_layout(title = f"{plot_var}<br><sup>Source: Central Bank of Russia: Consensus Forecast</sup>")

    # Create and style traces
    fig.add_trace(
        go.Scatter(
            x=df.loc[df[filter_var] == median_filter][date_var], 
            y=df.loc[df[filter_var] == median_filter][plot_var], 
            name='Median forecast',
            line=dict(
                color='rgb(0,176,246)', 
                width=2
            )
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.loc[df[filter_var] == lbound_filter][date_var], 
            y=df.loc[df[filter_var] == lbound_filter][plot_var], 
            name='10% percentile',
            line=dict(
                color='rgb(0,156,246)', 
                width=2,
                dash = 'dash'
            )
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.loc[df[filter_var] == ubound_filter][date_var], 
            y=df.loc[df[filter_var] == ubound_filter][plot_var], 
            name='90% percentile',
            line=dict(
                color='rgb(0,196,246)', 
                width=2,
                dash = 'dash'
            )
        )
    )

    fig = fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.5,
        #xanchor="right",
        #x=1
    ))

    fig = fig.update_traces(mode='lines')
    return fig

def fig_unhcr_refugees(df):
    df_unhcr = df['data']
    total_refugees = df['total']
    total_refugees = round(total_refugees/10**6, 2)
    xmax = df_unhcr['individuals'].max() + (10**6)/2
    
    fig = go.Figure(layout=go.Layout(
                                    title=go.layout.Title(text="Distribution of Refugees, mn<br><sup>Source: UNOCHA</sup>"),
                                    width = 400,
                                    )
                    )
    fig.update_layout(xaxis_range = [0, xmax])
    fig.add_trace(go.Bar(
                        y=df_unhcr['geomaster_name'],
                        x=df_unhcr['individuals'],
                        name='Persons, k',
                        orientation='h',
                        text = round(df_unhcr['individuals']/10**6, 2)
                    )
                )

    fig.update_traces(textangle=0, textposition="outside", cliponaxis=False)
    return fig

def fig_survey_idps(df):
    df_idps_reg = df['data']
    idps_total = df['total']/10**6
    idps_total = round(idps_total, 2)
    xmax = df_idps_reg['# est. IDPs presence per macro-region'].max() + (10**6)/2

    fig = go.Figure(layout=go.Layout(
                    title=go.layout.Title(text="Distribution of IDP, mn<br><sup>Source: UNOCHA</sup>"),
                    width = 400
                )
            )
    fig.update_layout(xaxis_range = [0, xmax])
    fig.add_trace(go.Bar(
                        y=df_idps_reg['Macro-region'],
                        x=df_idps_reg['# est. IDPs presence per macro-region'],
                        name='Persons, mn',
                        orientation='h',
                        text = round(df_idps_reg['# est. IDPs presence per macro-region']/10**6, 2),
                    ))

    fig.update_traces(textangle=0, textposition="outside", cliponaxis=False)
    return fig

def map_reg_idps(df):
    # Map of IDPs
    df_idps = df['data']
    fig = pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
        latitude=48.5,
        longitude=28.5,
        zoom=5,
        pitch=0,
        ),
        #mapbox_key=token,
        layers=[
            pdk.Layer(
            "ScatterplotLayer",
            data=df_idps,
            get_position=['long', 'lat'],
            #get_weigth = 'idp',
            get_radius='idp',
            radius_min_pixels=10,
            radius_max_pixels=20,
            get_fill_color=[255, 140, 0],
            get_line_color=[0, 0, 0],
            opacity = 0.4,
            stroked=True,
            filled=True,
            pickable=True
            )
        ]
    )
    return fig

def fig_fts_needs(df):
    # Dictionary contains info on metrics and df
    hum_needs = df

    fig = go.Figure(layout=go.Layout(
        title=go.layout.Title(text="Required humanitarian assistance by clusters, $ mn<br><sup>Source: FTS UN OCHA</sup>"),
        height = 800
        )
    )

    fig.add_trace(go.Bar(
        y=hum_needs['df']['cluster'],
        x=hum_needs['df']['requirements'],
        name='Required (US$)',
        orientation='h',
        text = round(hum_needs['df']['requirements']/10**6, 0)
        # marker=dict(
        #     color='rgba(246, 78, 139, 0.6)',
        #     line=dict(color='rgba(246, 78, 139, 1.0)', width=3)
        # )
        ))

    fig.add_trace(go.Bar(
        y=hum_needs['df']['cluster'],
        x=hum_needs['df']['funding'],
        name='Funded (US$)',
        orientation='h',
        text = round(hum_needs['df']['funding']/10**6, 0)
            # marker=dict(
            #     color='rgba(58, 71, 80, 0.6)',
            #     line=dict(color='rgba(58, 71, 80, 1.0)', width=3)
            # )
        ))

    fig.update_traces(textangle=0, textposition="outside", cliponaxis=False)
    return fig

def plot_figure(fig):
    try:
        return fig
    except Exception as e:
        logging.warning(f"Cannot plot figure {fig}", exc_info=True)

if __name__ == '__main__':
    pass