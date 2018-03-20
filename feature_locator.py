
import os
import sys
sys.path.append("C:\\Python36\\lib")
sys.path.append("C:\\Python36\\lib\\site-packages")
import pyfits
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from get_ephem import get_ephemerides, naif_lookup
from image import Image
from datetime import datetime, timedelta
import warnings
from skimage import feature
from image_registration.chi2_shifts import chi2_shift
from image_registration.fft_tools.shift import shiftnd, shift2d
from scipy.interpolate import interp2d, RectBivariateSpline, NearestNDInterpolator, griddata
from mpl_toolkits.axes_grid1 import make_axes_locatable
from Tool_Box import Convert
#from coordgrid import CoordGrid

class Feature_Locator:

    def __init__(self, coordgrid, lat_dimensions = [0, 40], lon_dimensions = [200, 300]):
        self.coordgrid = coordgrid
        self.lat_dimensions = lat_dimensions
        self.lon_dimensions = lon_dimensions
        self.pixels_per_degree = 1.0 / self.coordgrid.deg_per_px
        self.get_minimum_maximum = lambda dimensions: (int(dimensions[0]), int(dimensions[1]))

    def create_search_box(self, lat_dimensions, lon_dimensions):
        '''Returns search box with lattitude and longitude dimensions but in pixel scale. '''
        lat_dimensions, lon_dimensions = Convert.dimensions_to_pixels(lat_dimensions, lon_dimensions, self.pixels_per_degree)
        min_lat, max_lat = self.get_minimum_maximum(lat_dimensions)
        min_lon, max_lon = self.get_minimum_maximum(lon_dimensions)
        search_box = self.coordgrid.projected[min_lat:max_lat, min_lon:max_lon]
        return search_box

    def brightest_pixel_coordinates(self, search_box):
        indices = np.nanargmax(search_box)
        found_coordinates = np.unravel_index(indices, np.shape(search_box))
        latitude_shift = Convert.lat_degree_to_pixel(self.lat_dimensions[0], self.pixels_per_degree)
        longitude_shift = Convert.lon_degree_to_pixel(self.lon_dimensions[0], self.pixels_per_degree)
        found_coordinates = (found_coordinates[0] + latitude_shift, found_coordinates[1] + longitude_shift)
        print('Brightest pixel coordinates are ' + str(found_coordinates))
        return found_coordinates

    def find_latlon_of_feature(self):
        search_box = self.create_search_box(self.lat_dimensions, self.lon_dimensions)
        found_coordinates = self.brightest_pixel_coordinates(search_box)
        longitude, latitude = Convert.lonlat_pixels_to_degrees(found_coordinates, self.pixels_per_degree)
        return latitude, longitude

    def user_draws_a_box(self):
        min_lat = int(input('Input lowest latitude: '))
        max_lat = int(input('Input highest latitude: '))
        min_lon = int(input('Input lowest longitude: '))
        max_lon = int(input('Input highest longitude: '))
        
        self.lat_dimensions = [min_lat, max_lat]
        self.lon_dimensions = [min_lon, max_lon]


class Cloud_Locator(Feature_Locator):

    def announce_cloud_center(self, latitude, longitude):
        return 'Cloud center is {0} degrees latitude and {1} degrees longitude.'.format(latitude, longitude)

    def find_latlon_of_cloud_center(self):
        ''' Searches within box of specified dimensions and returns the latitude and longitude of the 
        brightest pixel on the cloud '''
        latitude, longitude = self.find_latlon_of_feature()
        print(self.announce_cloud_center(latitude, longitude))
        return latitude, longitude

    def plot_cloud_center(self, first = True, keep_going = 'y'):        
        self.user_draws_a_box()
        cloud_center_lat, cloud_center_lon = self.find_latlon_of_cloud_center()
        plt.scatter(cloud_center_lon, cloud_center_lat, color = 'k')
        plt.axvline(cloud_center_lon, color = 'k')
        plt.axhline(cloud_center_lat, color = 'k')



    
