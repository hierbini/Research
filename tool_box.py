from planet_info import *
import save_paths as sp
from glob import glob
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
import sys
sys.path.append("C:\\Python36\\lib")
sys.path.append("C:\\Python36\\lib\\site-packages")


""" CONVERSION FUNCTIONS """


def convert_lat_degree_to_pixel(lat_degree, pixels_per_degree):
    return (lat_degree + 90) * pixels_per_degree


def convert_lon_degree_to_pixel(lon_degree, pixels_per_degree):
    return lon_degree * pixels_per_degree


def convert_dimensions_to_pixels(lat_dimensions, lon_dimensions, pixels_per_degree):
    lat_dimensions = [convert_lat_degree_to_pixel(lat_dimensions[i], pixels_per_degree) for i in range(2)]
    lon_dimensions = [convert_lon_degree_to_pixel(lon_dimensions[i], pixels_per_degree) for i in range(2)]
    return lat_dimensions, lon_dimensions


def convert_latlon_pixels_to_degrees(indices, pixels_per_degree):
    latitude = (indices[0] / pixels_per_degree) - 90
    longitude = indices[1] / pixels_per_degree
    return latitude, longitude

""" PATH FUNCTIONS """


def choose_date():
    available_dates = glob('C:/Users/nguye/ResearchLab/Data/Lick/Data_Again/Reduced/*')
    dates = {}
    for i in range(len(available_dates)):
        dates[str(i)] = get_file_date(available_dates[i])

    print('Hello! Which date would you like to look at?')
    for i in range(len(dates)):
        print('(' + str(i) + ') ' + dates[str(i)])
    chosen_date = input('To chose, type the number that corresponds to the date: ')
    return dates[chosen_date]


def choose_planet_band(date):
    available_bands = glob('C:/Users/nguye/ResearchLab/Data/Lick/Data_Again/Reduced/' + date + '/*')
    bands = {}
    for i in range(len(available_bands)):
        bands[str(i)] = get_file_planet_band(available_bands[i])

    print('Which folder would you like to look at?')
    for i in range(len(bands)):
        print('(' + str(i) + ') ' + bands[str(i)])
    planet_band = input('To chose, type the number that corresponds to the band: ')
    return bands[planet_band]


def choose_folder():
    date = choose_date()
    planet_band = choose_planet_band(date)
    if planet_band == 'Neptune_H':
        return NeptuneH(), date
    elif planet_band == 'Neptune_Ks':
        return NeptuneKs(), date
    elif planet_band == 'Uranus_H':
        return UranusH(), date
    elif planet_band == 'Uranus_Ks':
        return UranusKs(), date


def get_filename(path):
    return path[-14:]


def get_file_date(path):
    return path[56:66]


def get_file_planet_band(path):
    planet_bands = ['Neptune_H', 'Neptune_Ks', 'Uranus_H', 'Uranus_Ks']
    for planet_band in planet_bands:
        band = path.find(planet_band)
        if band is not -1:
            return planet_band


def get_all_paths(date, planet):
    return sp.InfilePath(date, planet).all_files_in_folder


""" GENERIC FUNCTIONS FOR SCRIPTS THAT USE MULTIPLE IMAGES """


def get_degrees_per_pixels(planet, paths):
    degrees_per_pixels = []
    for path in paths:
        coordgrid = sp.SaveCoordGrid(path).load_coordgrid(planet)
        degrees_per_pixels.append(coordgrid['degrees_per_pixel'])
    return degrees_per_pixels


def get_all_projections(paths, planet):
    return [sp.SaveProjection(path).load_projection_from_file(planet) for path in paths]

""" GENERIC PROJECTION FUNCTIONS """

def get_pixel_value(pixel_coordinates, projection):
    lat_pixel, lon_pixel = pixel_coordinates[0], pixel_coordinates[1]
    brightest_pixel_value = projection[int(lat_pixel)][int(lon_pixel)]
    return brightest_pixel_value

def get_line(central_coords):
    """ Returns list of coordinates ten pixels to the left and to the right of coordinates"""
    lat = central_coords[0]
    lon = central_coords[1]
    left_of_line = [(lat, lon - x) for x in range(10)]
    right_of_line = [(lat, lon + x) for x in range(10)]
    return left_of_line + [central_coords] + right_of_line

def plot_projection(image_name, vmin, vmax, projection, ctrlon = 180, lat_limits = (-90, 90), lon_limits = (0, 360), cbarlabel = 'Count'):
    vmin, vmax = vmin, vmax
    fontsize = 14
    fig, ax0 = plt.subplots(1, 1, figsize=(10, 7))
    extent = [ctrlon - 180, ctrlon + 180, -90, 90]
    cim = ax0.imshow(projection, extent=extent, origin='lower left', cmap='gray', vmin=vmin, vmax=vmax)
    parallels = np.arange(lat_limits[0], lat_limits[1] + 30, 30.)
    meridians = np.arange(lon_limits[0], lon_limits[1] + 60, 60.)
    for loc in parallels:
        ax0.axhline(loc, color='cyan', linestyle=':')
    for loc in meridians:
        ax0.axvline(loc, color='cyan', linestyle=':')

    # plot lines intersecting
    ax0.set_xlabel('Longitude', fontsize=fontsize)
    ax0.set_ylabel('Latitude', fontsize=fontsize)
    ax0.set_ylim(lat_limits)
    ax0.set_xlim(lon_limits)
    ax0.set_title(image_name, fontsize=fontsize + 2)
    ax0.tick_params(which='both', labelsize=fontsize - 2)

    # plot the colorbar
    divider = make_axes_locatable(ax0)
    cax = divider.append_axes('right', size='5%', pad=0.05)
    cbar = fig.colorbar(cim, cax=cax, orientation='vertical')
    cbar.set_label(cbarlabel, fontsize=fontsize)
    cax.tick_params(which='both', labelsize=fontsize - 2)
    plt.show()