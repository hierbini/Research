import save_paths as sp
from planet_info import *
from shift_projection import *
import tool_box as tb

planet, date = tb.choose_folder()
paths = tb.get_all_paths(date, planet)
for path in paths:
    filename = tb.get_filename(path)
    projection = sp.SaveProjection(path).load_projection_from_file(planet)
    tb.plot_projection(filename, planet.vmin, planet.vmax, projection)

for path in paths:
    sp.SaveCoordGrid(path).load_coordgrid(planet)
