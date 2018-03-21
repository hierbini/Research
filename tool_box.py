
import os
import sys
sys.path.append("C:\\Python36\\lib")
sys.path.append("C:\\Python36\\lib\\site-packages")
import glob

class Convert:

    def lat_degree_to_pixel(lat_degree, pixels_per_degree):
        return (lat_degree + 90) * pixels_per_degree

    def lon_degree_to_pixel(lon_degree, pixels_per_degree):
        return lon_degree * pixels_per_degree

    def dimensions_to_pixels(lat_dimensions, lon_dimensions, pixels_per_degree):
        lat_dimensions = [Convert.lat_degree_to_pixel(lat_dimensions[i], pixels_per_degree) for i in range(2)]
        lon_dimensions = [Convert.lon_degree_to_pixel(lon_dimensions[i], pixels_per_degree) for i in range(2)]
        return lat_dimensions, lon_dimensions

    def lonlat_pixels_to_degrees(indices, pixels_per_degree):
        lattitude = (indices[0] / pixels_per_degree) - 90 
        longitude = indices[1] / pixels_per_degree
        return longitude, lattitude

class Path:

    def __init__(self, date, planet_band):
        self.reduced_folder = 'C:/Users/nguye/ResearchLab/Data/Lick/Data_Again/Reduced/'
        self.date = date
        self.planet_band = planet_band
        self.infile_directory = self.reduced_folder + self.date + "/" + self.planet_band + "/"
        self.all_files_in_folder = glob.glob(self.infile_directory + "*_red.fits")

    def path_to_infile(self):
        return self.infile_directory

class Neptune:

    def __init__(self):
        self.name = 'Neptune'
        self.rotational_velocity = 2.86
        self.polar_radius = 24341
        self.equatorial_radius = 24764

class Uranus:

    def __init__(self):
        self.name = 'Uranus'
        self.rotational_velocity = 2.59
        self.polar_radius = 24973
        self.equatorial_radius = 25559