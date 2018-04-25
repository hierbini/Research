
import os
import sys
sys.path.append("C:\\Python36\\lib")
sys.path.append("C:\\Python36\\lib\\site-packages")
import pyfits

class KHFraction:

    def __init__(self, H_feature_locator, K_feature_locator, H_projection, K_projection):
        self.H_projection = H_projection
        self.K_projection = K_projection
        self.H_feature_locator = H_feature_locator
        self.K_feature_locator = K_feature_locator

    def get_pixel_value(self, pixel_coordinates, projection):
        lat_pixel, lon_pixel = pixel_coordinates[0], pixel_coordinates[1]
        brightest_pixel_value = projection[int(lat_pixel)][int(lon_pixel)]
        return brightest_pixel_value

    def calculate_K_H_fraction(self, K_value, H_value):
        K_H_Fraction = K_value / H_value
        print("The K/H value is: " + str(K_H_Fraction))

    def get_line(self, central_coords):
        """ Returns list of coordinates ten pixels to the left and to the right of coordinates"""
        lat = central_coords[0]
        lon = central_coords[1]
        left_of_line = [(lat, lon - x) for x in range(10)]
        right_of_line = [(lat, lon + x) for x in range(10)]
        return left_of_line + [central_coords] + right_of_line

    def get_K_H_fractions_along_line(self, first = True, keep_going = 'y'):
        while keep_going == 'y':
            if first:
                print('Time to calculate your K/H value! Please specify the limits of your box.')
                first = False
            lat_dimensions, lon_dimensions = self.H_feature_locator.user_draws_a_box()
            H_search_box = self.H_feature_locator.create_search_box(self.H_projection, lat_dimensions, lon_dimensions)
            K_search_box = self.K_feature_locator.create_search_box(self.K_projection, lat_dimensions, lon_dimensions)
            H_brightest_pix_coords = self.H_feature_locator.coordinates_of_brightest_pixel(H_search_box)
            K_brightest_pix_coords = self.K_feature_locator.coordinates_of_brightest_pixel(K_search_box)
            H_line = self.get_line(H_brightest_pix_coords)
            K_line = self.get_line(K_brightest_pix_coords)
            H_pixel_values = [self.get_pixel_value(coord, self.H_projection) for coord in H_line]
            K_pixel_values = [self.get_pixel_value(coord, self.K_projection) for coord in K_line]

            K_H_fraction_along_line = [self.calculate_K_H_fraction(K_pixel_values[i], H_pixel_values[i]) for i in range(len(H_line))]

            keep_going = input("Would you like to calculate another value? (y/n): ")

