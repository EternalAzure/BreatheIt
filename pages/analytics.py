import pandas as pd
from datetime import datetime
import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px


dash.register_page(__name__)

layout = html.Div([
    html.H4('PM10 Air pollution in cities'),
    dcc.Graph(id="city_line_chart"),
    dcc.Checklist(
        id="checklist",
        options=["Venice", "Helsinki", "Paris", "Europe"],
        value=["Venice"],
        inline=True
    ),
])


@callback(
    Output("city_line_chart", "figure"),
    Input("checklist", "value"))
def update_line_chart(continents):
    df:pd.DataFrame = px.data.gapminder() # replace with your own data source
    get_dataframe(ForecastQuery(
        "PM10",
        time=datetime(2025, 5, 10, 0, 0),
        leadtime=23,
        model=None,
        limits={"north": 47, "south": 43, "west": 9, "east": 14}
    ))
    #df_f = df[df["year"] > 1960 ]
    #df_f = df_f[df_f['year'] < 1980]
    #breakpoint()
    fig = px.line(df,
        x="leadtime", y="value", color='datetime')
    return fig

update_line_chart("m")