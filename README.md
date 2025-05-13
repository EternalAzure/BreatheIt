# COPERNICUS DATA

This is a collection of tools to download and show Copernius satellite data.

Create or reset sqlite3 database with reset_db.ps1

## Load nc-files
Download netcdf files with loadit.py

You need to write a request for the script. Use Download tab on ads [website](https://ads.atmosphere.copernicus.eu/datasets/cams-europe-air-quality-forecasts?tab=download) to generate request. Like this:

```
# loadit.py
dataset = "cams-europe-air-quality-forecasts"
request = {
    "variable": ["particulate_matter_10um"],
    "model": ["ensemble"],
    "level": ["0"],
    "date": ["2025-05-10/2025-05-10"],
    "type": ["forecast"],
    "time": ["00:00"],
    "leadtime_hour": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", 
                        "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24"],
    "data_format": "netcdf_zip"
}
```
The script will create subfolder into data/netcdf for dataset and create descriptive name for the file.


## Build sql database
Create database by running reset_db.ps1. It creates neccessary tables into db and populates them. 

Parse nc-files into sql database with dibit.py. Give nc file as commandline argument like so ```py dibit.py EU-forecast-PM10-2025-05-10-24/ENS_FORECAST.nc```. Don't worry, the text client will guide you.

You can observe database with sqlite3 client. Run ```sqlite3 AirQuality.db``` in terminal to open db connection. ```.quit``` exits.

## Create geojson from nc-file
Create geojson from nc file with ```mapit.py```. As long as coordinate system is same, this needs ne be done only once. I have already included ```europe.forecast.geo.json``` into data-folder. It can be cropped into smaller pieces.

## Crop geojsons
Ploting large datasets is computationally intensive and cropping geojsons into smaller pieces may help. Use ```cropit.py``` to crop geojsons to fit west, east, north and south limits.

## Plot data
Show Choroplethmap with ```plotit.py``` or use ```app.py```. Both do the same thing but ```app.py``` is Dash version.

## NC vs DB
NC-files are like small databases. Variables data is accessed through dimensions. File ```geodata.py``` has function ```query_forecast_nc()``` that demonstrates how. To use nc files efficiently it is neccessary to know how to use numpy and xarray libraries. NC-files have their dimensions sorted which makes accessing data via index possible and easy.

SQL database can hold more data and can combine data from multiple files. One draw back is that transferring data into db will take long time. Even 68min for one hour of Europe wide forecasts. That means by the time we have transferred 24h forecast into db, a whole day might have passed. Speed will vary by technique, computer, dataset and technology. Sqlite3 may not be the fastest.