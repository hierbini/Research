from feature import KHFraction
from feature_locator import *
import tool_box as tb
from planet_info import *
import shift_time
import save_paths as sp
import shift_projection

K, H = 0, 1

def get_K_H_paths(date, planets):
    H_paths = sp.InfilePath(date, planets[H]).all_files_in_folder
    K_paths = sp.InfilePath(date, planets[K]).all_files_in_folder
    return K_paths, H_paths


def get_K_H_shift_times(K_paths, H_paths):
    H_shift_time = shift_time.ShiftTime(H_paths)
    K_shift_time = shift_time.ShiftTime(K_paths)
    average_H_time = H_shift_time.get_average_timestamp()
    average_K_time = K_shift_time.get_average_timestamp()
    new_average = (average_H_time + average_K_time) / 2
    new_H_shift_time = new_average - average_H_time
    new_K_shift_time = new_average - average_K_time
    return new_K_shift_time, new_H_shift_time


def get_K_H_projections(date, planets):
    H_projection = sp.SaveStackedProjection(date, planets[H]).load_stacked_projection_from_file(planets[H])
    K_projection = sp.SaveStackedProjection(date, planets[K]).load_stacked_projection_from_file(planets[K])
    return [K_projection, H_projection]


def get_K_H_degrees_per_pixels(K_path, H_path, planets):
    H_deg_per_pix = sp.SaveCoordGrid(K_path).load_coordgrid(planets[H])['degrees_per_pixel']
    K_deg_per_pix = sp.SaveCoordGrid(K_path).load_coordgrid(planets[K])['degrees_per_pixel']
    return [K_deg_per_pix, H_deg_per_pix]


def get_K_H_feature_locators(K_deg_per_pix, H_deg_per_pix):
    H_feature_locator = FeatureLocator(H_deg_per_pix)
    K_feature_locator = FeatureLocator(K_deg_per_pix)
    return K_feature_locator, H_feature_locator


def get_K_H_shifted_projections(planets, degrees_per_pixels, time_shifts, projections):
    K_deg_per_pix, H_deg_per_pix = degrees_per_pixels[K], degrees_per_pixels[H]
    K_time_shift, H_time_shift = time_shifts[K], time_shifts[H]
    K_projection, H_projection = projections[K], projections[H]
    K_shift_proj = shift_projection.ProjectionShift("K band", planets[K], K_deg_per_pix, K_time_shift, K_projection)
    H_shift_proj = shift_projection.ProjectionShift("H band", planets[H], H_deg_per_pix, H_time_shift, H_projection)
    K_shifted_projection = K_shift_proj.shift_projection()
    H_shifted_projection = H_shift_proj.shift_projection()
    return K_shifted_projection, H_shifted_projection

# Begin
planets, date = [NeptuneKs(), NeptuneH()], tb.choose_date()

# Collect information
paths = get_K_H_paths(date, planets)
projections = get_K_H_projections(date, planets)
degrees_per_pixels = get_K_H_degrees_per_pixels(paths[K][2], paths[H][2], planets)
shift_times = get_K_H_shift_times(paths[K], paths[H])
K_feature_locator, H_feature_locator = get_K_H_feature_locators(degrees_per_pixels[K], degrees_per_pixels[H])

# Get shifted projections
K_shifted_projection, H_shifted_projection = get_K_H_shifted_projections(planets, degrees_per_pixels, shift_times, projections)

# Calculate KH fraction

first, keep_going = True, 'y'
while keep_going == 'y':
    if first:
        print('Time to calculate your K/H value! Please specify the limits of your box.')
        first = False
    tb.plot_projection("Shifted H Projection", 0, 20, H_shifted_projection)
    K_H_fraction = KHFraction(H_feature_locator, K_feature_locator, H_shifted_projection, K_shifted_projection)
    K_H_fraction.print_things((1 / degrees_per_pixels[0]))
    keep_going = input("Would you like to calculate another value? (y/n): ")
