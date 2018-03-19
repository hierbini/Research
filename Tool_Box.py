
import os
import sys
sys.path.append("C:\\Python36\\lib")
sys.path.append("C:\\Python36\\lib\\site-packages")
import pyfits
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from get_ephem import get_ephemerides, naif_lookup
from image import Image
from datetime import datetime, timedelta
import warnings
from skimage import feature
from image_registration.chi2_shifts import chi2_shift
from image_registration.fft_tools.shift import shiftnd, shift2d
from scipy.interpolate import interp2d, RectBivariateSpline, NearestNDInterpolator, griddata
from mpl_toolkits.axes_grid1 import make_axes_locatable

class Convert:

    def lat_degree_to_pixel(lat_dimensions, pixels_per_degree):
        return [(lat_dimensions[i] + 90) * pixels_per_degree for i in range(2)]

    def lon_degree_to_pixel(lon_dimensions, pixels_per_degree):
        return [lon_dimensions[i] * pixels_per_degree for i in range(2)]

    def dimensions_to_pixels(lat_dimensions, lon_dimensions, pixels_per_degree):
        return Convert.lat_degree_to_pixel(lat_dimensions, pixels_per_degree), Convert.lon_degree_to_pixel(lon_dimensions, pixels_per_degree)

    def pixels_to_degrees(indices, pixels_per_degree):
        lattitude = (indices[0] / pixels_per_degree) - 90 
        longitude = indices[1] / pixels_per_degree
        return longitude, lattitude