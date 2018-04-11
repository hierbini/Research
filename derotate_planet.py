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

    def get_day_hour_minute(date, time):
        day = int(date[8:10])
        hour = int(time[0:2])
        minute = int(time[3:5])
        return day, hour, minute

    def get_time_in_order(H_date, H_time, K_date, K_time):
        H_day, H_hour, H_minute = DerotatePlanet.get_day_hour_minute(H_date, H_time)
        K_day, K_hour, K_minute = DerotatePlanet.get_day_hour_minute(K_date, K_time)

        if H_day == K_day:
            if K_hour == H_hour:
                if K_minute > H_minute:
                    return H_date, H_time, K_date, K_time
                else:
                    return K_date, K_time, H_date, H_time
            if H_hour > K_hour:
                return K_date, K_time, H_date, H_time
            else:
                return H_date, H_time, K_date, K_time
        if H_day > K_day:
            return K_date, K_time, H_date, H_time
        else:
            return H_date, H_time, K_date, K_time

    def find_time_between_images(begin_date, begin_time, end_date, end_time):
        begin_day, begin_hour, begin_minute = DerotatePlanet.get_day_hour_minute(begin_date, begin_time)
        end_day, end_hour, end_minute = DerotatePlanet.get_day_hour_minute(end_date, end_time)
        minute_difference = 0

        if begin_day == 1 and end_day == 31:
            begin_day = 31
            end_day = 30
        elif end_day == 1 and begin_day == 31:
            end_day = 31
            begin_day = 30
        if begin_hour == 12:
            begin_day -= 1
        if end_hour == 12:
            end_day -= 1

        if end_hour < begin_hour:
            end_hour = end_hour + 12
        minute_difference = end_minute - begin_minute
        return 60 * abs(end_hour - begin_hour) + minute_difference

    def get_correction_time(self):
        H_date, H_time = DerotatePlanet.get_date_and_time(self.H_path)
        K_date, K_time = DerotatePlanet.get_date_and_time(self.K_path)
        time_between_images = DerotatePlanet.find_time_between_images(H_date, H_time, K_date, K_time)
        correction_time = time_between_images / 2
        return correction_time

    def correct_projection(self):
        correction_time = self.get_correction_time()
        degrees_to_shift = self.degrees_per_minute * correction_time

