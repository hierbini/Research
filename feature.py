
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
from feature_locator import Feature_Locator
from Tool_Box import Convert


class CloudFeature:

    def __init__(self, coordgrid, feature_locator):
        self.coordgrid = coordgrid
        self.feature_locator = feature_locator

    def correct_rotation(self):
        ''' In the case that we need to compare two images, they should be temporally aligned. However, 
        due to time in between observations, we have to take into account planet's rotation. This function 
        returns something that corrects this rotation, allowing images to be aligned'''

class H_K_Fraction(CloudFeature):

    def __init__(self, neptune_infile, uranus_infile):
        self.neptune_infile = neptune_infile
        self.uranus_infile = uranus_infile

    def calculate_H_K_fraction(self, search_box, lat_dimensions, lon_dimensions):
        ''' This function will draw a box of specified longitudinal and lattitudinal dimensions on the
        projected image and calculate the H/K fraction of each pixel within this box''' 
