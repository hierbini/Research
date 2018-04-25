import numpy as np
import matplotlib.pyplot as plt
import tool_box as tb

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

    def plot_shifted_projection(self):
        shifted_projection = self.shift_projection()
        tb.plot_projection(self.image_name, self.planet, shifted_projection)
