
import os
import sys
sys.path.append("C:\\Python36\\lib")
sys.path.append("C:\\Python36\\lib\\site-packages")

import pyfits
import coordgrid

class CloudFeature:

    def __init__(self, coordgrid, feature_locator):
        self.coordgrid = coordgrid
        self.feature_locator = feature_locator

    def correct_planets_rotation(self, planet):
        ''' In the case that we need to compare two images, the images should be aligned. However, 
        due to time in between observations, one image may be shifted because of planetary rotation.
        This function returns something that corrects this rotation.'''

    def write_file(self, outfile):
        '''Adds to HDUlist of original image?'''
        hdulist_data = pyfits.PrimaryHDU(self.coordgrid.data, header = self.header)

class KHFraction(CloudFeature):

    def __init__(self, H_coordgrid, K_coordgrid, H_projection, K_projection):
        self.H_projection = H_projection
        self.K_projection = K_projection
        self.H_coordgrid = H_coordgrid
        self.K_coordgrid = K_coordgrid

    def get_brightest_pixel_value(self, coordgrid, projection, lat_dimensions, lon_dimensions):
        search_box = coordgrid.feature_locator.create_search_box(projection, lat_dimensions, lon_dimensions)
        brightest_pixel_coordinates = coordgrid.feature_locator.coordinates_of_brightest_pixel(search_box)
        lat_pixel, lon_pixel = brightest_pixel_coordinates[0], brightest_pixel_coordinates[1]
        brightest_pixel_value = projection[int(lat_pixel)][int(lon_pixel)]
        return brightest_pixel_value

    def calculate_K_H_fraction(self):
        lat_dimensions, lon_dimensions = self.H_coordgrid.feature_locator.user_draws_a_box()
        H_value = self.get_brightest_pixel_value(self.H_coordgrid, self.H_projection, lat_dimensions, lon_dimensions)
        K_value = self.get_brightest_pixel_value(self.K_coordgrid, self.K_projection, lat_dimensions, lon_dimensions)
        print(str(H_value), str(K_value))
        self.H_coordgrid.plot_projected(self.H_projection)
        K_H_Fraction = K_value / H_value
        return K_H_Fraction




