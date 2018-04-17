import numpy as np
from coordgrid import *

class ProjectionShift:

    def __init__(self, image_name, planet, degrees_per_pixel, timeshift, projection):
        self.image_name = image_name
        self.planet = planet
        self.degrees_per_pixel = degrees_per_pixel
        self.time_shift = timeshift
        self.projection = projection
        self.degrees_per_second = self.calculate_degrees_per_second()

    def calculate_degrees_per_second(self):
        """ Returns planet's rotation rate in longitudinal degrees per second. """
        seconds_one_rotation = self.planet.rotation_time * 60 * 60
        degrees_per_second = 360 / seconds_one_rotation
        return degrees_per_second

    def shift_projection(self):
        pixel_shift = self.degrees_per_second * self.time_shift * (1 / self.degrees_per_pixel)
        return np.roll(self.projection, int(pixel_shift), axis = 1)

    def plot_shifted_projection(self, ctrlon = 180, lat_limits = (-90, 90), lon_limits = (0, 360), cbarlabel = 'Count'):
        shifted_projection = self.shift_projection()
        vmin, vmax = self.planet.vmin, self.planet.vmax
        fontsize = 14
        fig, ax0 = plt.subplots(1, 1, figsize=(10, 7))
        extent = [ctrlon - 180, ctrlon + 180, -90, 90]
        cim = ax0.imshow(shifted_projection, extent = extent, origin = 'lower left', cmap = 'gray', vmin = vmin, vmax = vmax)
        parallels = np.arange(lat_limits[0], lat_limits[1] + 30, 30.)
        meridians = np.arange(lon_limits[0], lon_limits[1] + 60, 60.)
        for loc in parallels:
            ax0.axhline(loc, color = 'cyan', linestyle = ':')
        for loc in meridians:
            ax0.axvline(loc, color = 'cyan', linestyle = ':')

        # plot lines intersecting
        ax0.set_xlabel('Longitude', fontsize = fontsize)
        ax0.set_ylabel('Latitude', fontsize = fontsize)
        ax0.set_ylim(lat_limits)
        ax0.set_xlim(lon_limits)
        ax0.set_title(self.image_name, fontsize = fontsize + 2)
        ax0.tick_params(which='both', labelsize = fontsize - 2)

        # plot the colorbar
        divider = make_axes_locatable(ax0)
        cax = divider.append_axes('right', size='5%', pad=0.05)
        cbar = fig.colorbar(cim, cax=cax, orientation='vertical')
        cbar.set_label(cbarlabel, fontsize=fontsize)
        cax.tick_params(which='both', labelsize=fontsize - 2)


