from pprint import pprint
from datetime import datetime

import pandas as pd
import plotly.express as px

import geodata
from geodata import ForecastQuery, AnalysisQuery



def show(df, geojson, locations, color):
    color_max = min(df.iloc[:,2].max(), 40)
    fig = px.choropleth_map(df, geojson=geojson, locations=locations, color=color,
                            #color_continuous_scale="Aggrnyl", # Eh
                            #color_continuous_scale="Agsunset", # Eh
                            #color_continuous_scale="Blackbody", # Surkea
                            #color_continuous_scale="Bluered", # Eh
                            #color_continuous_scale="Blugrn", # Eh
                            #color_continuous_scale="Bluyl", # Hyvä
                            #color_continuous_scale="Brwnyl", # Hyvä
                            #color_continuous_scale="Bugn", # Hyvä
                            color_continuous_scale="Bupu", # Erinomainen
                            #color_continuous_scale="Burg", #
                            #color_continuous_scale="Burgyl", #
                            #color_continuous_scale="Cividis", #
                            #color_continuous_scale="Darkmint", #
                            #color_continuous_scale="Electric", #
                            #color_continuous_scale="Emrld", #
                            #color_continuous_scale="Blues", # Hyvä
                            #color_continuous_scale="Inferno", # Surke
                            #color_continuous_scale="Viridis", # Hyvä
                            #color_continuous_scale="Edge", # Hyvä
                            #color_continuous_scale="Phase", # Huono
                            range_color=(2, color_max), # NOTE Partikkeleiden raja-arvot väritystä varten
                            map_style="carto-positron",
                            zoom=3, center = {"lat": 55, "lon": 20},
                            opacity=0.3,
                            labels={'value':'µg/m3'},
                            title=df["variable"][0],
                            animation_frame="leadtime"
                            )
    fig.update_layout(margin={"r":0,"t":25,"l":0,"b":0}, title_text=f"{df['variable'][0]} {min(df['leadtime'])}-{max(df['leadtime'])}")
    fig.update_traces(marker_line_width=0)
    fig.show()


def main():
    print("Get geojson")
    geojson_path = "data/geojson/forecast_pm10.geo.json"
    geojson = geodata.get_geojson(geojson_path)
    df:pd.DataFrame = geodata.get_dataframe(ForecastQuery(
        variable="PM10",
        time=datetime(2025, 5, 10, 0, 0),
        leadtime=23,
        model=None
    ))
    
    locations = df.iloc[:, 0].tolist() # All ids aka every row of first column
    color='value'

    print("Show map")
    show(df, geojson, locations, color)



if __name__ == "__main__":
    main()