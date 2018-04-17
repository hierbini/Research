import pyfits
import datetime

class ShiftTime:

    def __init__(self, filepaths):
        assert len(filepaths) > 1, "Must have more than one image to find shift time."
        self.filepaths = filepaths
        self.timestamps = self.get_timestamps()

    def get_datetime_header(self, filepath):
        hdu = pyfits.open(filepath)
        headerdate = hdu[0].header['DATE-BEG']
        date, time = headerdate[0:10], headerdate[11:19]
        return date, time

    def create_datetime_instance(self, filepath):
        date, time = self.get_datetime_header(filepath)
        year, month, day = int(date[0:4]), int(date[5:7]), int(date[8:10])
        hour, minutes, seconds = int(time[0:2]), int(time[3:5]), int(time[6:8])
        return datetime.datetime(year, month, day, hour, minutes, seconds)

    def get_timestamps(self):
        datetimes = [self.create_datetime_instance(filepath) for filepath in self.filepaths]
        reference_date = datetime.datetime(1970, 8, 15, 6, 0, 0) #arbitrary reference date
        timestamps = [(date - reference_date).total_seconds() for date in datetimes]
        return timestamps

    def get_average_timestamp(self):
        total_seconds = sum(self.timestamps)
        average_timestamp = total_seconds/len(self.timestamps)
        return average_timestamp

    def shift_dictionary(self):
        '''Returns a dictionary of shifts corresponding to filename'''
        average_timestamp = self.get_average_timestamp()
        shift_dictionary = {}
        for i in range(len(self.filepaths)):
            shift_dictionary[self.filepaths[i][-14:]] = average_timestamp - self.timestamps[i]
        return shift_dictionary