from dash import Dash, html, dcc, dash, Input, Output, State
import dash_bootstrap_components as dbc
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
import geopandas as gpd
import json
import numpy as np
import geojson
from functions import *

df_odjemalci = pd.read_csv("data/podatki_vrsta_odjemalca.csv", delimiter=",", encoding="windows-1250")
df_izris = izrisi_odjemalci_Slovenija(df_odjemalci, 2020)
df_izris = df_izris.sort_index()

map_df = gpd.read_file('slovenija_map/obcine/obcine.shp')
map_df = map_df.to_crs("WGS84")
map_df = map_df.rename({'NAZIV': 'District'}, axis = 'columns')
map_df = map_df.drop(columns = ['EID_OBCINA',  'SIFRA', 'NAZIV_DJ', 'OZNAKA_MES', 'DATUM_SYS'])
map_df = map_df.sort_values('District')
map_df["Poraba"] = list(df_izris[0].values)
map_df = map_df.reset_index(drop=True)
map_df["geometry"] = (
    map_df.to_crs(map_df.estimate_utm_crs()).simplify(100).to_crs(map_df.crs)
)
map_df.to_file('slovenija_map/obcine/obcine.json', driver="GeoJSON") 
with open('slovenija_map/obcine/obcine.json', encoding="UTF-8") as f:
    data = json.load(f)

fig = px.choropleth(map_df,
                    geojson=data, 
                    color="Poraba", 
                    locations="District", 
                    featureidkey="properties.District",
                    color_continuous_scale="Sunsetdark",
                   )
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        geo=dict(bgcolor= 'rgba(0,0,0,0)'))

def generate_list_item(obcina):
    return html.Div(className="obcina-div",
                    children=[
                                html.H3(obcina),
                                html.P("info")
                            ])

li = list(df_izris.index)


app = Dash(__name__)

app.layout = html.Div(className="main-div", children=[
    html.Div(className="div1", children=[
        html.Div("div1")
    ]),
    html.Div(className="div2", children=[
        html.Div("div2")
    ]),
    html.Div(className="div3", children=[
        html.Div("div3")
    ]),
    html.Div(className="div4", children=[
        dcc.Graph(className="graph", figure=fig)
    ]),
    html.Div(className="div5", children=[
        html.Div("div5")
    ]),
    dbc.Card(className="obcine", children=[
        html.H4("OBČINE"),
        dbc.CardBody(className="obcine1", children=
        [
            html.Div(
                className="list-group",
                children=[generate_list_item(i) for i in li],
            ),
        ]
        ),
    ]),
    html.Div(className="div7", children=[
        html.Div("div7")
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)