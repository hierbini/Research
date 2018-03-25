
import os
import sys
sys.path.append("C:\\Python36\\lib")
sys.path.append("C:\\Python36\\lib\\site-packages")
import glob
import pickle
import coordgrid

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

class Projection:

    def __init__(self, filepath):
        self.filepath = filepath
        self.filename = "projection_" + filepath[-14:]
        self.save_folder = 'C:/Users/nguye/ResearchLab/Code/Nav/SavedProjections/'

    def create_projection(self, path):
        coords = coordgrid.CoordGrid(path)
        coords.edge_detect()
        coords.project()
        coords.plot_projected()

    def load_projection_from_file(self):
        try:
            with open(self.save_folder + self.filename, "rb") as file:
                print("Read data from file.")
                return pickle.load(file)
        except FileNotFoundError:
            self.create_projection(self.filepath)

    def save_projection(self, out):
        output = pickle.dumps(out, protocol=0)
        with open(self.save_folder + self.filename, "wb") as file:
            file.write(output)