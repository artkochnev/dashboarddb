import pydeck as pdk
import pandas as pd
from gdeltdoc import GdeltDoc, Filters

link_casualties = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQIdedbZz0ehRC0b4fsWiP14R7MdtU1mpmwAkuXUPElSah2AWCURKGALFDuHjvyJUL8vzZAt3R1B5qg/pub?output=csv"
link_idps = "https://data.humdata.org/visualization/ukraine-humanitarian-operations/data/idps.csv"
link_hostilities = "https://data.humdata.org/visualization/ukraine-humanitarian-operations/data/hostilities.geojson"
link_all = "https://raw.githubusercontent.com/OCHA-DAP/hdx-scraper-ukraine-viz/main/all.json"

#Cols to convert to values
def get_idps(link):
    df = pd.read_csv(link)
    idps = df['IDP estimation'].sum()
    num_cols = ['X Longitude', 'Y Latitude', 'IDP estimation', 'Population']
    for c in num_cols:
        df[c] = pd.to_numeric(df[c])
    df_regions = df.groupby(['admin1Name_eng']).sum()
    df = df[num_cols]
    df.columns = ['long', 'lat', 'idp', 'population']
    output = {'df': df, 'df regs': df_regions, 'idps': idps}
    return output

output = get_idps(link_idps)['df regs']
print(output)
# df = output['df']
# token = 'pk.eyJ1IjoiYXJ0ZW0ta29jaG5ldiIsImEiOiJjbDBwczhhMmQyMjc3M2ltOXZteGxkeTRyIn0.jS7sRmqp68P5NZj6mkKazQ'

# r = pdk.Deck(
#     map_style='mapbox://styles/mapbox/light-v9',
#     initial_view_state=pdk.ViewState(
#         latitude=49,
#         longitude=31,
#         zoom=5,
#         pitch=0,
#     ),
#     mapbox_key=token,
#     layers=[
#         pdk.Layer(
#             "ScatterplotLayer",
#             data=df,
#             get_position=['long', 'lat'],
#             #get_weigth = 'idp',
#             get_radius='idp',
#             radius_min_pixels=1,
#             radius_max_pixels=20,
#             get_fill_color=[255, 140, 0],
#             get_line_color=[0, 0, 0],
#             opacity = 0.4,
#             stroked=True,
#             filled=True,
#             pickable=True
#         )
#     ]
# )

