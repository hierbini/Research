import glob
import pickle
import coordgrid
import os

class InfilePath:

    def __init__(self, date, planet):
        self.reduced_folder = 'C:/Users/nguye/ResearchLab/Data/Lick/Data_Again/Reduced/'
        self.date = date
        self.planet_band = planet.band
        self.infile_directory = self.reduced_folder + self.date + "/" + self.planet_band + "/"
        self.all_files_in_folder = glob.glob(self.infile_directory + "*_red.fits")

    def path_to_infile(self):
        return self.infile_directory

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
        create_info_method(planet)

def save_info(out, save_address):
    output = pickle.dumps(out, protocol=0)
    with open(save_address, "wb") as file:
        file.write(output)

class SaveProjection:

    def __init__(self, filepath):
        self.filepath = filepath
        filedate = filepath[56:66] + '/'
        filename = 'projection_' + filepath[-14:]
        save_folder = 'C:/Users/nguye/ResearchLab/Code/Nav/SavedProjections/' + filedate
        self.save_address = ensure_directory_exists(save_folder) + filename

    def create_projection(self, planet):
        coords = coordgrid.CoordGrid(self.filepath, planet)
        coords.edge_detect()
        coords.project()
        coords.plot_projected([])

    def load_projection_from_file(self, planet):
        return load_info_from_file(planet, self.save_address, self.create_projection)

    def save_projection(self, out):
        save_info(out, self.save_address)

class SaveCoordGridVariables:

    def __init__(self, filepath):
        self.filepath = filepath
        self.filename = 'coordgrid_' + filepath[-14:]
        self.save_folder = 'C:/Users/nguye/ResearchLab/Code/Nav/CoordGridVariables/'

    def create_coords_variables(self, planet):
        coords = coordgrid.CoordGrid(self.filepath, planet)
        coords.edge_detect()
        coords.project()

    def load_coords_variables(self, planet):
        return load_info_from_file(planet, self.filename, self.save_folder, self.create_coords_variables)