from datetime import date
import streamlit as st
import pandas as pd
import investpy as ipy
import altair as alt
import plotly.express as px
import streamlit.components.v1 as components
import plotly.graph_objects as go

#PARAMETERS
start_date = '01/12/2021'
cut_off = '18/02/2022'
date_now = date.today()
date_now = date_now.strftime("%d/%m/%Y")
link_img = "https://www.economist.com/sites/default/files/images/print-edition/20220305_FBM981.png"
link_refugee = "https://data2.unhcr.org/population/get/sublocation?widget_id=283559&sv_id=54&population_group=5459,5460&forcesublocation=0&fromDate=1900-01-01"
#link_total_needs = "https://fts.unocha.org/download/281410/download"
link_cluster_needs = "https://data.humdata.org/dataset/3ade4119-fa7c-476b-94a9-f001c6c8e7ba/resource/ad246b9d-dcc2-44bf-9863-a57a745e6fcb/download/fts_requirements_funding_globalcluster_ukr.csv"
print(date_now)

bonds = ['Russia']
commodities = ['Gold', 'Brent Oil', 'Natural Gas', 'London Wheat', 'Nickel', 'Copper', 'London Sugar']
fxs = ['EUR/RUB', 'EUR/UAH', 'EUR/USD', "USD/HUF", "USD/PLN", "USD/CZK"]

#TEXT
summary = "Russia’s invasion of Ukraine has created a humanitarian crisis that will unfortunately almost certainly intensify, \
    and Ukraine’s economy is going to suffer terribly. International sanctions will impose strong economic and financial pain on \
    Russia and limit its ability to contain the fallout. Sharp increases in energy prices will lead to ever higher inflation in the \
    rest of Europe, and could push some economies into recession this year. Parts of CESEE, including EU member states, are likely to \
    suffer some financial contagion. For Russia, absent regime change, the crisis will cut it off from most or all Western economic \
    integration, and possibly drive it into a closer and more subservient economic and financial relationship with China. The EU will \
    scramble to diversify away from energy reliance on Russia as quickly as possible, while also investing heavily in upgrading its military capabilities."

intro1 = "Russia’s attack on Ukraine marked the start of warfare in Europe on a scale not seen since the Balkan wars of the 1990s. Many people have already died, and as Russia launches apparently increasingly indiscriminate shelling of major cities, the death toll is likely to rise dramatically. What was unimaginable a week ago is now happening. Reports from Ukraine show an already high level of human suffering.\
        Projecting developments from here requires a level of military expertise that we do not possess at wiiw. Taking our cue from those who know better, we envisage two possible broad scenarios."
        
intro2 = "The first is that Russia intensifies its attacks on Ukraine’s cities, causing a great deal of destruction of both human life and infrastructure, and ends up occupying a part, if not all, of the country, However, it is \
        not likely that Russia has the resources for a long-term occupation of the country (that is not to say that it will not try for some time, at least in part of Ukraine, but it will likely have to deal with guerrilla resistance). Moscow will then be forced to the negotiating table and likely demand various written commitments from Ukraine to agree to withdraw. There are already suggestions for how Putin’s “off-ramp” \
        could look, but to us these proposals still need some work. Hard sanctions are likely to remain in place for a long period." 

intro3 = "A second broad possible scenario is that, in reaction to sanctions pressure and a loss of their privileges in the West, Russian elites oust President Putin and his administration and end the war. Sanctions would be gradually removed, and economic and financial ties cautiously rebuilt. We do not know enough to put probabilities on these scenarios, but we judge the first as more likely than the second. \
        At wiiw we are undertaking a quantitative analysis to try to understand the impact of the war on the economics of Ukraine, Russia and the rest of Europe. In advance of the publication of that paper, here we outline our mostly qualitative assessments of developments so far."

fallout1 = "**Ukraine**: The impact on Ukraine’s economy and society is already dramatic and will become even more so. More than one million people have already fled, and the number of refugees may be several times that by the time the war ends. Evidence from recent conflicts suggest that the negative economic shock will be severe. As long as the war goes on, Ukraine will receive major financial (as well as military) support from much of the rest of the world. But the costs of reconstruction in Europe’s second biggest country will be enormous."
fallout2 = "**Russia**: As a result of its invasion, Russia faces heavy sanctions from the outside world. Reserves held in many foreign countries have been frozen, Russia has been partly excluded from SWIFT, and it now cannot important many high-tech and consumer goods (leading to panic buying). The rouble has collapsed and inflation will sky-rocket. For ordinary Russians, there is likely to be a great deal more economic pain to follow. The Russian Central Bank has shown itself in the past to be a highly capable operator. It is facing its stiffest test yet. While it may be possible to maintain a semblance of macro-financial stability, this is likely to require extremely restrictive monetary policy (it has already more than doubled interest rates), that will further amplify the negative economic shock."
fallout3 = "The Russian regime has spent many years building up resistance to Western economic pressure, but it clearly did not expect the speed and extent to which it would be sanctioned followed the invasion. While the authorities still have tools—not least the National Wealth Fund, some ability to tap more domestic sources of financing, and forcing firms to surrender most of their hard currency earnings—these are not infinite. Much now depends on the ability to continue to sell energy, and particularly gas to the EU. Oil traders are increasingly wary of Russian oil, forcing a large discount on barrels from the country. It is no longer unthinkable that the EU will decide to stop importing Russian gas. As EU residents are faced by scenes of humanitarian crisis on the TV news each night, public support for such a measure, and a willingness to face the costs of that, will likely grow. Studies recently produced by Algebris Investments and Bruegel try to put some numbers on this – the conclusion seems to be that the EU can cut imports of Russian gas completely, but should be prepared to pay quite a price for it."
fallout4 = "**The rest of Europe**: The EU, US, UK, Switzerland and others have moved quickly and strongly to sanction Russia. Freezing the central banks’ assets abroad deprives the Russian authorities of much of their ability to cushion the overall shock. Targeting of oligarchs is also a significant step, which could lead to increased domestic pressure on President Putin. However, the truly nuclear option for the EU—stopping buying Russian gas—has not yet been taken."
fallout5 = "Even with the current sanctions, commodity prices have risen, adding to already strong inflationary pressures across Europe. This will weigh on real incomes, and has led to speculation that Germany will be unable to avoid at least a technical recession. Given that inflation will be commodity-driven, and that the broader economic outlook has weakened, the ECB will probably push back any plans for monetary policy normalisation this year. Several European banks with Russian exposure are under pressure. Many other European firms are cutting ties with Russia. However, overall non-energy trade and investment ties between most of Europe and Russia are small, so here the channels of contagion are limited."
fallout6 = "Some financial contagion is already visible in CESEE. Currencies have weakened in countries near to Russia and Ukraine due to higher risk aversion, and interest rates on government debt have in some cases increased. Investor sentiment—both domestic and foreign—in the Baltic states is likely to suffer amid fears that Russia has designs on more than Ukraine. Poland, Slovakia, Hungary and others are already seeing a massive influx of refugees. Put brutally, this is a potential windfall for their labour markets."
fallout7 = "**Ukraine**: The outlook for the Ukrainian population and economy is bleak. The country may yet end up divided, however, with a Western part receiving major Western support to get back on its feet. It will take enormous resources, and a great deal of time, to rebuild what has been and will be destroyed in the conflict."
fallout8 = "**Russia**: If Russia destroys Ukrainian cities, commits war crimes and occupies parts or all of the country, it will become and international pariah state akin to Iran or Venezuela. Its ability to generate hard currency revenues via oil and gas will be curtailed, and it will become ever more economically integrated with, and dependent on, China. Russia’s long-term growth potential, already meagre, will fall further."
fallout9 = "**The rest of Europe**: Russia’s invasion of Ukraine is a crucial moment for both European and broader Western integration. The EU will scramble to diversify away from Russian energy sources as quickly as possible. That will include possible increased use of coal in the short run, planning new nuclear energy projects, looking for other sources of gas, and building LNG terminals. However, the central component will be a reinforcing of the green transition already underway, which in turn is the core element of the next phase of European integration (and the cornerstone of the EU’s response to economic fallout from the pandemic). As well as boosting investment in renewable energy sources, it will also be a catalyst to the development of greener transport, including major new transportation initiatives to bring many Europeans closer together."
fallout10 = "At present, the Russian invasion looks set to presage a fundamental unwinding of 30 years of economic integration between Russia and the West. As well as the harsh financial sanctions imposed on Russia, Western firms are leaving Russia en masse. That creates the likelihood that, even if at some point sanctions are eased, February 2022 may well have marked the highpoint of European economic integration in its broadest sense."
fallout11 = "It can also be hoped that the crisis will deliver a jolt to the EU accession process in the Western Balkans. Ukraine shows that piecemeal integration efforts from the EU can be quickly unwound. Until the countries of the Western Balkans are fully integrated into Euro-Atlantic institutions, including the EU, their development is fragile."
fallout12 = "EU countries will also now ramp up military spending, with Germany’s announcement that it will massively increase funds for defence in the wake of the Russian invasion particularly notable. Although truly EU stand-alone military capabilities are still hard to imagine anytime soon, EU countries will play a much stronger role as part of NATO than in the past. This is likely to include a much bigger permanent presence of NATO troops in the Baltic states and Poland. Economically, financially, politically and militarily, this situation, at least for some time, will be closer to the Cold War than anything we have seen in European since 1989."

# FUNCTIONS
def strip_ipy_df(df = pd.DataFrame(), instrument = str, rename = True):
    df = df[['Close']]
    if rename == True:
        df = df.rename(columns={"Close": instrument})
    return df

def get_bond(country, tenor = 10, benchmark = 'Germany'):
    country_bond = str(country) + " " + str(tenor) + "Y"
    df_country_bond = ipy.bonds.get_bond_historical_data(bond=country_bond,
                                            from_date=start_date,
                                            to_date=date_now)

    bench_bond = str(benchmark) + " " + str(tenor) + "Y"
    df_bench_bond = ipy.bonds.get_bond_historical_data(bond=bench_bond,
                                            from_date=start_date,
                                            to_date=date_now)

    # Generate YTMs
    df_country_bond_export = strip_ipy_df(df_country_bond, country_bond, rename = False)
    df_country_bond_merge = strip_ipy_df(df_country_bond, country_bond)
    df_country_bond_export['instrument'] = country_bond

    # Generate spreads
    spread_name = str(country_bond) + " vs " + str(bench_bond)
    df_bench_bond = strip_ipy_df(df_bench_bond, bench_bond)
    df_spread = pd.merge(df_country_bond_merge, df_bench_bond, left_index=True, right_index=True)
    df_spread[spread_name] = df_spread[country_bond] - df_spread[bench_bond]
    df_spread = df_spread[[spread_name]]
    df_spread['instrument'] = spread_name
    df_spread = df_spread.rename(columns={spread_name: "Close"})
    df = pd.DataFrame()

    df = df.append(df_country_bond_export)
    df = df.append(df_spread)
    #print(df)
    return df

def get_fx(fx):
    df = ipy.get_currency_cross_historical_data(currency_cross=fx, 
                                                from_date=start_date, 
                                                to_date=date_now)
    df = df[['Close']]
    df['instrument'] = fx
    return df

def get_commodity(commodity):
    df = ipy.commodities.get_commodity_historical_data(commodity=commodity, 
                                                from_date=start_date, 
                                                to_date=date_now)
    df = df[['Close']]
    df['instrument'] = commodity
    return df

@st.cache
def get_data(bonds, fxs, commodities):
    df = pd.DataFrame()    
    
    for bond in bonds:
        df = df.append(get_bond(bond))

    for fx in fxs:
        df = df.append(get_fx(fx))

    for commodity in commodities:
        df = df.append(get_commodity(commodity))

    return df

@st.cache
def get_unhcr(link):
    df = pd.read_json(link)
    df = pd.json_normalize(df['data'])
    df = df[['geomaster_name', 'individuals']]
    df['individuals'] = pd.to_numeric(df['individuals'])
    df.sort_values(by='individuals', ascending=False)
    return df

@st.cache
def get_fts_needs(link):
    df = pd.read_csv(link)
    df = df.loc[(df['code'] == 'FUKR22') & (df['countryCode'] == 'UKR')]
    df = df[(df['requirements'].isnull() == False) | ((df['requirements'].isnull() == True) & (df['cluster'].isin(['Not specified', 'Multiple clusters/sectors (shared)']) == True))]
    df['requirements'] = pd.to_numeric(df['requirements'], errors='coerce')
    df['funding'] = pd.to_numeric(df['funding'], errors='coerce')
    #df = df.dropna(subset=['requirements'])
    df = df.sort_values(['requirements'], ascending=False)
    funded_needs = df['funding'].sum()
    total_needs = df['requirements'].sum()
    ratio_funded_total = funded_needs / total_needs
    ratio_funded_total = "{:.0%}".format(ratio_funded_total)
    funded_needs = round(funded_needs/10**9, 2)
    total_needs = round(total_needs/10**9, 2)
    output = {'df': df, 'Funded': funded_needs, 'Total': total_needs, 'Requirements met': ratio_funded_total}
    return output

def get_key(df = pd.DataFrame(), key=str):
    df = df.loc[df['instrument'] == key]
    df = df[["Close"]]
    df = df.rename(columns={"Close": key})
    min = df[key].min()
    max = df[key].max()
    sd = df[key].std()
    pre_crisis = df[key][cut_off]
    last = df[key][len(df)-1]
    lvl_delta = round(last - pre_crisis, 2)
    pct_delta = "{:.0%}".format(round(lvl_delta/pre_crisis, 2))
    return_dict = {'data': df, 'last': last, 'lvl_delta': lvl_delta, 'pct_delta': pct_delta, 'min': min, 'max': max, 'sd': sd}
    return return_dict

# DATA AND CHARTS
df = get_data(bonds, fxs, commodities)
#df_bonds = get_key(df, "Russia 10Y")

df_unhcr = get_unhcr(link_refugee)
total_refugees = df_unhcr['individuals'].sum()
total_refugees = round(total_refugees/10**6, 2)

refugee_chart = alt.Chart(df_unhcr).mark_bar().encode(
    x=alt.X('geomaster_name', sort='-y', axis=alt.Axis(title='Country')),
    y=alt.Y('individuals', axis=alt.Axis(title='Refugee count'))
).properties(height=700, title = 'Ukrainian Refugees in Neighbor Countries')

refugee_chart = refugee_chart.configure_title(
    fontSize=20,
    #font='Courier',
    #anchor='start',
    #color='gray'
)

# Dictionary contains info on metrics and df
hum_needs = get_fts_needs(link_cluster_needs)

fig_hum_needs = go.Figure(layout=go.Layout(
        title=go.layout.Title(text="Required humanitarian assistance by clusters, $ mn<br><sup>Source: FTS UN OCHA</sup>"),
        height = 800
        )
    )

fig_hum_needs.add_trace(go.Bar(
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

fig_hum_needs.add_trace(go.Bar(
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

fig_hum_needs.update_traces(textangle=0, textposition="outside", cliponaxis=False)

fig_fx_uaheur = px.area(
    get_key(df, "EUR/UAH")['data'],
    y="EUR/UAH", 
    title = "EUR/UAH Exchange Rate<br><sup>Source: Investing.com</sup>",
    range_y=[get_key(df, "EUR/UAH")['min']-get_key(df, "EUR/UAH")['sd'],get_key(df, "EUR/UAH")['max']+get_key(df, "EUR/UAH")['sd']])

fig_fx_rubeur = px.area(
    get_key(df, "EUR/RUB")['data'],
    y="EUR/RUB", 
    title = "EUR/RUB Exchange Rate<br><sup>Source: Investing.com</sup>",
    range_y=[get_key(df, "EUR/RUB")['min']-get_key(df, "EUR/RUB")['sd'],get_key(df, "EUR/RUB")['max']+get_key(df, "EUR/RUB")['sd']],
    width = 450)

fig_fx_hufusd = px.area(
    get_key(df, "USD/HUF")['data'],
    y="USD/HUF", 
    title = "USD/HUF Exchange Rate<br><sup>Source: Investing.com</sup>",
    range_y=[get_key(df, "USD/HUF")['min']-get_key(df, "USD/HUF")['sd'],get_key(df, "USD/HUF")['max']+get_key(df, "USD/HUF")['sd']],
    width = 300,
    height = 300)

fig_fx_plnusd = px.area(
    get_key(df, "USD/PLN")['data'],
    y="USD/PLN", 
    title = "USD/PLN Exchange Rate<br><sup>Source: Investing.com</sup>",
    range_y=[get_key(df, "USD/PLN")['min']-get_key(df, "USD/PLN")['sd'],get_key(df, "USD/PLN")['max']+get_key(df, "USD/PLN")['sd']],
    width = 300,
    height = 300)

fig_fx_czkusd = px.area(
    get_key(df, "USD/CZK")['data'],
    y="USD/CZK", 
    title = "USD/CZK Exchange Rate<br><sup>Source: Investing.com</sup>",
    range_y=[get_key(df, "USD/CZK")['min']-get_key(df, "USD/CZK")['sd'],get_key(df, "USD/CZK")['max']+get_key(df, "USD/CZK")['sd']],
    width = 300,
    height = 300)

fig_bond_ru10de10 = px.area(
    get_key(df, "Russia 10Y vs Germany 10Y")['data'],
    y="Russia 10Y vs Germany 10Y", 
    title = "Spread: Yield to Maturity of Russia 10Y vs Germany 10Y Bonds<br><sup>Source: Investing.com</sup>",
    range_y=[get_key(df, "Russia 10Y vs Germany 10Y")['min']-get_key(df, "Russia 10Y vs Germany 10Y")['sd'],get_key(df, "Russia 10Y vs Germany 10Y")['max']+get_key(df, "Russia 10Y vs Germany 10Y")['sd']],
    width = 450)

fig_comm_oil = px.area(
    get_key(df, "Brent Oil")['data'],
    y="Brent Oil", 
    title = "Brent Oil Price<br><sup>Source: Investing.com</sup>",
    range_y=[get_key(df, "Brent Oil")['min']-get_key(df, "Brent Oil")['sd'],get_key(df, "Brent Oil")['max']+get_key(df, "Brent Oil")['sd']],
    width = 450)

fig_comm_gas = px.area(
    get_key(df, "Natural Gas")['data'],
    y="Natural Gas", 
    title = "Natural Gas Price<br><sup>Source: Investing.com</sup>",
    range_y=[get_key(df, "Natural Gas")['min']-get_key(df, "Natural Gas")['sd'],get_key(df, "Natural Gas")['max']+get_key(df, "Natural Gas")['sd']],
    width = 450)

fig_comm_gold = px.area(
    get_key(df, "Gold")['data'],
    y="Gold", 
    title = "Gold Price<br><sup>Source: Investing.com</sup>",
    range_y=[get_key(df, "Gold")['min']-get_key(df, "Gold")['sd'],get_key(df, "Gold")['max']+get_key(df, "Gold")['sd']],
    width = 450)

fig_comm_copper = px.area(
    get_key(df, "Copper")['data'],
    y="Copper", 
    title = "Copper Price<br><sup>Source: Investing.com</sup>",
    range_y=[get_key(df, "Copper")['min']-get_key(df, "Copper")['sd'],get_key(df, "Copper")['max']+get_key(df, "Copper")['sd']],
    width = 450)

fig_comm_wheat = px.area(
    get_key(df, "London Wheat")['data'],
    y="London Wheat", 
    title = "Wheat Price (London) <br><sup>Source: Investing.com</sup>",
    range_y=[get_key(df, "London Wheat")['min']-get_key(df, "London Wheat")['sd'],get_key(df, "London Wheat")['max']+get_key(df, "London Wheat")['sd']],
    width = 450)

fig_comm_sugar = px.area(
    get_key(df, "London Sugar")['data'],
    y="London Sugar", 
    title = "Sugar Price (London) <br><sup>Source: Investing.com</sup>",
    range_y=[get_key(df, "London Sugar")['min']-get_key(df, "London Sugar")['sd'],get_key(df, "London Sugar")['max']+get_key(df, "London Sugar")['sd']],
    width = 450)

#APP
st.title('Security crisis in Europe')
# st.write("Increase in yields of Russian bonds since February 18th, 2022: " + str(bonds_drop*100) + " basis points. The yields jumped by " + str(bonds_decline) + " from the pre-war time.")
st.write("*Executive Summary*")
st.write(summary)
st.subheader("Humanitarian needs in Ukraine: Latest Estimation")
st.write("*Source*: Financial Tracking Service UN OCHA")
cmet0, cmet1, cmet2, cmet3 = st.columns(4)
cmet0.metric("Refugees, mn people", total_refugees)
cmet1.metric("Total needs, $ BN", hum_needs['Total'])
cmet2.metric("Funded needs $ BN", hum_needs['Funded'])
cmet3.metric("Requirements met", hum_needs['Requirements met'])
st.markdown("---")

st.write(intro1)
st.write(intro2)
st.write(intro3)

st.header("The immediate fallout; what we can (try to) measure so far")

st.write(fallout1)


st.altair_chart(refugee_chart, use_container_width=True)
st.plotly_chart(fig_hum_needs)
st.plotly_chart(fig_fx_uaheur, use_container_width=True)

st.write(fallout2)

col_rufm1, col_rufm2 = st.columns([1,1])
col_rufm1.plotly_chart(fig_fx_rubeur)
col_rufm2.plotly_chart(fig_bond_ru10de10)

components.iframe("https://datawrapper.dwcdn.net/MicOM/2/", height=800, scrolling=True)
components.iframe("https://datawrapper.dwcdn.net/ZVnMA/4/", height=800, scrolling=True)
components.iframe("https://datawrapper.dwcdn.net/17yDJ/2/", height=800, scrolling=True)
components.iframe("https://datawrapper.dwcdn.net/EQ9IF/3/", height=800, scrolling=True)

st.write(fallout3)

col_ceefx1, col_ceefx2, col_ceefx3 = st.columns([1,1,1])
col_ceefx1.plotly_chart(fig_fx_plnusd)
col_ceefx2.plotly_chart(fig_fx_czkusd)
col_ceefx3.plotly_chart(fig_fx_hufusd)

st.header("Impact on the global markets")

st.write(fallout4)
col_comm11, col_comm12 = st.columns([1,1])
col_comm11.plotly_chart(fig_comm_oil, width = 500)
col_comm12.plotly_chart(fig_comm_gas, width = 500)

st.write(fallout5)
col_comm21, col_comm22 = st.columns(2)
col_comm21.plotly_chart(fig_comm_gold)
col_comm22.plotly_chart(fig_comm_copper)

st.write(fallout6)
col_comm31, col_comm32 = st.columns(2)
col_comm31.plotly_chart(fig_comm_wheat)
col_comm32.plotly_chart(fig_comm_sugar)

st.header("Structural changes and Grand Politics")
st.image(link_img, caption="Votes in favor of the UN Resolution condemning Russian invastion in Ukraine. Source: The Economist")
st.write(fallout7)
st.write(fallout8)
st.write(fallout9)
st.write(fallout10)
st.write(fallout11)
st.write(fallout12)
# st.write("Russian currency lost " + str(fx_drop) + " against EUR since February 18th, 2022. This is " + str(fx_decline) + " devaluation compared to the pre-war value.")
# st.line_chart(df_fx_ru)