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
from tool_box import Convert

class Projection(CoordGrid):

	def __init__(self):
		self.degrees_per_pixel = CoordGrid.deg_per_px
		self.pixels_per_degree = (1.0 / degrees_per_pixel) * (pixel_size / self.pixels_per_acrsecond)
		self.pixels_per_acrsecond = CoordGrid.pixscale_arcsec

	def image_pixel_dimensions(self, pixel_size = None):
		"""pixel_size is in arcseconds. if pixel_size = None, translates the pixel scale
    	of the image to a distance at the sub-observer point."""
		if pixel_size == None:
			pixel_size = self.pixels_per_acrsecond
		total_pixels = int(self.pixels_per_degree * 180) + 1
		image_width, image_height = 2 * total_pixels + 1, total_pixels 
    	return image_width, image_height

    def create_lonlat_grid(self):
    	extra_wrap_dist = 180
    	min_lon, max_lon = -extra_wrap_dist, 360 + extra_wrap_dist
    	min_lat, max_lat = -90, 90
        newlon, newlat = np.arange(min_lon, max_lon, 1 / pixels_per_degree), np.arange(min_lat, max_lat, 1 / pixels_per_degree)
        gridlon, gridlat = np.meshgrid(newlon, newlat)
        nans = np.isnan(self.lon_e.flatten())

        def input_helper(arr, nans):
            '''removing large region of NaNs speeds things up significantly'''
            return arr.flatten()[np.logical_not(nans)]

        inlon, inlat = input_helper(self.lon_e, nans), input_helper(self.lat_g, nans)
        indat, inmu = input_helper(self.centered, nans), input_helper(self.mu, nans)

        #fix wrapping by adding dummy copies of small lons at > 360 lon
        inlon_near0 = inlon[inlon < extra_wrap_dist]
        inlon_near0 += 360
        inlon_near360 = inlon[inlon > 360 - extra_wrap_dist]
        inlon_near360 -= 360
        inlon_n = np.concatenate((inlon_near360, inlon, inlon_near0))
        inlat_n = np.concatenate((inlat[inlon > 360 - extra_wrap_dist], inlat, inlat[inlon < extra_wrap_dist]))
        indat_n = np.concatenate((indat[inlon > 360 - extra_wrap_dist], indat, indat[inlon < extra_wrap_dist]))
        inmu_n = np.concatenate((inmu[inlon > 360 - extra_wrap_dist], inmu, inmu[inlon < extra_wrap_dist]))

        #do the regridding
        datsort = griddata((inlon_n, inlat_n), indat_n, (gridlon, gridlat), method = interp)
        musort = griddata((inlon_n, inlat_n), inmu_n, (gridlon, gridlat), method = interp)

        #trim extra data we got from wrapping
	    wrap_i_l = len(gridlon[0][gridlon[0] < 0]) - 1
	    wrap_i_u = len(gridlon[0][gridlon[0] >= 360])
	    datsort = datsort[:,wrap_i_l:-wrap_i_u]
	    musort = musort[:,wrap_i_l:-wrap_i_u]
	    gridlon = gridlon[:,wrap_i_l:-wrap_i_u]
	    gridlat = gridlat[:,wrap_i_l:-wrap_i_u]

        return gridlon, gridlat, datsort, musort

	def project(self, outstem = 'h', pixsz = None, interp = 'cubic', writefile = False):
        '''Project the data onto a flat x-y grid. interp asks whether to regrid using a nearest 
        neighbor, linear, or cubic'''

        image_width, image_height = self.image_pixel_dimensions()
        print('New image will be %d by %d pixels'%(image_width, image_height))
        print('Pixel scale %f km = %f pixels per degree'%(CoordGrid.pixscale_km, self.pixels_per_degree))
        gridlon, gridlat, datsort, musort = self.create_lonlat_grid()
        
        # make far side of planet into NaNs
        snorm = surface_normal(gridlat, gridlon, self.ob_lon)
        emang = emission_angle(self.ob_lat, snorm).T
        farside = np.where(emang < 0.0)
        datsort[farside] = np.nan
        musort[farside] = np.nan
        self.projected = datsort
        self.projected_mu = musort

        #write data to fits file   
        if writefile: 
            hdulist_out = self.im.hdulist
            hdulist_out[0].header['OBJECT'] = self.target+'_projected'
            hdulist_out[0].data = datsort
            hdulist_out[0].writeto(outstem + '_proj.fits', overwrite=True)
            print('Writing file %s'%outstem + '_proj.fits')
        
    def plot_projected(self, ctrlon = 180, lat_limits = [-90, 90], lon_limits = [0, 360], cbarlabel = 'Count', vmin = 0, vmax = 800):
        '''Once projection has been run, plot it using this function'''  
        ### remember to add back outfname, after ctr
        
        #apply center longitude to everything
        total_pixels, pixels_per_degree = self.projected.shape[1], 1.0 / self.deg_per_px
        print(pixels_per_degree)
        offset = (ctrlon + 180)%360
        offsetpix = int(np.round(offset*pixels_per_degree))
        uoffsetpix = npix - offsetpix
        newim = np.copy(self.projected)
        lefthalf = self.projected[:,:offsetpix]
        righthalf = self.projected[:,offsetpix:]
        newim[:,uoffsetpix:] = lefthalf #switch left and right halves
        newim[:,:uoffsetpix] = righthalf
          
        #plot it
        fs = 14 #fontsize for plots
        fig, ax0 = plt.subplots(1,1, figsize = (10,7))
        extent = [ctrlon - 180, ctrlon + 180, -90, 90]
        cim = ax0.imshow(newim, extent = extent, origin = 'lower left', cmap = 'gray', vmin = vmin, vmax = vmax)
        parallels = np.arange(lat_limits[0],lat_limits[1] + 30, 30.)
        meridians = np.arange(lon_limits[0],lon_limits[1] + 60, 60.)
        for loc in parallels:
            ax0.axhline(loc, color = 'cyan', linestyle = ':')
        for loc in meridians:
            ax0.axvline(loc, color = 'cyan', linestyle = ':')
        
        #plot lines intersecting
        ax0.set_xlabel('Longitude', fontsize = fs)
        ax0.set_ylabel('Latitude', fontsize = fs)
        ax0.set_ylim(lat_limits)
        ax0.set_xlim(lon_limits)
        ax0.set_title(self.date_time, fontsize = fs + 2)
        ax0.tick_params(which = 'both', labelsize = fs - 2)

        #Plot cloud center
        self.cloud_locator.plot_cloud_center()
        
        #plot the colorbar
        divider = make_axes_locatable(ax0)
        cax = divider.append_axes('right', size='5%', pad=0.05)
        cbar = fig.colorbar(cim, cax = cax, orientation = 'vertical')
        cbar.set_label(cbarlabel, fontsize = fs)
        cax.tick_params(which = 'both', labelsize = fs - 2)
        
        #plt.savefig(outfname, bbox = None)
        plt.show()

    def write_latlon_projec(self, outfile):
        lat = self.lat_g
        lon = self.lon_e
        mu = self.mu
        proj = self.projected
        projmu = self.projected_mu

        hdulist_data = pyfits.PrimaryHDU(self.data, header = self.header)
        hdulat = pyfits.ImageHDU(lat, name='LAT')
        hdulon = pyfits.ImageHDU(lon, name='LON')
        hdumu = pyfits.ImageHDU(mu, name='EMI')
        hduproj = pyfits.ImageHDU(proj, name='PROJ')
        hduprojmu = pyfits.ImageHDU(projmu, name='PROJMU')

        hdulist = pyfits.HDUList([hdulist_data, hdulat, hdulon, hdumu, hduproj, hduprojmu])
        hdulist.writeto(outfile, clobber='True')

    def add_proj(frames):


        frame_sum = np.zeros(frames[0].shape)

        for frame in frames:

            frame_sum = frame_sum + frame

        return frame_sum
        
        
