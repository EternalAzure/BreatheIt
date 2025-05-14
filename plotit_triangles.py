import os
import json
import time
from pprint import pprint
from typing import TypeAlias
from datetime import datetime
from urllib.request import urlopen

import numpy as np
import pandas as pd
import xarray as xr
import plotly.express as px
from scipy.spatial import Delaunay

px.colors

SIZE = 1000


def get_data_set(path:str) -> xr.Dataset:
    ds = xr.open_dataset(path, engine="netcdf4")
    return ds


def get_triangles(ds:xr.Dataset):
    longitudes = ds.variables["lon"].data.tolist()[:SIZE]
    latitudes = ds.variables["lat"].data.tolist()[:SIZE]
    coordinates = np.array(np.meshgrid(longitudes, latitudes)).T.reshape(-1, 2)
    tri = Delaunay(coordinates)
    triangles = [coordinates[simplex] for simplex in tri.simplices]
    return triangles


def calculate_partiles_in_triangle(ds:xr.Dataset, points:list):
    # NOTE We need to calculate indeces for fast data access
    point1 = points[0]
    point2 = points[1]
    point3 = points[2]
    #point1_lon_index = round(round(point1[0] -24.95) / 0.1) #NOTE Must round because python is inaccurate with floats
    #point1_lat_index = round(round(point1[1] -30.5) / 0.1)
    #point2_lon_index = round(round(point2[0] -24.95) / 0.1)
    #point2_lat_index = round(round(point2[1] -30.5) / 0.1)
    #point3_lon_index = round(round(point3[0] -24.95) / 0.1)
    #point3_lat_index = round(round(point3[1] -30.5) / 0.1)

    # Use indeces
    #measurement1 = float(ds.variables["pm2p5"][0][point1_lat_index][point1_lon_index].data)
    #measurement2 = float(ds.variables["pm2p5"][0][point2_lat_index][point2_lon_index].data)
    #measurement3 = float(ds.variables["pm2p5"][0][point3_lat_index][point3_lon_index].data)
    measurement1 = float(ds.sel({"lon":point1[0], "lat":point1[1], "time":ds.variables["time"][0]}, method="nearest").variables["pm2p5"].data)
    measurement2 = float(ds.sel({"lon":point2[0], "lat":point2[1], "time":ds.variables["time"][0]}, method="nearest").variables["pm2p5"].data)
    measurement3 = float(ds.sel({"lon":point3[0], "lat":point3[1], "time":ds.variables["time"][0]}, method="nearest").variables["pm2p5"].data)
    average = (measurement1+measurement2+measurement3) / 3
    return average

GeoJSON: TypeAlias = dict
Measurements: TypeAlias = list[list]
def get_geodata(ds:xr.Dataset, path:str) -> tuple[GeoJSON, Measurements]:
    if os.path.exists(path):
        print("Use existing geojson")
        with open(path, "r") as file:
            geojson:GeoJSON = json.load(file)
            data:Measurements = []
            for feature in geojson["features"]:
                id = feature["id"]
                avg = feature["properties"]["average"]
                data.append([id, avg])
            return geojson, data

    print("Create new geojson")
    triangles = get_triangles(ds)
    data:Measurements = []
    geojson:GeoJSON = {
        "type": "FeatureCollection",
        "features": []
    }
    start_time = time.perf_counter()
    for i, triangle in enumerate(triangles, 1):
        print(f"{i:03d}/{len(triangles)} {time.perf_counter()-start_time}sec", end="\r")

        id = str(i)
        points:list[float] = triangle.tolist()
        points = [[round(point[0], 2), round(point[1], 2)] for point in points]
        average = calculate_partiles_in_triangle(ds, points)

        # Add to geojson
        geojson["features"].append(
            {
                "id": id,
                "type": "Feature",
                "properties": {
                    "average": average
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [points]
                }
            }
        )

        # Add particles to data
        data.append([id, average])
    print(f"{i:03d}/{len(triangles)} {time.perf_counter()-start_time}sec")

    with open(path, "w") as file:
        file.write(json.dumps(geojson))

    return geojson, data


def show(df, geojson, locations, color):
    fig = px.choropleth_map(df, geojson=geojson, locations=locations, color=color,
                            #color_continuous_scale="Aggrnyl", # Eh
                            #color_continuous_scale="Agsunset", # Eh
                            #color_continuous_scale="Blackbody", # Surkea
                            #color_continuous_scale="Bluered", # Eh
                            #color_continuous_scale="Blugrn", # Eh
                            #color_continuous_scale="Bluyl", # Hyvä opacity 0.2
                            #color_continuous_scale="Brwnyl", # Hyvä opacity 0.1
                            #color_continuous_scale="Bugn", # Hyvä opacity 0.1
                            color_continuous_scale="Bupu", # Erinomainen opacity 0.15 color europe:5-30 finland: 2-5 uusimaa: 3-7 kairo: 30-90
                            #color_continuous_scale="Burg", #
                            #color_continuous_scale="Burgyl", #
                            #color_continuous_scale="Cividis", #
                            #color_continuous_scale="Darkmint", #
                            #color_continuous_scale="Electric", #
                            #color_continuous_scale="Emrld", #
                            #color_continuous_scale="Blues", # Hyvä opacity 0.3
                            #color_continuous_scale="Inferno", # Surke
                            #color_continuous_scale="Viridis", # Hyvä opacity 0.1
                            #color_continuous_scale="Edge", # Hyvä opacity 0.1-0.2
                            #color_continuous_scale="Phase", # Huono
                            range_color=(30, 90),
                            map_style="carto-positron",
                            zoom=3, center = {"lat": 55, "lon": 20},
                            opacity=0.4,
                            labels={'unemp':'unemployment rate'}
                            )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_traces(marker_line_width=0)
    fig.show()


def main():
    print(f"Started {datetime.now()}")

    print("Read dataset")
    filepath = "ab5fd25f378b5a07d5a21ddef29249af/cams.eaq.vra.ENSa.pm2p5.l0.2022-01.nc" # Dimensions:  (time: 744, lat: 420, lon: 700)
    dataset = get_data_set(filepath)

    print("Get geojson")
    geojson, data = get_geodata(dataset, "europe3.geo.json")

    df = pd.DataFrame(data, columns=["id", "pm2p5"])
    locations = [i for i in range(len(df))]
    color='pm2p5'

    print("Show map")
    show(df, geojson, locations, color)
    print(f"Ended {datetime.now()}")


if __name__ == "__main__":
    main()