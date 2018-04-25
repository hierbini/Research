from feature import KHFraction
from feature_locator import *
import tool_box as tb
from planet_info import *
import save_paths as sp

planetH, planetK, date = NeptuneH(), NeptuneKs(), tb.choose_date()
H_path = sp.InfilePath(date, planetH).all_files_in_folder[2]
K_path = sp.InfilePath(date, planetK).all_files_in_folder[2]
H_projection = sp.SaveProjection(H_path).load_projection_from_file(planetH)
K_projection = sp.SaveProjection(K_path).load_projection_from_file(planetK)
H_deg_per_pix = sp.SaveCoordGrid(K_path).load_coordgrid(planetH)['degrees_per_pixel']
K_deg_per_pix = sp.SaveCoordGrid(K_path).load_coordgrid(planetK)['degrees_per_pixel']
H_feature_locator = FeatureLocator(H_deg_per_pix)
K_feature_locator = FeatureLocator(K_deg_per_pix)
K_H_fraction = KHFraction(H_feature_locator, K_feature_locator, H_projection, K_projection)
K_H_fraction.get_K_H_fractions_along_line()

#commit
