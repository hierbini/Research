
import os
import sys
sys.path.append("C:\\Python36\\lib")
sys.path.append("C:\\Python36\\lib\\site-packages")

import pyfits
import coordgrid

class CloudFeature:

    def __init__(self, coordgrid, feature_locator):
        self.coordgrid = coordgrid
        self.CloudFeature = feature_locator

    def correct_planets_rotation(self, planet):
        ''' In the case that we need to compare two images, the images should be aligned. However, 
        due to time in between observations, one image may be shifted because of planetary rotation.
        This function returns something that corrects this rotation.'''

    def write_file(self, outfile):
        '''Adds to HDUlist of original image?'''
        hdulist_data = pyfits.PrimaryHDU(self.coordgrid.data, header = self.header)

class HKFraction(CloudFeature):

    """
    The Plan:
    - get path to H and K path, use middle image
    - project both images (no need to plot probably? or plot one image)
    - get brightest pixel for both images
    - get value from both images at that coordinate
    - divide H value by K value

    eventually:
    - create method to correct for planet rotation
    """

    def __init__(self, planetH_path, planetK_path):
        self.H_image = planetH_path.all_files_in_folder[2] # Using 2 as middle image
        self.K_image = planetK_path.all_files_in_folder[2]
        self.H_coordgrid = coordgrid.CoordGrid(self.H_image)
        self.K_coordgrid = coordgrid.CoordGrid(self.K_image)
        self.edge_detect_H_and_K()
        self.project_H_and_K()

    def edge_detect_H_and_K(self):
        self.H_coordgrid.edge_detect()
        self.K_coordgrid.edge_detect()

    def project_H_and_K(self):
        self.H_coordgrid.project()
        self.K_coordgrid.project()

    def get_brightest_pixel_value(self, coordgrid, lat_dimensions, lon_dimensions):
        search_box = CloudFeature.feature_locator.create_search_box(lat_dimensions, lon_dimensions)
        brightest_pixel_coordinates = CloudFeature.feature_locator.coordinates_of_brightest_pixel(search_box)
        lat_pixel, lon_pixel = brightest_pixel_coordinates[0], brightest_pixel_coordinates[1]
        brightest_pixel_value = coordgrid.projected[lat_pixel, lon_pixel]
        return brightest_pixel_value

    def calculate_H_K_fraction(self):
        ''' This function will draw a box of specified longitudinal and latitudinal dimensions on the
        projected image and calculate the H/K fraction of each pixel within this box'''
        print('Time to calculate our H/K fraction. Please specify the dimensions of your box: ')
        CloudFeature.feature_locator.user_draws_a_box()
        self.lat_dimensions = CloudFeature.feature_locator.lat_dimensions
        self.lon_dimensions = CloudFeature.feature_locator.lon_dimensions
        H_value = self.get_brightest_pixel_value(self.H_coordgrid, self.lat_dimensions, self.lon_dimensions)
        K_value = self.get_brightest_pixel_value(self.K_coordgrid, self.lat_dimensions, self.lon_dimensions)
        H_K_fraction = H_value / K_value
        return H_K_fraction




