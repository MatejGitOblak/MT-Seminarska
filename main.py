from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import geopandas as gpd



app = Dash(__name__)

app.layout = html.Div(children=[
])

if __name__ == '__main__':
    app.run_server(port=9001, debug=True)