from planet_shift_time import *
from planet_shift import *
from tool_box import *
from planet_info import *
import coordgrid

planet_band, date = NeptuneH(), '2017-08-31'
paths = [Path(date, planet_band.name + '_H').all_files_in_folder[i] for i in range(4)]
coordgrids = [coordgrid.CoordGrid(path, planet_band) for path in paths]
projections = [Projection(path).load_projection_from_file(planet_band) for path in paths]

shift_time = ShiftTime(paths)
shift_dictionary = shift_time.shift_dictionary()

shiftprojections = []

for i in range(len(paths)):
    image_name = paths[i][-14:]
    degrees_per_pixel = coordgrids[i].deg_per_px
    timeshift = shift_dictionary[image_name]
    projection = projections[i]
    shiftprojections.append(ProjectionShift(image_name, planet_band, degrees_per_pixel, timeshift, projection))
