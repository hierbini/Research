import matplotlib.pyplot as plt
import coordgrid
from tool_box import Path

path = Path('2017-08-31', 'Neptune_H')
infile_path = path.path_to_infile()

#files = []

coords = coordgrid.CoordGrid(infile_path+'s0124_red.fits')
coords.edge_detect()
coords.project()
coords.plot_projected()

# to manipulate latitudes and longitudes, use coords.lat_g, coords.lon_e
#plt.imshow(coords.lat_g, origin = 'lower left')
#plt.show()

# to determine locations of bright features at first glance
#coords.locate_feature()
