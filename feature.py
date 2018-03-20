
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
from coordgrid import CoordGrid
#from Tool_Box import Convert


class CloudFeature:

    def __init__(self, coordgrid, feature_locator):
        self.coordgrid = coordgrid
        self.feature_locator = feature_locator

    def correct_planets_rotation(self, planet):
        ''' In the case that we need to compare two images, the images should be aligned. However, 
        due to time in between observations, one image may be shifted because of planetary rotation.
        This function returns something that corrects this rotation.'''

        '''
        use middle file for now
        '''
        
    def write_file(self, outfile):
        '''Adds to HDUlist of original image?'''
        hdulist_data = pyfits.PrimaryHDU(self.coordgrid.data, header = self.header)

class H_K_Fraction(CloudFeature):

    def __init__(self, neptune_infile, uranus_infile):
        self.neptune_infile = neptune_infile
        self.uranus_infile = uranus_infile

    def calculate_H_K_fraction(self, search_box, lat_dimensions, lon_dimensions):
        ''' This function will draw a box of specified longitudinal and latitudinal dimensions on the
        projected image and calculate the H/K fraction of each pixel within this box''' 
