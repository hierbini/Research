from shift_time import *
from projection import *
from save_paths import *
from planet_info import *
import coordgrid

def get_all_paths(planet, date):
    return [InfilePath(date, planet).all_files_in_folder[i] for i in range(4)]

def get_all_coordgrids(planet, paths):
    return [coordgrid.CoordGrid(path, planet) for path in paths]

def get_all_projections(paths):
    return [SaveProjection(path).load_projection_from_file(planet) for path in paths]

def get_all_shift_instances(shift_dictionary, coordgrids, projections):
    shiftprojections = []
    for i in range(len(paths)):
        image_name = paths[i][-14:]
        degrees_per_pixel = coordgrids[i].deg_per_px
        timeshift = shift_dictionary[image_name]
        projection = projections[i]
        shiftprojections.append(ProjectionShift(image_name, planet, degrees_per_pixel, timeshift, projection))
    return shiftprojections

def project_all_shift_instances(shift_dictionary, coordgrids, projections):
    shift_instances = get_all_shift_instances(shift_dictionary, coordgrids, projections)
    for shift_instance in shift_instances:
        shift_instance.plot_shifted_projection()
    plt.show()

if __name__ == "__main__":
    planet, date = NeptuneH(), '2017-08-31'
    paths = get_all_paths(planet, date)
    coordgrids = get_all_coordgrids(planet, paths)
    projections = get_all_projections(paths)
    shift_dictionary = ShiftTime(paths).shift_dictionary()
    #project_all_shift_instances(shift_dictionary, coordgrids, projections)

    #insert stack image code
