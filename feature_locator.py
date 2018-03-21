
import os
import sys
sys.path.append("C:\\Python36\\lib")
sys.path.append("C:\\Python36\\lib\\site-packages")

import numpy as np
import matplotlib.pyplot as plt
from tool_box import Convert

class FeatureLocator:

    def __init__(self, coordgrid, lat_dimensions = [-90, 90], lon_dimensions = [0, 360]):
        self.coords = coordgrid
        self.lat_dimensions = lat_dimensions
        self.lon_dimensions = lon_dimensions
        self.pixels_per_degree = 1.0 / self.coords.deg_per_px
        self.get_minimum_maximum = lambda dimensions: (int(dimensions[0]), int(dimensions[1]))

    def create_search_box(self, projection, lat_dimensions, lon_dimensions):
        '''Returns search box with latitude and longitude dimensions but in pixel scale. '''
        lat_dimensions, lon_dimensions = Convert.dimensions_to_pixels(lat_dimensions, lon_dimensions, self.pixels_per_degree)
        min_lat, max_lat = self.get_minimum_maximum(lat_dimensions)
        min_lon, max_lon = self.get_minimum_maximum(lon_dimensions)
        search_box = projection[min_lat:max_lat, min_lon:max_lon]
        return search_box

    def coordinates_of_brightest_pixel(self, search_box):
        indices = np.nanargmax(search_box)
        unshifted_coords = np.unravel_index(indices, np.shape(search_box))
        lat_shift = Convert.lat_degree_to_pixel(self.lat_dimensions[0], self.pixels_per_degree)
        lon_shift = Convert.lon_degree_to_pixel(self.lon_dimensions[0], self.pixels_per_degree)
        coordinates = [int(unshifted_coords[0] + lat_shift), int(unshifted_coords[1] + lon_shift)]
        print('Brightest pixel coordinates are ' + str(coordinates))
        return coordinates

    def find_latlon_of_feature(self, projection):
        search_box = self.create_search_box(projection, self.lat_dimensions, self.lon_dimensions)
        found_coordinates = self.coordinates_of_brightest_pixel(search_box)
        longitude, latitude = Convert.lonlat_pixels_to_degrees(found_coordinates, self.pixels_per_degree)
        return latitude, longitude

    def user_draws_a_box(self):
        min_lat = int(input('Input lowest latitude: '))
        max_lat = int(input('Input highest latitude: '))
        min_lon = int(input('Input lowest longitude: '))
        max_lon = int(input('Input highest longitude: '))
        self.lat_dimensions = [min_lat, max_lat]
        self.lon_dimensions = [min_lon, max_lon]

        return self.lat_dimensions, self.lon_dimensions

class CloudLocator(FeatureLocator):

    def announce_cloud_center(self, latitude, longitude):
        return 'Cloud center is {0} degrees latitude and {1} degrees longitude.'.format(latitude, longitude)

    def find_latlon_of_cloud_center(self, projection):
        """ Searches within box of specified dimensions and returns the latitude and longitude of the
        brightest pixel on the cloud """
        latitude, longitude = self.find_latlon_of_feature(projection)
        print(self.announce_cloud_center(latitude, longitude))
        return latitude, longitude

    def plot_cloud_center(self, projection):
        self.user_draws_a_box()
        cloud_center_lat, cloud_center_lon = self.find_latlon_of_cloud_center(projection)
        plt.scatter(cloud_center_lon, cloud_center_lat, color = 'k')
        plt.axvline(cloud_center_lon, color = 'k')
        plt.axhline(cloud_center_lat, color = 'k')



    
