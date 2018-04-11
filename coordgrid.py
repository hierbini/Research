#!/usr/bin/env python

import sys
sys.path.append("C:\\Python36\\lib")
sys.path.append("C:\\Python36\\lib\\site-packages")
import pyfits
import numpy as np
import matplotlib.pyplot as plt
from get_ephem import get_ephemerides, naif_lookup
from image import Image
from datetime import datetime, timedelta
import warnings
from skimage import feature
from image_registration.chi2_shifts import chi2_shift
from image_registration.fft_tools.shift import shift2d
from scipy.interpolate import griddata
from mpl_toolkits.axes_grid1 import make_axes_locatable
from feature_locator import FeatureLocator, CloudLocator
from tool_box import Projection
import planet_info

def lat_lon(x, y, ob_lon, ob_lat, pixscale_km, np_ang, req, rpol):
    '''Find latitude and longitude on planet given x,y pixel locations and
    planet equatorial and polar radius'''
    np_ang = -np_ang
    x1 = pixscale_km*(np.cos(np.radians(np_ang))*x - np.sin(np.radians(np_ang))*y)
    y1 = pixscale_km*(np.sin(np.radians(np_ang))*x + np.cos(np.radians(np_ang))*y)
    olrad = np.radians(ob_lat)
    
    #set up quadratic equation for ellipsoid
    r2 = (req/rpol)**2
    a = 1 + r2*(np.tan(olrad))**2 #second order
    b = 2*y1*r2*np.sin(olrad) / (np.cos(olrad)**2) #first order
    c = x1**2 + r2*y1**2 / (np.cos(olrad))**2 - req**2 #constant

    radical = b**2 - 4*a*c
    #will equal nan outside planet since radical < 0
    with warnings.catch_warnings():
        warnings.simplefilter("ignore") #suppresses error for taking sqrt nan
        x3s1=(-b+np.sqrt(radical))/(2*a)
        x3s2=(-b-np.sqrt(radical))/(2*a)
    z3s1=(y1+x3s1*np.sin(olrad))/np.cos(olrad)
    z3s2=(y1+x3s2*np.sin(olrad))/np.cos(olrad)
    odotr1=x3s1*np.cos(olrad)+z3s1*np.sin(olrad)
    odotr2=x3s2*np.cos(olrad)+z3s2*np.sin(olrad)
    #the two solutions are front and rear intersections with planet
    #only want front intersection
    
    #tricky way of putting all the positive solutions into one array
    with warnings.catch_warnings():
        warnings.simplefilter("ignore") #suppresses error for taking < nan
        odotr2[odotr2 < 0] = np.nan
        x3s2[odotr2 < 0] = np.nan
        z3s2[odotr2 < 0] = np.nan
        odotr1[odotr1 < 0] = odotr2[odotr1 < 0]
        x3s1[odotr1 < 0] = x3s2[odotr1 < 0]
        z3s1[odotr1 < 0] = z3s2[odotr1 < 0]
    
    odotr,x3,z3 = odotr1,x3s1,z3s1
    y3 = x1
    r = np.sqrt(x3**2 + y3**2 + z3**2)
    
    #lon_e = np.degrees(np.arctan(y3/x3)) + ob_lon
    lon_e = np.degrees(np.arctan2(x3,y3)-np.pi/2) + ob_lon 
    with warnings.catch_warnings():
        warnings.simplefilter("ignore") #suppresses error for taking < nan
        lon_e[lon_e < 0] += 360
    lat_c = np.degrees(np.arcsin(z3/r))
    lat_g = np.degrees(np.arctan(r2*np.tan(np.radians(lat_c))))
    #plt.imshow(lon_e, origin = 'lower left')
    #plt.show()
    return lat_g, lat_c, lon_e

def surface_normal(lat_g, lon_e, ob_lon):
    '''Returns the normal vector to the surface of the planet.
    Take dot product with sub-obs or sub-sun vector to find cosine of emission angle'''
    nx = np.cos(np.radians(lat_g))*np.cos(np.radians(lon_e-ob_lon))
    ny = np.cos(np.radians(lat_g))*np.sin(np.radians(lon_e-ob_lon))
    nz = np.sin(np.radians(lat_g))
    return np.asarray([nx,ny,nz])

def emission_angle(ob_lat, surf_n):
    '''Return the cosine of the emission angle of surface wrt observer'''
    ob = np.asarray([np.cos(np.radians(ob_lat)), 0 , np.sin(np.radians(ob_lat))])
    return np.dot(surf_n.T,ob)

class CoordGrid:
    
    def __init__(self, infile, planet_band, centered = False):
        '''Pull ephemeris data, calculate lat and lon'''
        self.infile_path = infile
        self.im = Image(infile)
        self.hdulist = self.im.hdulist
        self.header = pyfits.getheader(infile)
        self.req = planet_band.equatorial_radius
        self.rpol = planet_band.polar_radius
        self.data = self.im.data
        self.cen = centered
        self.pixscale_arcsec = planet_band.pixel_scale
        
        #pull and reformat header info
        targ = self.im.header['OBJECT'].split('_')[0]
        targ = targ.split(' ')[0]
        self.target = targ

        date = self.im.header['DATE-OBS']#.split('T')[0] # Date Obs doesn't work for Lick
        try:
            expstart = self.im.header['EXPSTART'] ### Be wary of Lick header info being wrong!
        except KeyError:
            expstart = self.im.header['TIME-OBS'] ### use this for ALMA: self.im.header['DATE-OBS'].split('T')[1]

        imsize_x = self.data.shape[0]
        imsize_y = self.data.shape[1]
        tstart = datetime.strptime(date +' '+expstart[:5],'%Y-%m-%d %H:%M')
        tend = tstart + timedelta(minutes=1)
        tstart = datetime.strftime(tstart, '%Y-%m-%d %H:%M')
        tend = datetime.strftime(tend, '%Y-%m-%d %H:%M')
        
        #pull ephemeris data
        naif = naif_lookup(targ)
        ephem = get_ephemerides(naif, 568, tstart, tend, '1 minutes')[0][0] #just the row for start time
        print(ephem)
        ephem = [val.strip(' ') for val in ephem]
        time = ephem[0]
        ra, dec = ephem[3], ephem[4]
        dra, ddec = float(ephem[5]), float(ephem[6])
        az, el = float(ephem[7]), float(ephem[8])
        try:
            airmass, extinction = float(ephem[9]), float(ephem[10])
        except ValueError:
            airmass, extinction = 'n.a.', 'n.a.'
        apmag, sbrt = float(ephem[11]), float(ephem[12])
        ang_diam = float(ephem[15])
        self.ob_lon, self.ob_lat = float(ephem[16]), float(ephem[17])
        self.sun_lon, self.sun_lat = float(ephem[18]), float(ephem[19])
        self.np_ang, self.np_dist = float(ephem[20]), float(ephem[21])
        self.dist = float(ephem[22])*1.496e8 #from AU to km        
        self.date_time = tstart

        self.pixscale_km = self.dist*np.radians(pixscale/3600)
        avg_circumference = 2*np.pi*((req + rpol)/2.0)
        self.deg_per_px = self.pixscale_km * (1/avg_circumference) * 360 #approximate conversion between degrees and pixels at sub-observer point

        xcen, ycen = int(imsize_x/2), int(imsize_y/2) #pixels at center of planet

        xx = np.arange(imsize_x) - xcen
        yy = np.arange(imsize_y) - ycen
        x, y = np.meshgrid(xx, yy)
        self.lat_g, self.lat_c, self.lon_e = lat_lon(x, y, self.ob_lon, self.ob_lat, self.pixscale_km, self.np_ang, req,rpol)

        self.surf_n = surface_normal(self.lat_g, self.lon_e, self.ob_lon)
        self.mu = emission_angle(self.ob_lat, self.surf_n)
        
        self.feature_locator = FeatureLocator(self)
        self.cloud_locator = CloudLocator(self)

    def edge_detect(self, low_thresh = 0.01, high_thresh = 0.05, sigma = 3, plot = False, xs = 500 ,ys = 700, s = 500):
        '''Uses skimage canny algorithm to find edges of planet, correlates
        that with edges of model, '''
        self.model_planet = np.nan_to_num(self.lat_g * 0.0 + 1.0)

        imdata = np.zeros((2048, 2048))
        imdata[xs:xs+s, ys:ys+s] = self.data[xs:xs+s, ys:ys+s]
        
        model_edges = feature.canny(self.model_planet, sigma=sigma, low_threshold = low_thresh, high_threshold = high_thresh)
        edges = feature.canny(imdata/np.max(imdata), sigma=sigma, low_threshold = low_thresh, high_threshold = high_thresh)

    
        [dx, dy, dxerr, dyerr] = chi2_shift(model_edges, edges)
        self.dx = dx #need these if we want to shift another filter the same amount
        self.dy = dy

        self.centered = shift2d(self.data,-1*dx,-1*dy)
        self.edges = shift2d(edges,-1*dx,-1*dy)
        self.data_shifted = shift2d(imdata, -1*dx, -1*dy)

        if plot:
            fig, (ax0, ax1, ax2) = plt.subplots(1, 3, figsize=(10, 5))
            ax0.imshow(imdata, origin = 'lower left', vmin = 0, vmax = 1000)
            ax0.set_title('Imdata')
            ax1.imshow(self.model_planet, origin = 'lower left')
            ax1.set_title('Model Planet')
            ax2.imshow(self.data_shifted, origin = 'lower left', vmin=0, vmax=1000)
            ax2.set_title('Image')
            plt.show()
        
    def plot_latlon(self):
        '''Make pretty plot of lat_g and lon_e overlaid on planet'''

        if self.cen:
        # Data already centered, so no need to call edge detect
            self.centered = self.data
            self.model_planet = np.nan_to_num(self.lat_g * 0.0 + 1.0)


        fig, (ax0, ax1) = plt.subplots(1,2, figsize = (12,6))
        
        #latitudes
        ax0.imshow(self.centered, origin = 'lower left', vmin=0.0, vmax=1000, cmap='jet')
        levels_lat = np.arange(-90,105,15)
        label_levels_lat = np.arange(-90,60,30)
        ctr_lat = ax0.contour(self.lat_g, levels_lat, colors='white', linewidths=1)
        ax0.clabel(ctr_lat, label_levels_lat, inline=1, inline_spacing = 2, fontsize=12, fmt='%d')
        ax0.contour(self.model_planet, colors = 'white', linewidths = 1)
        #ax0.set_title('Latitudes', fontsize = 18)
        ax0.get_xaxis().set_ticks([])
        ax0.axes.get_yaxis().set_ticks([])
        
        #longitudes
        ax1.imshow(self.centered, origin = 'lower left', vmin = 1, vmax = 1000)
        # removed cmap='gist_rainbow'
        #hack here to avoid discontinuity in contours - split longs in half
        with warnings.catch_warnings():
            warnings.simplefilter("ignore") #suppresses error for taking < nan
            lon_e1 = np.copy(self.lon_e)
            lon_e1[lon_e1 >= 180] = np.nan
            lon_e2 = np.copy(self.lon_e)
            lon_e2[lon_e2 < 180] = np.nan
        
        levels_lon = range(0,360,30)
        levels_lon_hack = [1] + list(levels_lon[1:]) #make contour at zero actually 1 - otherwise won't plot it since it's at the edge
        ctr_lon1 = ax1.contour(lon_e1, levels_lon_hack, colors='white', linewidths=1)
        ctr_lon2 = ax1.contour(lon_e2, levels_lon_hack, colors='white', linewidths=1)
                
        fmt = {}
        vals = np.arange(0,360,30)
        for l, v in zip(levels_lon_hack, vals):
            fmt[l] = str(int(v)) #make it so the labels say the right things despite hack
        ax1.clabel(ctr_lon1, levels_lon_hack, fmt = fmt, inline=1, inline_spacing = 2, fontsize=12)
        ax1.clabel(ctr_lon2, levels_lon_hack, fmt = fmt, inline=1, inline_spacing = 2, fontsize=12)
        ax1.contour(self.model_planet, colors = 'white', linewidths = 1)
        #ax1.set_title('Longitudes', fontsize = 18)
        ax1.get_xaxis().set_ticks([])
        ax1.axes.get_yaxis().set_ticks([])        
                
        plt.tight_layout()
        #plt.savefig('lat_lon_overlay.png')
        plt.show()
      
    def write_latlon(self, outfile):
        lat = self.lat_g
        lon = self.lon_e

        hdulist_data = pyfits.PrimaryHDU(self.data, header = self.header)
        hdulat = pyfits.ImageHDU(lat, name='LAT')
        hdulon = pyfits.ImageHDU(lon, name='LON')

        #hdulist_out[0].data = self.centered
        #hdulist_out[0].writeto(outfile)

        hdulist = pyfits.HDUList([hdulist_data, hdulat, hdulon])
        hdulist.writeto(outfile, clobber='True')
        #hdulist_out[1].writeto(outfile)
        #hdulist_out[2].header['OBJECT'] = self.im.target+'_LONGITUDES'

        #hdulist_out[2].writeto(outfile)

    def project(self, outstem = 'h', pixsz = None, interp = 'cubic', writefile = False):
        '''Project the data onto a flat x-y grid.
        pixsz is in arcsec. if pixsz = None, translates the pixel scale
        of the image to a distance at the sub-observer point.
        interp asks whether to regrid using a nearest neighbor, linear, or cubic'''
        
        #determine the number of pixels in resampled image
        if pixsz == None:
            pixsz = self.pixscale_arcsec
        npix_per_degree = (1/self.deg_per_px) * (pixsz / self.pixscale_arcsec) # (old pixel / degree lat) * (arcsec / old pixel) / (arcsec / new pixel) = new pixel / degree lat
        npix = int(npix_per_degree * 180) + 1 #(new pixel / degree lat) * (degree lat / planet) = new pixel / planet
        print('New image will be %d by %d pixels'%(2*npix + 1, npix))
        print('Pixel scale %f km = %f pixels per degree'%(self.pixscale_km, npix_per_degree))
        
        #create new lon-lat grid
        extra_wrap_dist = 180
        newlon, newlat = np.arange(-extra_wrap_dist,360 + extra_wrap_dist, 1/npix_per_degree), np.arange(-90,90, 1/npix_per_degree)
        gridlon, gridlat = np.meshgrid(newlon, newlat)
        nans = np.isnan(self.lon_e.flatten())
        def input_helper(arr, nans):
            '''removing large region of NaNs speeds things up significantly'''
            return arr.flatten()[np.logical_not(nans)]
        inlon, inlat, indat, inmu = input_helper(self.lon_e, nans), input_helper(self.lat_g, nans), input_helper(self.centered, nans), input_helper(self.mu, nans)

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
        
    def plot_projected(self, projection, ctrlon = 180, lat_limits = [-90, 90], lon_limits = [0, 360], cbarlabel = 'Count', vmin = 0, vmax = 800):
        '''Once projection has been run, plot it using this function'''  
        ### remember to add back outfname, after ctr
        
        #apply center longitude to everything

        newim = projection
        if newim == []:
            npix, npix_per_degree = self.projected.shape[1], 1.0 / self.deg_per_px
            print(npix_per_degree)
            offset = (ctrlon + 180)%360
            offsetpix = int(np.round(offset*npix_per_degree))
            uoffsetpix = npix - offsetpix
            newim = np.copy(self.projected)
            lefthalf = self.projected[:,:offsetpix]
            righthalf = self.projected[:,offsetpix:]
            newim[:,uoffsetpix:] = lefthalf #switch left and right halves
            newim[:,:uoffsetpix] = righthalf
    
            projection_data = Projection(self.infile_path)
            projection_data.save_projection(newim)

        first = True
        keep_going = 'y'

        while keep_going == 'y':
            if first:
                print('Hello, this is where you define the dimensions of your box!')
                first = False
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
            self.cloud_locator.plot_cloud_center(newim)
            
            #plot the colorbar
            divider = make_axes_locatable(ax0)
            cax = divider.append_axes('right', size='5%', pad=0.05)
            cbar = fig.colorbar(cim, cax = cax, orientation = 'vertical')
            cbar.set_label(cbarlabel, fontsize = fs)
            cax.tick_params(which = 'both', labelsize = fs - 2)
            
            #plt.savefig(outfname, bbox = None)
            plt.show()
            keep_going = input('Do you want to find a different coordinate? (y/n): ')
            print('------------------------------------------------------')

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
