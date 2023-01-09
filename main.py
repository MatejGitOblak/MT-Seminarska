from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import json
from functions1 import *

clicked_obcina = 'Ljubljana'
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

bar_fig_left = px.bar(df, x='Poraba v MWh', y='Vrsta', title='Ljubljana', orientation='h')

bar_fig_left.update_layout(
    xaxis_tickformat =',d',
)

bar_fig_right = px.bar(df, x='Poraba v MWh', y='Vrsta', title='Ljubljana', orientation='h')

bar_fig_right.update_layout(
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
        html.Div(id="izbira-dejavnosti", className="izbira-dejavnosti", children=[
            html.H2("Izbira dejavnosti"),
            dcc.Checklist(
                className="checklist",
                id="checklist",
                options=list(dejavnosti_dict.keys())
            )]
        )
    ]),
    html.Div(className="div2", children=[
        html.H4("Najdi občino"),
        html.H5("OBČINA 1"),
        dcc.Dropdown(
            className="dropdown1",
            options=list(odjemalci_dict['skupaj']['OBČINE']),
            id = 'dropdown1',),
        html.H5("OBČINA 2"),
        dcc.Dropdown(
            className="dropdown1",
            options=list(odjemalci_dict['skupaj']['OBČINE']),
            id = 'dropdown2',)
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
        dcc.Graph(className="graph2", id='bar_graph_left', figure=bar_fig_left, config={'displayModeBar': False}),
        dcc.Graph(className="graph2_2", id='bar_graph_right', figure=bar_fig_right, config={'displayModeBar': False})
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
        Output('bar_graph_left', 'figure'),
        Output('graph1', 'figure'),
        Output('graph3', 'figure'),
        Output('obcina-ime1', 'children'),
        Output('obcina-ime2', 'children'),
        Output('graph', 'figure'),
        Output('bar_graph_right', 'figure'),
    ],
    [
        Input('checklist', 'value'),
        Input('radio', 'value'),
        Input('dropdown1', 'value'),
        Input('dropdown2', 'value')
    ]
)

def do_smth(checklist, radio_odjemalci, drop1, drop2):
    global obcina1, obcina2, izbrana_obcina, ime_obcina1, ime_obcina2, odjemalci_dict, map_df, data, fig
    global clicked_obcina, bar_fig_right, bar_fig_left
    if radio_odjemalci == 1:
        if drop1 is not None:
            obcina1 = px.choropleth(map_df.loc[map_df["District"] == drop1],
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
                    
            d = {'Vrsta': ["Gospodinjstvo", "industrija"],
                'Poraba v MWh': [
                    odjemalci_dict['gospodinjstvo']['Poraba'].loc[odjemalci_dict['gospodinjstvo']['OBČINE'] == drop1].values[0]/1000,
                    odjemalci_dict['industrija']['Poraba'].loc[odjemalci_dict['industrija']['OBČINE'] == drop1].values[0]/1000
                ]}
            df = pd.DataFrame(data=d)

            bar_fig_left = px.bar(df, x='Poraba v MWh', y='Vrsta', title=drop1, orientation='h')
            bar_fig_left.update_layout(
                xaxis_tickformat =',d',
            )

            ime_obcina1 = drop1

        if drop2 is not None:
            obcina2 = px.choropleth(map_df.loc[map_df["District"] == drop2],
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

            ime_obcina2 = drop2

            d = {'Vrsta': ["Gospodinjstvo", "industrija"],
                'Poraba v MWh': [
                    odjemalci_dict['gospodinjstvo']['Poraba'].loc[odjemalci_dict['gospodinjstvo']['OBČINE'] == drop2].values[0]/1000,
                    odjemalci_dict['industrija']['Poraba'].loc[odjemalci_dict['industrija']['OBČINE'] == drop2].values[0]/1000
                ]}
            df = pd.DataFrame(data=d)

            bar_fig_right = px.bar(df, x='Poraba v MWh', y='Vrsta', title=drop2, orientation='h')
            bar_fig_right.update_layout(
                xaxis_tickformat =',d',
            )

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
        return bar_fig_left, obcina1, obcina2, ime_obcina1, ime_obcina2, fig, bar_fig_right
    elif radio_odjemalci == 2 and checklist is not None and checklist != []:
        map_df = odjemalci_dict['df_map']

        map_df["Poraba"] = calculate_sums_dejavnosti(checklist, dejavnosti_dict)

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


        obcina1 = px.choropleth(map_df.loc[map_df["District"] == drop1],
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

        ime_obcina1 = drop1


        obcina2 = px.choropleth(map_df.loc[map_df["District"] == drop2],
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

        ime_obcina2 = drop2

        list_1 = []

        for dejavnost in checklist:
            list_1.append(dejavnosti_dict[dejavnost].loc[dejavnosti_dict[dejavnost]['OBČINE'] == drop1]['Poraba'].values[0]/1000)

        d = {'Vrsta': checklist,
             'Poraba v MWh': list_1}
        df = pd.DataFrame(data=d)

        bar_fig_left = px.bar(df, x='Poraba v MWh', y='Vrsta', title=drop1, orientation='h')
        bar_fig_left.update_layout(
            xaxis_tickformat =',d',
        )

        list_2 = []

        for dejavnost in checklist:
            list_2.append(dejavnosti_dict[dejavnost].loc[dejavnosti_dict[dejavnost]['OBČINE'] == drop2]['Poraba'].values[0]/1000)

        d = {'Vrsta': checklist,
             'Poraba v MWh': list_2}
        df = pd.DataFrame(data=d)

        bar_fig_right = px.bar(df, x='Poraba v MWh', y='Vrsta', title=drop2, orientation='h')
        bar_fig_right.update_layout(
            xaxis_tickformat =',d',
        )
        return bar_fig_left, obcina1, obcina2, ime_obcina1, ime_obcina2, fig, bar_fig_right
    else:
        return bar_fig_left, obcina1, obcina2, ime_obcina1, ime_obcina2, fig, bar_fig_right

@app.callback(
    [
        Output('izbira-podatkov', 'style'),
        Output('izbira-dejavnosti', 'style'),
        Output('podatki', 'n_clicks'),
        Output('dejavnosti', 'n_clicks')
    ],
    [
        Input('podatki', 'n_clicks'),
        Input('dejavnosti', 'n_clicks')
    ]
)

def change_style(podatki, dejavnosti):
    if podatki is not None:
        if podatki == 1:
            podatki = 0
            return {'display': 'inline-block'}, {'display': 'none'}, 0, 0

    if dejavnosti is not None:
        if dejavnosti == 1:
            dejavnosti = 0
            return {'display': 'none'}, {'display': 'inline-block'}, 0, 0

    else:
        return {'display': 'inline-block'}, {'display': 'none'}, 0, 0

if __name__ == '__main__':
    app.run_server(debug=True)