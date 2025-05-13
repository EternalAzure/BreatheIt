import pandas as pd
from datetime import datetime

import plotly
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, State

import geodata
from geodata import ForecastQuery, AnalysisQuery, GeoJSON


app = Dash(__name__)

app.layout = html.Div([
    #html.H4('PM10 particles in air'),
    html.P("Select a region:"),
    dcc.RadioItems(
        id='region',
        options=["North", "West", "East", "South", "Venice"],
        value="Venice",
        inline=True
    ),
    dcc.Graph(id="graph"),
])

def get_geojson(region) -> GeoJSON:
    match region:
        case "Europe":
            geojson_path = f"data/geojson/europe.forecast.geo.json"
        case "North":
            geojson_path = f"data/geojson/north-eu.forecast.geo.json"
        case "West":
            geojson_path = f"data/geojson/west-eu.forecast.geo.json"
        case "East":
            geojson_path = f"data/geojson/east-eu.forecast.geo.json"
        case "South":
            geojson_path = f"data/geojson/south-eu.forecast.geo.json"
        case "Venice":
            geojson_path = f"data/geojson/venize.forecast.geo.json"
        case _:
            geojson_path = f"data/geojson/venice.forecast.geo.json"
    return geodata.get_geojson(geojson_path)


def animated_map_figure(variable:str, geojson:GeoJSON):
    df:pd.DataFrame = geodata.get_dataframe(ForecastQuery(
        variable=variable,
        time=datetime(2025, 5, 10, 0, 0),
        leadtime=22,
        model=None,
        limits=geojson["limits"]
    ))
    locations = df.iloc[:, 0].tolist() # All ids aka every row of first column
    color_max = min(df.iloc[:,1].max(), 30)
    fig = px.choropleth_map(
        df,
        geojson,
        locations=locations,
        color="value",
        range_color=[2, color_max],
        color_continuous_scale="Bupu",
        opacity=0.3,
        animation_frame="leadtime"
    )
    fig.update_layout(map_zoom=6)
    return fig


def map_figure(variable, geojson:GeoJSON):
    df:pd.DataFrame = geodata.get_dataframe(ForecastQuery(
        variable=variable,
        time=datetime(2025, 5, 10, 0, 0),
        leadtime=0,
        model=None,
        limits=geojson["limits"]
    ))
    locations = df.iloc[:, 0].tolist() # All ids aka every row of first column
    color_max = min(df.iloc[:,1].max(), 30)
    fig = px.choropleth_map(
        df,
        geojson,
        locations=locations,
        color="value",
        range_color=[2, color_max],
        color_continuous_scale="Bupu",
        opacity=0.3
    )
    fig.update_layout(map_zoom=3)
    return fig



@app.callback(
    Output('graph', 'figure'),
    Input('region', 'value'),
    prevent_initial_call=False
)
def display_choropleth(region:str):
    variable="PM10"
    geojson = get_geojson(region)
    
    fig:go.Figure=None
    if region == "Venice":
        fig = animated_map_figure(variable, geojson)
    else:
        fig = map_figure(variable, geojson)

    fig.update_geos(projection_type="natural earth")
    fig.update_layout(
        map_style="carto-positron",
        map_center=geojson["center"],
        margin={"r":0,"t":25,"l":0,"b":0}, 
        title_text=f"{variable} forecast",
        height=700)
    fig.update_traces(marker_line_width=0)

    return fig



app.run(debug=True)