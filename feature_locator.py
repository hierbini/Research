
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

    def __init__(self, coordgrid, lat_dimensions = [-90, 90], lon_dimensions = [0, 360]):
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
        print(search_box)
        return search_box

    def brightest_pixel_coordinates(self, search_box):
        indices = np.nanargmax(search_box)
        lon_lat_coordinates = np.unravel_index(indices, np.shape(search_box))
        print(lon_lat_coordinates)
        return lon_lat_coordinates

class Cloud_Locator(Feature_Locator):

    def announce_cloud_center(self, lattitude, longitude):
        return 'Cloud center is {0} degrees lattitude and {1} degrees longitude.'.format(lattitude, longitude)

    def find_latlon_of_cloud_center(self):
        ''' Searches within box of specified dimensions and returns the lattitude and longitude of the 
        brightest pixel on the cloud '''
        search_box = self.create_search_box(self.lat_dimensions, self.lon_dimensions)
        print(self.lat_dimensions, self.lon_dimensions)
        found_coordinates = self.brightest_pixel_coordinates(search_box)
        longitude, lattitude = Convert.pixels_to_degrees(found_coordinates, self.pixels_per_degree)
        print(self.announce_cloud_center(lattitude, longitude))
        return lattitude, longitude

    def plot_cloud_center(self):
        cloud_center_lat, cloud_center_lon = self.find_latlon_of_cloud_center()
        plt.scatter(cloud_center_lon, cloud_center_lat, color = 'k')
        plt.axvline(cloud_center_lon, color = 'k')
        plt.axhline(cloud_center_lat, color = 'k')

    
