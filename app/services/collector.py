import requests

def get_optimized_route(bin_locations):
    url = "https://api.mapbox.com/directions/v5/mapbox/driving/"
    coordinates = ";".join([f"{bin['longitude']},{bin['latitude']}" for bin in bin_locations])
    params = {
        "access_token": "MAPBOX_API_KEY",
        "overview": "full",
        "geometries": "geojson"
    }
    response = requests.get(url + coordinates, params=params)
    return response.json()
