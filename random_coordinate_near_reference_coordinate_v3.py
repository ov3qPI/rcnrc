import random
import argparse
import re
import math
from geopy.distance import geodesic
from geopy.point import Point

EARTH_RADIUS_KM = 6371.0088
RNG = random.SystemRandom()

def _uniform_distance_by_area_spherical(min_distance_km: float, max_distance_km: float) -> float:
    if min_distance_km < 0 or max_distance_km < 0:
        raise ValueError("Distances must be non-negative.")
    if min_distance_km > max_distance_km:
        raise ValueError("Minimum distance cannot be greater than maximum distance.")
    if min_distance_km == max_distance_km:
        return float(min_distance_km)
    a_min = min_distance_km / EARTH_RADIUS_KM
    a_max = max_distance_km / EARTH_RADIUS_KM
    u = RNG.random()
    cos_a = math.cos(a_min) - u * (math.cos(a_min) - math.cos(a_max))
    cos_a = max(-1.0, min(1.0, cos_a))
    a = math.acos(cos_a)
    return EARTH_RADIUS_KM * a

def random_coordinate(center_lat, center_lon, min_distance_km, max_distance_km):
    bearing = RNG.uniform(0.0, 360.0)
    distance_km = _uniform_distance_by_area_spherical(min_distance_km, max_distance_km)
    p = geodesic(kilometers=distance_km).destination(Point(center_lat, center_lon), bearing)
    return round(p.latitude, 6), round(p.longitude, 6)

def parse_distance_input(distance_input):
    try:
        if "-" in distance_input:
            min_distance, max_distance = map(float, distance_input.split("-", 1))
            if min_distance > max_distance:
                raise ValueError("Minimum distance cannot be greater than maximum distance.")
        else:
            min_distance = 0.0
            max_distance = float(distance_input)
        return min_distance, max_distance
    except ValueError:
        raise ValueError("Invalid distance format. Please provide a number or a range (e.g., '10' or '5-15').")

def main():
    parser = argparse.ArgumentParser(description="Random Coordinate Generator")
    parser.add_argument("--coord", type=str, help="Reference point in 'Lat,Long' format (e.g., '40.7128,-74.0060').")
    parser.add_argument("--range", type=str, help="Distance (km) or range (e.g., '10' or '5-15').")
    args = parser.parse_args()
    try:
        if args.coord:
            cleaned = re.sub(r"[^\d.,-]", "", args.coord)
            center_latitude, center_longitude = map(float, cleaned.split(",", 1))
        else:
            cleaned = re.sub(r"[^\d.,-]", "", input("Enter reference point (Lat, Long): "))
            center_latitude, center_longitude = map(float, cleaned.split(",", 1))
        distance_input = args.range if args.range else input("Enter the distance (km) or range (e.g., '10' or '5-15'): ")
        min_distance, max_distance = parse_distance_input(distance_input)
        lat, lon = random_coordinate(center_latitude, center_longitude, min_distance, max_distance)
        print(f"Random coordinate: {lat}, {lon}")
    except ValueError as e:
        print(f"Invalid input: {e}")

if __name__ == "__main__":
    main()
