import matplotlib.pyplot as plt
import coordgrid
from tool_box import Path, Projection

H_path = Path('2017-07-08', 'Neptune_H').all_files_in_folder[2]
H_projection = Projection(H_path).load_projection_from_file()
coords = coordgrid.CoordGrid(H_path)
coords.plot_projected(H_projection)

# to manipulate latitudes and longitudes, use coords.lat_g, coords.lon_e
#plt.imshow(coords.lat_g, origin = 'lower left')
#plt.show()

# to determine locations of bright features at first glance
#coords.locate_feature()
