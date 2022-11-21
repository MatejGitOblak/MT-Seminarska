from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import geopandas as gpd

slovenia = gpd.read_file('slovenija_map/obcine/obcine.shp', encoding='cp1250')

app = Dash(__name__)

app.layout = html.Div(children=[
])

if __name__ == '__main__':
    app.run_server(port=9001, debug=True)