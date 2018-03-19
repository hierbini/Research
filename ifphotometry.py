import pyfits
import numpy as np
import glob
import matplotlib.pyplot as plt

def get_airm(filein, ext):
    hdulist = pyfits.open(path+filein+ext, errors='ignore', ignore_missing_end=True)
    hdr = hdulist[0].header
    airm = hdr['airmass']
    return airm

def get_coadds(filein, ext):
    hdulist = pyfits.open(path+filein+ext, errors='ignore', ignore_missing_end=True)
    hdr = hdulist[0].header
    coadds = hdr['coadds']
    return coadds

def get_tint(filein, ext):
    hdulist = pyfits.open(path+filein+ext, errors='ignore', ignore_missing_end=True)
    hdr = hdulist[0].header
    tint = hdr['itime']
    return tint

def airmass(airm1, airm2, tau):

    teff1 =tau*(airm1 - 1.0)
    teff2 =tau*(airm2 - 1.0)

    factor = (10**(teff2/2.5))/(10**(teff1/2.5))

    return factor

files = np.array(['n0064', 'n0067']) # list of files

ext = '.fits'
date = '2015-08-29'

path = '/home/josh/Documents/Data/Keck/'+date+'/data/'

### Relevant constants for Neptune/Nirc2 ###

r_odot = 30.10366151 # Neptune distance AU
pix = .009942 # Nirc 2 narrow camera pixel scale (arcsec/pixel)
pixel = pix*np.pi/(3600.*180.)
omega = pixel*pixel # solid angle



############################################

for f in files:
    hdulist = pyfits.open(path+f+ext, errors='ignore', ignore_missing_end=True)
    hdr = hdulist[0].header
    im = hdulist[0].data
    filt = hdr['filter'].rstrip()
    airm1 = hdr['airmass']
    coadds1 = hdr['coadds']
    tint1 = hdr['itime']

    if filt == 'H + clear':
        filehd = 'n0103' # Standard Star HD 1160
        tau = 0.059 # mag/airmass for H + clear

        airm2 = get_airm(filehd, ext)
        coadds2 = get_coadds(filehd, ext)
        tint2 = get_tint(filehd, ext)

        flux_hd = 1000 * 1.708e-12 # W/m2/um to erg/cm2/um
        counts = 5.580e6 # from photometry.pro, num counts/sec
        conv = flux_hd / counts /(coadds2 * tint2) 

        F_odot = 232223./np.pi # Solar flux parameter

    if filt == 'Kp + clear':
        filehd = 'n0107' # Standard Star HD 1160
        tau = 0.088 # mag/airmass for H + clear

        airm2 = get_airm(filehd, ext)
        coadds2 = get_coadds(filehd, ext)
        tint2 = get_tint(filehd, ext)

        flux_hd = 1000 * 6.983e-13 # W/m2/um to erg/cm2/um
        counts = 2.77625e06 # from photometry.pro, num counts/sec
        conv = flux_hd / counts / (coadds2 * tint2) 

        F_odot = 94773.6/np.pi # Solar flux parameter

    if filt == 'PK50_1.5 + Hcont':

        filehd = 'n0107' # Standard Star HD 1160
        tau = 0.088 # mag/airmass for H + clear

        airm2 = get_airm(filehd, ext)
        coadds2 = get_coadds(filehd, ext)
        tint2 = get_tint(filehd, ext)

        flux_hd = 1000 * 6.983e-13 # W/m2/um to erg/cm2/um
        counts = 2.77625e06 # from photometry.pro, num counts/sec
        conv = flux_hd / counts / (coadds2 * tint2) 

        F_odot = 94773.6/np.pi # Solar flux parameter

    factor = airmass(airm1, airm2, tau)
    im = factor*im
    im = im / (coadds1 * tint1)


    solarflux = F_odot/r_odot**2
    conversion = 1./omega*1./solarflux
    if_im = im * conv * conversion
    
    plt.imshow(if_im, cmap = 'gray', vmin = 0, vmax=1); plt.show()


