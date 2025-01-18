import random
import argparse
from geopy.distance import geodesic
from geopy.point import Point
import re

def random_coordinate(center_lat, center_lon, min_distance_km, max_distance_km):
    """
    Generate a random coordinate within a given distance range of a center point.
    """
    # Generate a random bearing (0 to 360 degrees)
    bearing = round(random.uniform(0, 360), 3)
    
    # Generate a random distance (min_distance_km to max_distance_km)
    distance_km = random.uniform(min_distance_km, max_distance_km)
    
    # Use geopy to calculate the destination point
    center_point = Point(center_lat, center_lon)
    random_point = geodesic(kilometers=distance_km).destination(center_point, bearing)
    
    # Truncate to 4 decimal places
    truncated_lat = round(random_point.latitude, 4)
    truncated_lon = round(random_point.longitude, 4)
    
    return truncated_lat, truncated_lon

def parse_distance_input(distance_input):
    """
    Parse the distance input to determine if it's a range or a single number.
    """
    try:
        if '-' in distance_input:
            # Split the range input and parse as floats
            min_distance, max_distance = map(float, distance_input.split('-'))
            if min_distance > max_distance:
                raise ValueError("Minimum distance cannot be greater than maximum distance.")
        else:
            # Treat input as a single max distance, with min distance = 0
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
        # Get center coordinates
        if args.coord:
            cleaned_input = re.sub(r'[^\d.,-]', '', args.coord)
            center_latitude, center_longitude = map(float, cleaned_input.split(','))
        else:
            center_coordinates = input("Enter reference point (Lat, Long): ")
            cleaned_input = re.sub(r'[^\d.,-]', '', center_coordinates)
            center_latitude, center_longitude = map(float, cleaned_input.split(','))

        # Get distance input
        if args.range:
            distance_input = args.range
        else:
            distance_input = input("Enter the distance (km) or range (e.g., '10' or '5-15'): ")
        
        min_distance, max_distance = parse_distance_input(distance_input)
        
        # Generate a random coordinate
        random_lat, random_lon = random_coordinate(center_latitude, center_longitude, min_distance, max_distance)
        print(f"Random coordinate: {random_lat}, {random_lon}")
    except ValueError as e:
        print(f"Invalid input: {e}")

if __name__ == "__main__":
    main()