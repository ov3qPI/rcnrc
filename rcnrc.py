import random
from geopy.distance import geodesic
from geopy.point import Point
import re

def random_coordinate(center_lat, center_lon, max_distance_km):
    """
    Generate a random coordinate within a given distance of a center point.

    :param center_lat: Latitude of the center point
    :param center_lon: Longitude of the center point
    :param max_distance_km: Maximum distance in kilometers
    :return: (latitude, longitude) of the random point
    """
    # Generate a random bearing (0 to 360 degrees)
    bearing = random.uniform(0, 360)
    
    # Generate a random distance (0 to max_distance_km)
    distance_km = random.uniform(0, max_distance_km)
    
    # Use geopy to calculate the destination point
    center_point = Point(center_lat, center_lon)
    random_point = geodesic(kilometers=distance_km).destination(center_point, bearing)
    
    return random_point.latitude, random_point.longitude

def main():
    print("Random Coordinate Generator")
    try:
        # Prompt user for input
        center_coordinates = input("Enter reference point (Lat, Long): ")
        
        # Remove degree symbols and whitespace, then parse as floats
        cleaned_input = re.sub(r'[^\d.,-]', '', center_coordinates)
        center_latitude, center_longitude = map(float, cleaned_input.split(','))
        
        max_distance = float(input("Enter the max distance (km): "))
        
        # Generate a random coordinate
        random_lat, random_lon = random_coordinate(center_latitude, center_longitude, max_distance)
        print(f"Random coordinate: {random_lat}, {random_lon}")
    except ValueError:
        print("Invalid input. Please ensure the format and values are correct.")

if __name__ == "__main__":
    main()