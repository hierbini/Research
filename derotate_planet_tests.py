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

    def test_get_time_in_order(self):

        # Test same hour
        H_date = K_date = '2017-08-31'
        H_time, K_time = '10:40', '10:10'
        order_list = [DerotatePlanet.get_time_in_order(H_date, H_time, K_date, K_time)]
        test_list = [K_date, K_time, H_date, H_time]
        self.assertEqual(order_list, test_list)

        H_date = K_date = '2017-08-31'
        H_time, K_time = '10:10', '10:40'
        order_list = [DerotatePlanet.get_time_in_order(H_date, H_time, K_date, K_time)]
        test_list = [H_date, H_time, K_date, K_time]
        self.assertEqual(order_list, test_list)

        # Test different hours
        H_date = K_date = '2017-08-31'
        H_time, K_time = '10:45', '09:50'
        order_list = [DerotatePlanet.get_time_in_order(H_date, H_time, K_date, K_time)]
        test_list = [K_date, K_time, H_date, H_time]
        self.assertEqual(order_list, test_list)

        H_date = K_date = '2017-08-31'
        H_time, K_time = '10:45', '11:45'
        order_list = [DerotatePlanet.get_time_in_order(H_date, H_time, K_date, K_time)]
        test_list = [H_date, H_time, K_date, K_time]
        self.assertEqual(order_list, test_list)

        # Test different days
        H_date, K_date = '2017-08-30', '2017-08-31'
        H_time, K_time = '11:45', '01:50'
        order_list = [DerotatePlanet.get_time_in_order(H_date, H_time, K_date, K_time)]
        test_list = [H_date, H_time, K_date, K_time]
        self.assertEqual(order_list, test_list)

        H_date, K_date = '2017-08-31', '2017-08-30'
        H_time, K_time = '12:45', '11:50'
        order_list = [DerotatePlanet.get_time_in_order(H_date, H_time, K_date, K_time)]
        test_list = [K_date, K_time, H_date, H_time]
        self.assertEqual(order_list, test_list)

        # Test different months
        H_date, K_date = '2017-09-01', '2017-08-31'
        H_time, K_time = '02:45', '11:50'
        order_list = [DerotatePlanet.get_time_in_order(H_date, H_time, K_date, K_time)]
        test_list = [K_date, K_time, H_date, H_time]
        self.assertEqual(order_list, test_list)

        H_date, K_date = '2017-08-31', '2017-09-01'
        H_time, K_time = '11:50', '02:45'
        order_list = [DerotatePlanet.get_time_in_order(H_date, H_time, K_date, K_time)]
        test_list = [H_date, H_time, K_date, K_time]
        self.assertEqual(order_list, test_list)

    def test_get_time_between_images(self):

        # Test same hours
        begin_date = end_date = '2017-08-31'
        end_time, begin_time = '10:40', '10:10'
        time_difference = DerotatePlanet.find_time_between_images(begin_date, begin_time, end_date, end_time)
        self.assertEqual(time_difference, 30)

        # Test different hours
        begin_date = end_date = '2017-08-31'
        end_time, begin_time = '10:45', '09:50'
        time_difference = DerotatePlanet.find_time_between_images(begin_date, begin_time, end_date, end_time)
        self.assertEqual(time_difference, 55)

        # Test different days
        begin_date, end_date = '2017-08-30', '2017-08-31'
        begin_time, end_time = '11:45', '01:50'
        time_difference = DerotatePlanet.find_time_between_images(begin_date, begin_time, end_date, end_time)
        self.assertEqual(time_difference, 125)

        # Test different months
        begin_date, end_date = '2017-08-31', '2017-09-01'
        begin_time, end_time = '11:50', '02:45'
        time_difference = DerotatePlanet.find_time_between_images(begin_date, begin_time, end_date, end_time)
        self.assertEqual(time_difference, 175)

if __name__ == '__main__':
    unittest.main()