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
df_izris = izrisi_odjemalci_gospodinjstva(df_odjemalci, 2020)
df_izris = df_izris.sort_index()

map_df = gpd.read_file('slovenija_map/obcine/obcine.shp')
map_df = map_df.to_crs("WGS84")
map_df = map_df.rename({'NAZIV': 'District'}, axis = 'columns')
map_df = map_df.drop(columns = ['EID_OBCINA',  'SIFRA', 'NAZIV_DJ', 'OZNAKA_MES', 'DATUM_SYS'])
map_df = map_df.sort_values('District')

map_df["Poraba"] = list(df_izris[0].values)

norm_poraba_gosp = izracun_normalizacije_gospodinjstva(map_df, 2021)
norm_poraba_ind = izracun_normalizacije_poslovni_objekti(map_df, 2021)
norm_poraba_slo = izracun_normalizacije_Slovenija(map_df, 2021)

map_df["Poraba"] = norm_poraba_gosp["Poraba"]

map_df['District'] = df_izris.index


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

fig1 = px.choropleth(map_df.loc[map_df["District"] == "Ljubljana"],
                    geojson=data, 
                    color="Poraba", 
                    locations="District", 
                    featureidkey="properties.District",
                    color_continuous_scale="Sunsetdark"
                   )
fig1.update_geos(fitbounds="locations", visible=False)
fig1.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        geo=dict(bgcolor= 'rgba(0,0,0,0)'),
        coloraxis_showscale=False)

def generate_list_item(obcina, gosp, ind):
    st = "Gospodinjstva: %.2f Industrija: %.2f" % (float(gosp), float(ind))
    return html.Div(className="obcina-div",
                    children=[
                                html.H3(obcina),
                                html.P(st)
                            ])

li1 = list(df_izris.index)
li2 = list(norm_poraba_ind["Poraba"])
li3 = list(norm_poraba_gosp["Poraba"])

app = Dash(__name__)

app.layout = html.Div(className="main-div", children=[
    html.Div(className="div1", children=[
        html.Div(children=[
            html.H2("Izbor podatkov"),
            dbc.RadioItems(
                    id='radio',
                    options=[
                        {'label': 'Vrsta odjemalca', 'value': 1},
                        {'label': 'Vrsta dejavnosti', 'value': 2}
                    ],
                    value=1,
                    inline=True
            )]
        )
    ]),
    html.Div(className="div2", children=[
        html.Div("div2")
    ]),
    html.Div(className="div3", children=[
        dcc.Graph(className="graph1", id='graph1', figure=fig1, config={'displayModeBar': False})
    ]),
    html.Div(className="div4", children=[
        dcc.Graph(className="graph", id='graph', figure=fig, config={'displayModeBar': False})
    ]),
    html.Div(className="div5", id='div5', children=[
        dcc.Graph(className="graph2", id='graph2', figure={}, config={'displayModeBar': False})
    ]),
    dbc.Card(className="obcine", children=[
        html.H4("OBČINE"),
        dbc.CardBody(className="obcine1", children=
        [
            html.Div(
                className="list-group",
                children=[generate_list_item(li1[i], li2[i], li3[i]) for i in range(len(li1))],
            ),
        ]
        ),
    ]),
    html.Div(className="div7", children=[
        html.Div("div7")
    ])
])

@app.callback(
    [
        Output('graph2', 'figure'),
        Output('graph1', 'figure'),
    ],
    Input('graph', 'clickData')
)

def do_smth(figure):
    global fig1
    if figure is not None:
        fig1 = px.choropleth(map_df.loc[map_df["District"] == figure["points"][0]['location']],
                            geojson=data, 
                            color="Poraba", 
                            locations="District", 
                            featureidkey="properties.District",
                            color_continuous_scale="Sunsetdark"
                        )
        fig1.update_geos(fitbounds="locations", visible=False)
        fig1.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                geo=dict(bgcolor= 'rgba(0,0,0,0)'),
                coloraxis_showscale=False)

        d = {'Vrsta': ["Gospodinjstvo", "industrija"],
             'Poraba v MWh': [
                izrisi_odjemalci_Slovenija(df_odjemalci, 2020)[0][figure["points"][0]['location']]/1000,
                izrisi_odjemalci_poslovni_objekti(df_odjemalci, 2020)[0][figure["points"][0]['location']]/1000
             ]}
        df = pd.DataFrame(data=d)

        fig2 = px.bar(df, x='Poraba v MWh', y='Vrsta', title=figure["points"][0]['location'], orientation='h')
        return fig2, fig1
    else:
        return {}, fig1

if __name__ == '__main__':
    app.run_server(debug=True)