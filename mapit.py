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

import create_geojson


def find_file(filename:str) -> Path:
    """Takes filename, partial or full path and find correct file from data-folder."""
    print(f"\nSearching {filename=}")

    #dir_path = os.path.dirname(os.path.realpath(__file__))
    netcdf_files = [Path(file).absolute() for file in glob.glob(f"data/netcdf/*/*/*.nc")]
    filepath = Path(filename).with_suffix(".nc")

    if filepath.is_absolute():
        # 1) Absolute and found
        if filepath in netcdf_files: return filepath
        # 2) Absolute and not found
        else:
            print("Filepath not found in data/netcdf -folder")
            filename = input("Please give another filename: ")
            return find_file(filename)
    
    if filepath.parent == Path("."):
        matches = [file for file in netcdf_files if file.name == filepath.name]
        if len(matches) > 1:
            # 3) Can't specify which file
            print(f"Found multiple files with the same name:")
            for match in matches:
                print(match)
            filename = input("Please give another filename: ")
            return find_file(filename)
        elif matches: 
            # 4) Found match for ambiguous name
            print("Found only one file matching name:")
            print(f"{matches[0]}")
            confirmation = input("Is this correct file? (y/n): ").lower()
            if confirmation == "y" or confirmation == "yes":
                return matches[0]
            else:
                # 5) User rejected the match
                print("Try one of these:")
                for file in netcdf_files[:20]:
                    print(file)
                filename = input("Please give another filename: ")
                return find_file(filename)
    
    matches = [file for file in netcdf_files if str(file).endswith(str(filepath))]
    if len(matches) > 1:
        # 6) Found multiple files
        print(f"Found multiple files with the same name:")
        for match in matches:
            print(match)
        filename = input("Please give more specific name: ")
        return find_file(filename)
    if matches:
        # 7) Found one match
        return matches[0]
    
    print("No matches found.")
    print("Try one of these:")
    for file in netcdf_files[:20]:
        print(file)
    filename = input("Please give more specific name: ")
    return find_file(filename)


def main():
    parser = ArgumentParser(
                    prog='Map It',
                    description='Creates geojsons from netCDF'
    )
    parser.add_argument("target", help="Filename.")
    parser.add_argument("filepath", help="Filename or path. Can be partial path. File is expected to be in data-folder.")
    args = parser.parse_args()
    filename:str = args.filepath
    target:str = args.target
    target = Path("data") / "geojson" / target
    if os.path.exists(target):
        confirmation = input(f"Target path already exists. Overwrite? (yes/no): ").lower()
        if confirmation != "y" and confirmation != "yes":
            print("Aborted.")
            return

    target = target.with_suffix(".json")
    origin = find_file(filename)
    
    confirmation = input(f"\nWrite geojson\nFrom {str(origin)}\nTo {str(target)}\nyes/no: ").lower()
    if confirmation != "y" and confirmation != "yes":
        print("Aborted.")
        return
    
    create_geojson.from_forecast(origin, target)
    print("Done.")



if __name__ == "__main__":
    main()