import json

with open("data/geojson/europe.squares.geo.json", "r") as file:
    data = json.load(file)

north_limit = None
south_limit = None
west_limit = None
east_limit = None


sub_region = {
    "type": "FeatureCollection",
    "center": {"lat": round((south_limit+north_limit)/2, 2), "lon": round((west_limit+east_limit)/2, 2)},
    "limits": {
        "north": north_limit,
        "south": south_limit,
        "west": west_limit,
        "east": east_limit
    },
    "features": []
}

for feature in data["features"]:
    centroid = feature["geometry"]["centroid"]
    lon = centroid[0]
    lat = centroid[1]
    location = {
        "type": "Feature",
        "id": feature["id"],
        "geometry": {
            "type": "Polygon",
            "centroid": centroid,
            "coordinates": feature["geometry"]["coordinates"]
        }
    }
    if (lon > west_limit and
        lon < east_limit and
        lat < north_limit and
        lat > south_limit):
        sub_region["features"].append(location)

with open("data/geojson/europe.forecast.geo.json", "w") as file:
    file.write(json.dumps(sub_region))