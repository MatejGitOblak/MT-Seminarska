from dash import Dash, html, dcc, dash, Input, Output, State
import dash_bootstrap_components as dbc
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
import geopandas as gpd
import json
import numpy as np
import geojson
from functions1 import *
import copy
import plotly.graph_objects as go

izbrana_obcina = 'Ljubljana'
ime_obcina1 = 'Ljubljana'
ime_obcina2 = 'Ljubljana'

odjemalci_dict = load_and_preprocess_odjemalci()
dejavnosti_dict = load_and_preprocess_dejavnosti()

map_df = odjemalci_dict['df_map']

map_df["Poraba"] = odjemalci_dict['gospodinjstvo_norm']['Poraba']

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
        geo=dict(bgcolor= 'rgba(0,0,0,0)'),
        )

obcina1 = px.choropleth(map_df.loc[map_df["District"] == "Ljubljana"],
                    geojson=data, 
                    color="Poraba", 
                    locations="District", 
                    featureidkey="properties.District",
                    color_continuous_scale="Sunsetdark"
                   )
obcina1.update_geos(fitbounds="locations", visible=False)
obcina1.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        geo=dict(bgcolor= 'rgba(0,0,0,0)'),
        coloraxis_showscale=False,)

obcina2 = px.choropleth(map_df.loc[map_df["District"] == "Ljubljana"],
                    geojson=data, 
                    color="Poraba", 
                    locations="District", 
                    featureidkey="properties.District",
                    color_continuous_scale="Sunsetdark"
                   )
obcina2.update_geos(fitbounds="locations", visible=False)
obcina2.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        geo=dict(bgcolor= 'rgba(0,0,0,0)'),
        coloraxis_showscale=False,)

d = {'Vrsta': ["Gospodinjstvo", "industrija"],
        'Poraba v MWh': [
        odjemalci_dict['gospodinjstvo']['Poraba'].loc[odjemalci_dict['gospodinjstvo']['OBČINE'] == 'Ljubljana'].values[0]/1000,
        odjemalci_dict['industrija']['Poraba'].loc[odjemalci_dict['industrija']['OBČINE'] == 'Ljubljana'].values[0]/1000
        ]}
df = pd.DataFrame(data=d)

fig2 = px.bar(df, x='Poraba v MWh', y='Vrsta', title='Ljubljana', orientation='h')

fig2.update_layout(
    xaxis_tickformat =',d',
)

def generate_list_item(obcina, gosp, ind):
    st = "Gospodinjstva: %.2f MWh" % float(gosp)
    st1 = "Industrija: %.2f MWh" % float(ind)
    return html.Div(className="obcina-div",
                    children=[
                                html.H3(obcina),
                                html.P(st),
                                html.P(st1)
                            ])

app = Dash(__name__)

app.layout = html.Div(className="main-div", children=[
    html.Div(className="div1", children=[
        html.Div(className="div1-izbira", children=[
            html.Button(id="podatki", className="podatki", children=["Izbor podatkov"]),
            html.Button(id="občine", className="občine", children=["Primerjava občin"]),
            html.Button(id="dejavnosti", className="dejavnosti", children=["Izbira dejavnosti"]),
        ]),
        html.Div(id="izbira-podatkov", className="izbira-podatkov", children=[
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
        ),
        html.Div(id="izbira-občine", className="izbira-občine", children=[
            html.H2("Primerjava občine"),
            dbc.RadioItems(
                    id='radio-občine',
                    options=[
                        {'label': 'Občina 1', 'value': 1},
                        {'label': 'Občina 2', 'value': 2}
                    ],
                    value=1,
                    inline=True
            )]
        ),
        html.Div(id="izbira-dejavnosti", className="izbira-dejavnosti", children=[
            html.H2("Izbira dejavnosti"),
            dbc.RadioItems(
                    id='radio-občine',
                    options=[
                        {'label': 'Občina 1', 'value': 1},
                        {'label': 'Občina 2', 'value': 2}
                    ],
                    value=1,
                    inline=True
            )]
        )
    ]),
    html.Div(className="div2", children=[
        html.Div("Statistični podatki"),
        html.Div(className="stat-podatki", children=[
            html.Div(className="stat-podatki1", children=[
                html.H4("Občina 1"),
                html.H6("Poraba: 40294kWh"),
                html.H6("Poraba/prebivalec: 544kWh")
            ]),
            html.Div(className="stat-podatki2", children=[
                html.H4("Občina 2"),
                html.H6("Poraba: 54294kWh"),
                html.H6("Poraba/previbalec: 724kWh")
            ])
        ])
    ]),
    html.Div(className="div3", children=[
        html.H3(id="obcina-ime1", children=["Ljubljana"]),
        dcc.Graph(className="graph1", id='graph1', figure=obcina1, config={'displayModeBar': False})
    ]),
    html.Div(className="div4", children=[
        html.H3(children=["Slovenija"]),
        dcc.Graph(className="graph", id='graph', figure=fig, config={'displayModeBar': False})
    ]),
    html.Div(className="div5", id='div5', children=[
        dcc.Graph(className="graph2", id='graph2', figure=fig2, config={'displayModeBar': False})
    ]),
    dbc.Card(className="obcine", children=[
        html.H4("OBČINE"),
        dbc.CardBody(className="obcine1", children=
        [
            html.Div(
                className="list-group",
                children=[generate_list_item(
                    list(odjemalci_dict['skupaj']['OBČINE'])[i], 
                    list(odjemalci_dict['gospodinjstvo']["Poraba"]/1000)[i], 
                    list(odjemalci_dict['industrija']["Poraba"]/1000)[i]
                    ) for i in range(len(list(odjemalci_dict['skupaj']['OBČINE'])))],
            ),
        ]
        ),
    ]),
    html.Div(className="div7", children=[
        html.H3(id="obcina-ime2", children=["Ljubljana"]),
        dcc.Graph(className="graph3", id='graph3', figure=obcina2, config={'displayModeBar': False})
    ])
])

@app.callback(
    [
        Output('graph2', 'figure'),
        Output('graph1', 'figure'),
        Output('graph3', 'figure'),
        Output('obcina-ime1', 'children'),
        Output('obcina-ime2', 'children')
    ],
    [
        Input('graph', 'clickData'),
        Input('radio-občine', 'value')
    ]
)

def do_smth(figure, radio):
    global obcina1, obcina2, izbrana_obcina, ime_obcina1, ime_obcina2
    
    if figure is not None:
        if figure['points'][0]['location'] != izbrana_obcina:
            if radio == 1:
                obcina1 = px.choropleth(map_df.loc[map_df["District"] == figure["points"][0]['location']],
                                    geojson=data, 
                                    color="Poraba", 
                                    locations="District", 
                                    featureidkey="properties.District",
                                    color_continuous_scale="Sunsetdark"
                                )
                obcina1.update_geos(fitbounds="locations", visible=False)
                obcina1.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        geo=dict(bgcolor= 'rgba(0,0,0,0)'),
                        coloraxis_showscale=False)

                ime_obcina1 = figure["points"][0]['location']

            if radio == 2:
                obcina2 = px.choropleth(map_df.loc[map_df["District"] == figure["points"][0]['location']],
                                    geojson=data, 
                                    color="Poraba", 
                                    locations="District", 
                                    featureidkey="properties.District",
                                    color_continuous_scale="Sunsetdark"
                                )
                obcina2.update_geos(fitbounds="locations", visible=False)
                obcina2.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        geo=dict(bgcolor= 'rgba(0,0,0,0)'),
                        coloraxis_showscale=False)

                ime_obcina2 = figure["points"][0]['location']

        d = {'Vrsta': ["Gospodinjstvo", "industrija"],
             'Poraba v MWh': [
                odjemalci_dict['gospodinjstvo']['Poraba'].loc[odjemalci_dict['gospodinjstvo']['OBČINE'] == figure["points"][0]['location']].values[0]/1000,
                odjemalci_dict['industrija']['Poraba'].loc[odjemalci_dict['industrija']['OBČINE'] == figure["points"][0]['location']].values[0]/1000
             ]}
        df = pd.DataFrame(data=d)

        fig2 = px.bar(df, x='Poraba v MWh', y='Vrsta', title=figure["points"][0]['location'], orientation='h')
        fig2.update_layout(
            xaxis_tickformat =',d',
        )
        izbrana_obcina = figure['points'][0]['location']
        return fig2, obcina1, obcina2, ime_obcina1, ime_obcina2
    else:
        return {}, obcina1, obcina2, ime_obcina1, ime_obcina2

@app.callback(
    [
        Output('izbira-podatkov', 'style'),
        Output('izbira-občine', 'style'),
        Output('izbira-dejavnosti', 'style'),
        Output('podatki', 'n_clicks'),
        Output('občine', 'n_clicks'),
        Output('dejavnosti', 'n_clicks')
    ],
    [
        Input('podatki', 'n_clicks'),
        Input('občine', 'n_clicks'),
        Input('dejavnosti', 'n_clicks')
    ]
)

def change_style(podatki, občine, dejavnosti):
    if podatki is not None:
        if podatki == 1:
            podatki = 0
            return {'display': 'inline-block'}, {'display': 'none'}, {'display': 'none'}, 0, 0, 0

    if občine is not None:
        if občine == 1:
            občine = 0
            return {'display': 'none'}, {'display': 'inline-block'}, {'display': 'none'}, 0, 0, 0

    if dejavnosti is not None:
        if dejavnosti == 1:
            dejavnosti = 0
            return {'display': 'none'}, {'display': 'none'}, {'display': 'inline-block'}, 0, 0, 0

    else:
        return {'display': 'inline-block'}, {'display': 'none'}, {'display': 'none'}, 0, 0, 0



if __name__ == '__main__':
    app.run_server(debug=True)