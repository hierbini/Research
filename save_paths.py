import glob
import pickle
import os
from stacked_projection import *
import coordgrid
import tool_box as tb


class InfilePath:

    def __init__(self, date, planet):
        self.reduced_folder = 'C:/Users/nguye/ResearchLab/Data/Lick/Data_Again/Reduced/'
        self.date = date
        self.planet_band = planet.band
        self.infile_directory = self.reduced_folder + self.date + "/" + self.planet_band + "/"
        self.all_files_in_folder = glob.glob(self.infile_directory + "*_red.fits")

    def path_to_infile(self):
        return self.infile_directory

### FUNCTIONS THAT SAVE INFORMATION ###

def ensure_directory_exists(filepath):
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    return filepath


def load_info_from_file(planet, save_address, create_info_method):
    try:
        with open(save_address, "rb") as file:
            print("Load info from file.")
            return pickle.load(file)
    except FileNotFoundError:
        return create_info_method(planet)


def save_info(out, save_address):
    output = pickle.dumps(out, protocol=0)
    with open(save_address, "wb") as file:
        file.write(output)


class SaveProjection:

    def __init__(self, filepath):
        self.filepath = filepath
        filedate = tb.get_file_date(filepath) + '/'
        filename = 'projection_' + tb.get_filename(filepath)
        planet_band = tb.get_file_planet_band(filepath) + '/'
        save_folder = 'C:/Users/nguye/ResearchLab/Code/Nav/SavedProjections/' + filedate + planet_band
        self.save_address = ensure_directory_exists(save_folder) + filename

    def create_projection(self, planet):
        coords = coordgrid.CoordGrid(self.filepath, planet)
        coords.edge_detect()
        coords.project()
        coords.plot_projected([])
        return coords.projected

    def load_projection_from_file(self, planet):
        return load_info_from_file(planet, self.save_address, self.create_projection)

    def save_projection(self, out):
        save_info(out, self.save_address)


class SaveStackedProjection:

    def __init__(self, date, planet):
        self.date = date
        self.planet = planet
        self.band = planet.band
        save_folder = 'C:/Users/nguye/ResearchLab/Code/Nav/SavedStackedProjections/'
        self.save_address = save_folder + date + '/' + planet.band

    def create_stacked_projection(self, planet):
        paths = tb.get_all_paths(planet, self.date)
        degree_per_pixels = tb.get_degree_per_pixels(planet, paths)
        projections = tb.get_all_projections(paths, planet)
        shift_dictionary = ShiftTime(paths).shift_dictionary()
        shift_instances = get_all_shift_instances(shift_dictionary, degree_per_pixels, projections)

        integration_times = get_all_integration_times(paths)
        shifted_projections = get_all_shifted_projections(integration_times, shift_instances)

        stacked_projection = stack_projections(shifted_projections)
        image_name = 'Stacked Projection for ' + self.date
        plot_projection(image_name, self.planet, stacked_projection / 5)

        answer = input("Do you want to save this stacked projection? (y/n): ")
        if answer == 'y':
            self.save_stacked_projection(stacked_projection)

    def load_stacked_projection_from_file(self, planet):
        return load_info_from_file(planet, self.save_address, self.create_stacked_projection)

    def save_stacked_projection(self, out):
        save_info(out, self.save_address)


class SaveCoordGrid:

    def __init__(self, filepath):
        self.filepath = filepath
        filedate = tb.get_file_date(filepath) + '/'
        filename = 'coordgrid_' + tb.get_filename(filepath)
        save_folder = 'C:/Users/nguye/ResearchLab/Code/Nav/SavedCoordgrids/' + filedate
        self.save_address = ensure_directory_exists(save_folder) + filename

    def create_coordgrid(self, planet):
        coords = coordgrid.CoordGrid(self.filepath, planet)
        coords_variables = {"degrees_per_pixel": coords.deg_per_px}
        self.save_coordgrid(coords_variables)
        return coords_variables

    def load_coordgrid(self, planet):
        return load_info_from_file(planet, self.save_address, self.create_coordgrid)

    def save_coordgrid(self, out):
        save_info(out, self.save_address)