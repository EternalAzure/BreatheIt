import os
import json
import glob
import sqlite3
import pandas as pd
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import TypeAlias, Literal, Optional


@dataclass
class ForecastQuery:
    variable: Literal['PM2.5'
                    'PM2.5 Nitrate'
                    'PM2.5 Sulphate'
                    'PM2.5 REC'
                    'PM2.5 TEC'
                    'PM2.5 SIA'
                    'PM2.5 TOM'
                    'PM10'
                    'PM10 Dust'
                    'PM10 Salt'
                    'NH3'
                    'CO'
                    'HCHO'
                    'OCHCHO'
                    'NO2'
                    'VOCs'
                    'O3'
                    'NO + NO2'
                    'SO2'
                    'Alder pollen'
                    'Birch pollen'
                    'Grass pollen'
                    'Mugwort pollen'
                    'Olive pollen'
                    'Ragweed pollen']
    time: datetime
    leadtime: int
    model: Optional[str]

@dataclass
class AnalysisQuery:
    variable: Literal['PM2.5'
                    'PM2.5 Nitrate'
                    'PM2.5 Sulphate'
                    'PM2.5 REC'
                    'PM2.5 TEC'
                    'PM2.5 SIA'
                    'PM2.5 TOM'
                    'PM10'
                    'PM10 Dust'
                    'PM10 Salt'
                    'NH3'
                    'CO'
                    'HCHO'
                    'OCHCHO'
                    'NO2'
                    'VOCs'
                    'O3'
                    'NO + NO2'
                    'SO2'
                    'Alder pollen'
                    'Birch pollen'
                    'Grass pollen'
                    'Mugwort pollen'
                    'Olive pollen'
                    'Ragweed pollen']
    start_time: datetime
    end_time: datetime


GeoJSON: TypeAlias = dict
Measurements: TypeAlias = list[list]
def for_plotly_choropleth_map(geojson_path:str):
    """Deprecated"""
    if os.path.exists(geojson_path):
        with open(geojson_path, "r") as file:
            geojson:GeoJSON = json.load(file)
            data:Measurements = []
            for feature in geojson["features"]:
                id = feature["id"]
                value = feature["properties"]["measurement"]
                data.append([id, value])
            return geojson, data

    print(f"No files found with {geojson_path=}")
    print(f"Here is a list of existing geojsons:")
    geojsons = glob.glob("data/geojson/*.geo.json")
    for file in geojsons:
        print(file)
    raise ValueError(f"No files found with {geojson_path=}")


def query_forecast(query:ForecastQuery):
    leadtime = query.time + timedelta(hours=query.leadtime)
    with sqlite3.connect("AirQuality.db") as conn:
        cursor = conn.cursor()
        parameters = {
            "variable": query.variable,
            "datetime": query.time.strftime("%Y/%m/%d %H:%M"), 
            "leadtime": leadtime.strftime("%Y/%m/%d %H:%M"), 
            "model": query.model
        }
        if not query.model:
            parameters.pop("model")
            sql = f"""
                SELECT variable_name, value, lon, lat, leadtime 
                FROM forecasts 
                WHERE variable_name=:variable AND datetime=:datetime AND leadtime<=:leadtime
            """
        else:
            sql = f"""
                SELECT variable_name, value, lon, lat, leadtime 
                FROM forecasts 
                WHERE variable_name=:variable AND datetime=:datetime AND leadtime<=:leadtime AND model=:model
            """
        results = cursor.execute(sql, parameters).fetchall()
        df = pd.DataFrame(results, columns=["variable", "value", "lon", "lat", "leadtime"])
        df['id'] = df.apply(lambda row: f"[{row['lon']}, {row['lat']}]", axis=1)
        df = df[['id'] + [col for col in df.columns if col != 'id']]
        return df


def query_analysis(query:AnalysisQuery):
    pass


def get_dataframe(query:ForecastQuery|AnalysisQuery):
    if isinstance(query, ForecastQuery):
        return query_forecast(query)
    elif isinstance(query, AnalysisQuery):
        return query_analysis(query)
    raise ValueError(f"Query must be instance of either {ForecastQuery.__name__} or {AnalysisQuery.__name__}")


GeoJSON: TypeAlias = dict
def get_geojson(geojson_path:str):
    if os.path.exists(geojson_path):
        with open(geojson_path, "r") as file:
            geojson:GeoJSON = json.load(file)
            return geojson

    print(f"No files found with {geojson_path=}")
    print(f"Here is a list of existing geojsons:")
    geojsons = glob.glob("data/geojson/*.geo.json")
    for file in geojsons:
        print(file)
    raise ValueError(f"No files found with {geojson_path=}")