from planet_info import *
from coordgrid import *
from tool_box import *
import pyfits

class DerotatePlanet:

    def __init__(self, planet, A_coordgrid, B_coordgrid):
        self.planet = planet
        self.A_coordgrid = A_coordgrid
        self.B_coordgrid = B_coordgrid
        self.A_path = self.A_coordgrid.infile_path
        self.B_path = self.B_coordgrid.infile_path
        self.A_date, self.A_time = DerotatePlanet.get_date_and_time(self.A_path)
        self.B_date, self.B_time = DerotatePlanet.get_date_and_time(self.B_path)
        self.degrees_per_minute = self.calculate_degrees_per_minute()


    def calculate_degrees_per_minute(self):
        """ Returns planet's rotation rate in longitudinal degrees per minute. """
        minutes_one_rotation = self.planet.rotation_time * 60
        degrees_per_minute = minutes_one_rotation / 360
        return degrees_per_minute

    def get_date_and_time(file):
        hdu = pyfits.open(file)
        headerdate = hdu[0].header['DATE-BEG']
        return DerotatePlanet.get_date(headerdate), DerotatePlanet.get_time(headerdate)

    def get_date(headerdate):
        return headerdate[0:10]

    def get_time(headerdate):
        return headerdate[11:16]

    def get_day_hour(date, time):
        day = int(date[8:10])
        hour = int(time[0:2])
        return day, hour

    def get_minutes_seconds(time):
        minutes = int(time[3:5])
        seconds = int(time[6:8])
        return minutes, seconds

    def order_AB_date_time(A_date, A_time, B_date, B_time):
        A_day, A_hour = DerotatePlanet.get_day_hour(A_date, A_time)
        A_minutes, A_seconds = DerotatePlanet.get_minutes_seconds(A_time)
        B_day, B_hour = DerotatePlanet.get_day_hour(B_date, B_time)
        B_minutes, B_seconds = DerotatePlanet.get_minutes_seconds(B_time)

        if A_day == 1:
            A_day = 31
            B_day = 30
        if B_day == 1:
            A_day = 30
            B_day = 31

        if A_day == B_day:
            if B_hour == A_hour:
                if B_minutes > A_minutes:
                    return A_date, A_time, B_date, B_time
                else:
                    return B_date, B_time, A_date, A_time
            if A_hour > B_hour:
                return B_date, B_time, A_date, A_time
            else:
                return A_date, A_time, B_date, B_time
        if A_day > B_day:
            return B_date, B_time, A_date, A_time
        else:
            return A_date, A_time, B_date, B_time

    def get_time_between_images(begin_date, begin_time, end_date, end_time):
        begin_day, begin_hour = DerotatePlanet.get_day_hour(begin_date, begin_time)
        begin_minutes, begin_seconds = DerotatePlanet.get_minutes_seconds(begin_time)
        end_day, end_hour, end_minute = DerotatePlanet.get_day_hour(end_date, end_time)
        end_minutes, begin_seconds = DerotatePlanet.get_minutes_seconds(begin_time)

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
        minute_difference = (end_minutes + end_seconds/60) - (begin_minutes + begin_seconds/60)
        return 60 * abs(end_hour - begin_hour) + minute_difference

    def get_correction_time(self):
        begin_date, begin_time, end_date, end_time = DerotatePlanet.order_AB_date_time(self.A_date, self.A_time, self.B_date, self.B_time)
        time_between_images = DerotatePlanet.get_time_between_images(begin_date, begin_time, end_date, end_time)
        correction_time = time_between_images / 2
        return correction_time

    def correct_projection(self):
        correction_time = self.get_correction_time()
        degrees_to_shift = self.degrees_per_minute * correction_time

