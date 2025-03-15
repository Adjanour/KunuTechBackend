import math


def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points on Earth.

    :param lat1: Latitude of the first point (degrees)
    :param lon1: Longitude of the first point (degrees)
    :param lat2: Latitude of the second point (degrees)
    :param lon2: Longitude of the second point (degrees)
    :return: Distance in kilometers
    """
    R = 6371  # Radius of the Earth in kilometers

    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Differences in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distance in kilometers
    distance = R * c
    return distance


# Example Usage:
lat1, lon1 = 5.6037, -0.1870  # Accra, Ghana
lat2, lon2 = 6.6666, -1.6163  # Kumasi, Ghana

print(f"Distance: {haversine(lat1, lon1, lat2, lon2):.2f} km")
