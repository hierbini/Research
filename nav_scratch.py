from save_paths import *
from planet_info import *
from projection_functions import *
import tool_box as tb

planet = NeptuneH()
path = InfilePath('2017-08-07', planet).all_files_in_folder[4]
filename = tb.get_filename(path)
projection = SaveProjection(path).load_projection_from_file(planet)
plot_projection(filename, planet, projection)
