
import os
import sys
sys.path.append("C:\\Python36\\lib")
sys.path.append("C:\\Python36\\lib\\site-packages")
import save_paths as sp
from glob import glob
from planet_info import *

""" CONVERSION FUNCTIONS """


def convert_lat_degree_to_pixel(lat_degree, pixels_per_degree):
    return (lat_degree + 90) * pixels_per_degree


def convert_lon_degree_to_pixel(lon_degree, pixels_per_degree):
    return lon_degree * pixels_per_degree


def convert_dimensions_to_pixels(lat_dimensions, lon_dimensions, pixels_per_degree):
    lat_dimensions = [convert_lat_degree_to_pixel(lat_dimensions[i], pixels_per_degree) for i in range(2)]
    lon_dimensions = [convert_lon_degree_to_pixel(lon_dimensions[i], pixels_per_degree) for i in range(2)]
    return lat_dimensions, lon_dimensions


def convert_lonlat_pixels_to_degrees(indices, pixels_per_degree):
    lattitude = (indices[0] / pixels_per_degree) - 90
    longitude = indices[1] / pixels_per_degree
    return longitude, lattitude

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


def get_all_paths(planet, date):
    return sp.InfilePath(date, planet).all_files_in_folder


""" GENERIC FUNCTIONS FOR SCRIPTS THAT USE MULTIPLE IMAGES """


def get_degree_per_pixels(planet, paths):
    degrees_per_pixels = []
    for path in paths:
        coordgrid = sp.SaveCoordGrid(path).load_coordgrid(planet)
        degrees_per_pixels.append(coordgrid['degrees_per_pixel'])
    return degrees_per_pixels


def get_all_projections(paths, planet):
    return [sp.SaveProjection(path).load_projection_from_file(planet) for path in paths]
