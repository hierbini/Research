from planet_info import *
from coordgrid import *
from tool_box import *
import pyfits

class DerotatePlanet:

    def __init__(self, planet, H_coordgrid, K_coordgrid):
        self.planet = planet
        self.H_coordgrid = H_coordgrid
        self.K_coordgrid = K_coordgrid
        self.H_path = self.H_coordgrid.infile_path
        self.K_path = self.K_coordgrid.infile_path
        self.degrees_per_minute = self.calculate_degrees_per_minute()

    def calculate_degrees_per_minute(self):
        """ Returns planet's rotation rate in longitudinal degrees per minute. """
        minutes_one_rotation = self.planet.rotation_time * 60
        degrees_per_minute = minutes_one_rotation / 360
        return degrees_per_minute

    def get_date_and_time(file):
        hdu = pyfits.open(file)
        headerdate = hdu[0].header['DATE-BEG']
        return (DerotatePlanet.get_date(headerdate), DerotatePlanet.get_time(headerdate))

    def get_date(headerdate):
        return headerdate[0:10]

    def get_time(headerdate):
        return headerdate[11:16]

    def get_month_day_hour_minute(date, time):
        month = int(date[5:7])
        day = int(date[8:10])
        hour = int(time[0:2])
        minute = int(time[3:5])
        return month, day, hour, minute

    def find_time_between_images(H_date, H_time, K_date, K_time):
        H_month, H_day, H_hour, H_minute = DerotatePlanet.get_month_day_hour_minute(H_date, H_time)
        K_month, K_day, K_hour, K_minute = DerotatePlanet.get_month_day_hour_minute(K_date, K_time)
        max_hour, min_hour = max(K_hour, H_hour), min(K_hour, H_hour)
        minute_difference = 0

        if H_day == K_day:
            if H_hour > K_hour:
                minute_difference = K_minute - H_minute
            else:
                minute_difference = H_minute - K_minute
            return abs(60 * (max_hour - min_hour) - minute_difference)
        elif H_day > K_day:
             minute_difference = K_minute - H_minute
        elif K_day > H_day:
             minute_difference = H_minute - K_minute
        max_hour, min_hour = min_hour + 12, max_hour
        return abs(60 * (max_hour - min_hour) - minute_difference)

    def get_correction_time(self):
        H_date, H_time = DerotatePlanet.get_date_and_time(self.H_path)
        K_date, K_time = DerotatePlanet.get_date_and_time(self.K_path)
        time_between_images = DerotatePlanet.find_time_between_images(H_date, H_time, K_date, K_time)
        correction_time = time_between_images / 2
        return correction_time

    def correct_projection(self):
        correction_time = self.get_correction_time()
        degrees_to_shift = self.degrees_per_minute * correction_time

