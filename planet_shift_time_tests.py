import unittest
from planet_shift_time_old import *
from planet_info import *
from coordgrid import *
from tool_box import *
import pyfits

class TestDerotatePlanet(unittest.TestCase):

    def setUp(self):
        self.planet = Neptune()
        date = '2017-08-31'
        self.H_path = Path(date, self.planet.name + '_H').all_files_in_folder[2]

    def test_get_date_and_time(self):
        H_date, H_time = PlanetShiftTime.get_date_and_time(self.H_path)
        self.assertEqual(H_date, '2017-09-01')
        self.assertEqual(H_time, '10:49:02')

    def test_get_time_in_order(self):



        # Test same hour
        H_date = K_date = '2017-08-31'
        H_time, K_time = '10:40:02', '10:10:03'
        order_list = list(PlanetShiftTime.order_AB_date_time(H_date, H_time, K_date, K_time))
        test_list = [K_date, K_time, H_date, H_time]
        self.assertListEqual(order_list, test_list)

        H_date = K_date = '2017-08-31'
        H_time, K_time = '10:10:03', '10:40:10'
        order_list = list(PlanetShiftTime.order_AB_date_time(H_date, H_time, K_date, K_time))
        test_list = [H_date, H_time, K_date, K_time]
        self.assertListEqual(order_list, test_list)

        # Test different hours
        H_date = K_date = '2017-08-31'
        H_time, K_time = '10:45:03', '09:50:04'
        order_list = list(PlanetShiftTime.order_AB_date_time(H_date, H_time, K_date, K_time))
        test_list = [K_date, K_time, H_date, H_time]
        self.assertListEqual(order_list, test_list)

        H_date = K_date = '2017-08-31'
        H_time, K_time = '10:45:23', '11:45:25'
        order_list = list(PlanetShiftTime.order_AB_date_time(H_date, H_time, K_date, K_time))
        test_list = [H_date, H_time, K_date, K_time]
        self.assertListEqual(order_list, test_list)

        # Test different days
        H_date, K_date = '2017-08-30', '2017-08-31'
        H_time, K_time = '11:45:45', '01:50:03'
        order_list = list(PlanetShiftTime.order_AB_date_time(H_date, H_time, K_date, K_time))
        test_list = [H_date, H_time, K_date, K_time]
        self.assertListEqual(order_list, test_list)

        H_date, K_date = '2017-08-31', '2017-08-30'
        H_time, K_time = '12:45:03', '11:50:23'
        order_list = list(PlanetShiftTime.order_AB_date_time(H_date, H_time, K_date, K_time))
        test_list = [K_date, K_time, H_date, H_time]
        self.assertEqual(order_list, test_list)

        # Test different months
        H_date, K_date = '2017-09-01', '2017-08-31'
        H_time, K_time = '02:45:34', '11:50:54'
        order_list = list(PlanetShiftTime.order_AB_date_time(H_date, H_time, K_date, K_time))
        test_list = [K_date, K_time, H_date, H_time]
        self.assertListEqual(order_list, test_list)

        H_date, K_date = '2017-08-31', '2017-09-01'
        H_time, K_time = '11:50:34', '02:45:34'
        order_list = list(PlanetShiftTime.order_AB_date_time(H_date, H_time, K_date, K_time))
        test_list = [H_date, H_time, K_date, K_time]
        self.assertListEqual(order_list, test_list)

    def test_get_time_between_images(self):

        # Test same hours
        begin_date = end_date = '2017-08-31'
        end_time, begin_time = '10:40:04', '10:10:03'
        time_difference = PlanetShiftTime.get_time_between_images(begin_date, begin_time, end_date, end_time)
        self.assertEqual(time_difference, 1801)

        # Test different hours
        begin_date = end_date = '2017-08-31'
        end_time, begin_time = '10:45:04', '09:50:03'
        time_difference = PlanetShiftTime.get_time_between_images(begin_date, begin_time, end_date, end_time)
        self.assertEqual(time_difference, 3301)

        # Test different days
        begin_date, end_date = '2017-08-30', '2017-08-31'
        begin_time, end_time = '11:45:20', '01:50:10'
        time_difference = PlanetShiftTime.get_time_between_images(begin_date, begin_time, end_date, end_time)
        self.assertEqual(time_difference, 7490)
        # Test different months
        begin_date, end_date = '2017-08-31', '2017-09-01'
        begin_time, end_time = '11:50:04', '02:45:03'
        time_difference = PlanetShiftTime.get_time_between_images(begin_date, begin_time, end_date, end_time)
        self.assertEqual(time_difference, 10499)

if __name__ == '__main__':
    unittest.main()