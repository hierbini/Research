import coordgrid
from tool_box import Path, Projection
from planet_info import *

planet = NeptuneH()
H_path = Path('2017-08-31', planet.name + '_H').all_files_in_folder[4]
H_projection = Projection(H_path).load_projection_from_file(planet)
coords = coordgrid.CoordGrid(H_path, planet)
coords.plot_projected(H_projection)

