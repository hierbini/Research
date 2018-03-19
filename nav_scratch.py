#from nirc2_reduce import coordgrid

import sys
import os
import matplotlib.pyplot as plt

#pathcode = os.path.expanduser('/home/josh/Documents/Code/Nav/')
#sys.path.append(pathcode)

path = 'C:/Users/nguye/ResearchLab/Data/Lick/Data_Again/Reduced/'
date = '2017-08-31' 
fullpath = path + date + '/Neptune_H/'

import coordgrid

files = []

coords = coordgrid.CoordGrid(fullpath+'s0124_red.fits')
coords.edge_detect()
coords.plot_latlon()
coords.project()
coords.plot_projected()
#coords.write_latlon(fullpath + 's0231_test.fits')

# to manipulate latitudes and longitudes, use coords.lat_g, coords.lon_e
#plt.imshow(coords.lat_g, origin = 'lower left')
plt.show()

# to determine locations of bright features at first glance
#coords.locate_feature()
