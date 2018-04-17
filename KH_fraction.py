from feature import KHFraction
from tool_box import InfilePath, Projection
from planet_info import  Neptune, Uranus
import coordgrid

planet, date = Neptune(), '2017-07-06'
H_path = InfilePath(date, planet.name + '_H').all_files_in_folder[2]
K_path = InfilePath(date, planet.name + '_Ks').all_files_in_folder[2]
H_projection = Projection(H_path).load_projection_from_file()
K_projection = Projection(K_path).load_projection_from_file()
H_coordgrid = coordgrid.CoordGrid(H_path)
K_coordgrid = coordgrid.CoordGrid(K_path)
K_H_fraction = KHFraction(H_coordgrid, K_coordgrid, H_projection, K_projection).calculate_K_H_fraction()

#commit
