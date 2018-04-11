import unittest
from derotate_planet import *
from planet_info import *
from coordgrid import *
from tool_box import *
import pyfits

class TestDerotatePlanet(unittest.TestCase):

    def setUp(self):
        self.planet = Neptune()
        date = '2017-08-31'
        self.H_path = Path(date, self.planet.name + '_H').all_files_in_folder[2]
        """
        
        self.K_path = Path(date, planet.name + '_Ks').all_files_in_folder[2]
        self.H_coordgrid = coordgrid.CoordGrid(self.H_path)
        self.K_coordgrid = coordgrid.CoordGrid(self.K_path)
        """

    def test_get_date_and_time(self):
        H_date, H_time = DerotatePlanet.get_date_and_time(self.H_path)
        self.assertEqual(H_date, '2017-09-01')
        self.assertEqual(H_time, '10:49')

    def test_time_between_images(self):

        # Test same hour
        H_date = K_date = '2017-08-31'
        H_time, K_time = '10:40', '10:10'
        time_difference = DerotatePlanet.find_time_between_images(H_date, H_time, K_date, K_time)
        self.assertEqual(time_difference, 30)

        H_date = K_date = '2017-08-31'
        H_time, K_time = '10:10', '10:40'
        time_difference = DerotatePlanet.find_time_between_images(H_date, H_time, K_date, K_time)
        self.assertEqual(time_difference, 30)

        # Test different hours
        H_date = K_date = '2017-08-31'
        H_time, K_time = '10:45', '09:50'
        time_difference = DerotatePlanet.find_time_between_images(H_date, H_time, K_date, K_time)
        self.assertEqual(time_difference, 55)

        H_date = K_date = '2017-08-31'
        H_time, K_time = '11:45', '10:45'
        time_difference = DerotatePlanet.find_time_between_images(H_date, H_time, K_date, K_time)
        self.assertEqual(time_difference, 60)

        #Test different days
        H_date, K_date = '2017-08-30', '2017-08-31'
        H_time, K_time = '12:45', '01:50'
        time_difference = DerotatePlanet.find_time_between_images(H_date, H_time, K_date, K_time)
        self.assertEqual(time_difference, 65)

        H_date, K_date = '2017-08-30', '2017-08-31'
        H_time, K_time = '12:45', '02:50'
        time_difference = DerotatePlanet.find_time_between_images(H_date, H_time, K_date, K_time)
        self.assertEqual(time_difference, 125)

if __name__ == '__main__':
    unittest.main()