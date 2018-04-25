from shift_time import *
from projection_functions import *
from planet_info import *
import numpy as np
import pyfits
import tool_box as tb
import save_paths as sp

def get_all_shift_instances(shift_dictionary, degree_per_pixels, projections):
    shiftprojections = []
    for i in range(len(paths)):
        image_name = get_filename(paths[i])
        degrees_per_pixel = degree_per_pixels[i]
        timeshift = shift_dictionary[image_name]
        projection = projections[i]
        shiftprojections.append(ProjectionShift(image_name, planet, degrees_per_pixel, timeshift, projection))
    return shiftprojections

def get_all_integration_times(paths):
    integration_times = []
    for path in paths:
        hdu = pyfits.open(path)
        integration_time = hdu[0].header['TRUITIME']
        integration_times.append(integration_time)
    return integration_times

def get_all_shifted_projections(integration_times, shift_instances):
    shifted_projections = []
    for i in range(len(shift_instances)):
        shifted_projection = shift_instances[i].shift_projection()
        shifted_projections.append(shifted_projection)
    return shifted_projections

def stack_projections(projections):
    assert len(projections) > 1
    shape = np.shape(projections[0])
    stacked_projection = np.zeros(shape)
    for projection in projections:
        stacked_projection += projection
    return stacked_projection

def project_all_shift_instances(shift_instances):
    for shift_instance in shift_instances:
        shift_instance.plot_shifted_projection()
    plt.show()

if __name__ == "__main__":
    planet, date = tb.choose_folder()
    stacked_projection = sp.SaveStackedProjection(date, planet)
    stacked_projection.load_stacked_projection_from_file(planet)
