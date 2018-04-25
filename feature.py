
import os
import sys
sys.path.append("C:\\Python36\\lib")
sys.path.append("C:\\Python36\\lib\\site-packages")
import matplotlib.pyplot as plt
import tool_box as tb

class KHFraction:

    def __init__(self, H_feature_locator, K_feature_locator, H_projection, K_projection):
        self.H_projection = H_projection
        self.K_projection = K_projection
        self.H_feature_locator = H_feature_locator
        self.K_feature_locator = K_feature_locator

    def calculate_K_H_fraction(self, K_value, H_value):
        K_H_Fraction = K_value / H_value
        return K_H_Fraction

    def get_K_H_fractions_along_line(self):
        lat_dimensions, lon_dimensions = self.H_feature_locator.user_draws_a_box()
        H_search_box = self.H_feature_locator.create_search_box(self.H_projection, lat_dimensions, lon_dimensions)
        K_search_box = self.K_feature_locator.create_search_box(self.K_projection, lat_dimensions, lon_dimensions)
        self.H_brightest_pix_coords = self.H_feature_locator.coordinates_of_brightest_pixel(H_search_box)
        self.K_brightest_pix_coords = self.K_feature_locator.coordinates_of_brightest_pixel(K_search_box)
        self.H_line = tb.get_line(self.H_brightest_pix_coords)
        self.K_line = tb.get_line(self.K_brightest_pix_coords)
        self.H_pixel_values = [tb.get_pixel_value(coord, self.H_projection) for coord in self.H_line]
        self.K_pixel_values = [tb.get_pixel_value(coord, self.K_projection) for coord in self.K_line]
        self.K_H_fraction_along_line = [self.calculate_K_H_fraction(self.K_pixel_values[i], self.H_pixel_values[i]) for i in range(len(self.H_line))]

    def print_things(self, pixels_per_degrees):
        self.get_K_H_fractions_along_line()
        H_line = [(tb.convert_latlon_pixels_to_degrees(self.H_line[i], pixels_per_degrees)) for i in range(len(self.H_line))]
        print('Latitude: {0}'.format(tb.convert_latlon_pixels_to_degrees(self.H_brightest_pix_coords, pixels_per_degrees)[0]))

        for i in range(len(H_line)):
            longitude = round(H_line[i][1], 2)
            brightness = round(self.H_pixel_values[i], 2)
            KH_fraction = round(self.K_H_fraction_along_line[i], 2)
            print('Longitude: {0} | Brightness: {1} | KH Fraction: {2}'.format(longitude, brightness, KH_fraction))
