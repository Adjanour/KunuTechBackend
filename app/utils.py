import math

def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great-circle distance between two points on Earth using the Haversine formula.

    :param lat1: Latitude of the first point (degrees)
    :param lon1: Longitude of the first point (degrees)
    :param lat2: Latitude of the second point (degrees)
    :param lon2: Longitude of the second point (degrees)
    :return: Distance in kilometers
    """
    R = 6371  # Radius of the Earth in km

    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Compute differences
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Apply Haversine formula
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Compute distance
    distance = R * c
    return round(distance, 2)  # Return rounded distance in km
