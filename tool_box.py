
import os
import sys
sys.path.append("C:\\Python36\\lib")
sys.path.append("C:\\Python36\\lib\\site-packages")

def convert_lat_degree_to_pixel(lat_degree, pixels_per_degree):
    return (lat_degree + 90) * pixels_per_degree

def convert_lon_degree_to_pixel(lon_degree, pixels_per_degree):
    return lon_degree * pixels_per_degree

def convert_dimensions_to_pixels(lat_dimensions, lon_dimensions, pixels_per_degree):
    lat_dimensions = [convert_lat_degree_to_pixel(lat_dimensions[i], pixels_per_degree) for i in range(2)]
    lon_dimensions = [convert_lon_degree_to_pixel(lon_dimensions[i], pixels_per_degree) for i in range(2)]
    return lat_dimensions, lon_dimensions

def convert_lonlat_pixels_to_degrees(indices, pixels_per_degree):
    lattitude = (indices[0] / pixels_per_degree) - 90
    longitude = indices[1] / pixels_per_degree
    return longitude, lattitude