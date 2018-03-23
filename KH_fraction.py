from feature import KHFraction
from tool_box import Path, Optimizer
from planet_info import  Neptune, Uranus
import coordgrid

planet, date = Neptune(), '2017-08-31'
H_path = Path(date, planet.name + '_H').all_files_in_folder[2]
K_path = Path(date, planet.name + '_Ks').all_files_in_folder[2]
H_projection = Optimizer(H_path).load_pickled_data_from_file()
K_projection = Optimizer(K_path).load_pickled_data_from_file()
H_coordgrid = coordgrid.CoordGrid(H_path)
K_coordgrid = coordgrid.CoordGrid(K_path)

first = True
keep_going = True
K_H_fraction = KHFraction(H_coordgrid, K_coordgrid, H_projection, K_projection).calculate_K_H_fraction()
print(K_H_fraction)

