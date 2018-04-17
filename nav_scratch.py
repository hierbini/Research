from coordgrid import *
from save_paths import *
from planet_info import *

planet = NeptuneH()
H_path = InfilePath('2017-08-07', planet).all_files_in_folder[3]
H_projection = SaveProjection(H_path).load_projection_from_file(planet)
print(H_projection)
coords = coordgrid.CoordGrid(H_path, planet)
coords.plot_projected(H_projection)

