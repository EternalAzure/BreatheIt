import os
import json
import time
import glob
from pathlib import Path
from pprint import pprint
from typing import TypeAlias
from datetime import datetime
from argparse import ArgumentParser

import numpy as np
import pandas as pd
import xarray as xr
import plotly.express as px





def _get_data_set(path:str) -> xr.Dataset:
    ds = xr.open_dataset(path, engine="netcdf4")
    return ds


def get_squares(ds:xr.Dataset) -> list[list]:
    """Creates new coordinates to make squares around original points."""
    longitudes = ds.variables["longitude"].data.tolist()
    latitudes = ds.variables["latitude"].data.tolist()
    coordinates = np.array(np.meshgrid(longitudes, latitudes)).T.reshape(-1, 2)

    squares = []
    for point in coordinates:
        lon, lat = point
        lon = float(lon)
        lat = float(lat)
        north_east = (round(lon + 0.05, 2),  round(lat + 0.05, 2))
        south_east = (round(lon + 0.05, 2),  round(lat - 0.05, 2))
        south_west = (round(lon - 0.05, 2),  round(lat - 0.05, 2))
        nort_west  = (round(lon -0.05, 2),   round(lat + 0.05, 2))
        squares.append([point.tolist(), [north_east, south_east, south_west, nort_west]])

    return squares


def calculate_particles(ds:xr.Dataset, point:list, variable_name:str):
    """Variable name eg. pm2p5"""
    # Etsii sel() funktiolla partikkelien määrän ensimmäisenä tuntina annetussa sijainnissa
    measurement = float(ds.sel({"longitude":point[0], "latitude":point[1], "time":ds.variables["time"][0]}, method="nearest").variables[variable_name].data)
    return measurement


GeoJSON: TypeAlias = dict
Measurements: TypeAlias = list[list]
def _get_geodata(ds:xr.Dataset, variable_name:str) -> GeoJSON:
    print("Creating new geojson...")
    shapes = get_squares(ds)

    geojson:GeoJSON = { # sijainnit id:llä
        "type": "FeatureCollection",
        "features": []
    }
    start_time = time.perf_counter()
    idx = 0
    for centroid, boundary in shapes:
        idx += 1
        print(f"{idx:03d}/{len(shapes)} {time.perf_counter()-start_time}sec", end="\r")
        measurement = calculate_particles(ds, centroid, variable_name)
        centroid = [round(centroid[0], 2), round(centroid[1], 2)]
        # Add to geojson
        geojson["features"].append(
            {
                "id": str(centroid), # NOTE 
                "type": "Feature",
                "properties": {
                    "measurement": measurement # Tallennetaan arvo ettei sitä tarvitse laskea uudestaan
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [boundary], # Plotly piirtää kuviot näiden perusteella
                    "centroid": centroid # Keskipiste debuggaamista varten
                }
            }
        )
    print(f"{idx:03d}/{len(shapes)} {time.perf_counter()-start_time}sec")

    return geojson



def from_forecast(origin:str, target:str):
    print("Reading dataset...")
    dataset:xr.Dataset = _get_data_set(origin)

    print("Getting geojson...")
    geojson = _get_geodata(dataset, "pm10_conc")

    print("Writing geojson...")
    with open(target, "w") as file:
        file.write(json.dumps(geojson))

    print("Done.")
    

