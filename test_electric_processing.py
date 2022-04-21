import unittest
import pytest
import electric_processing


class ElectricTastCase(unittest.TestCase):
    """Tests for electric_processing.py """


    def test_get_user_input(self):
        """Check if returned values is not zero"""
        h, d = electric_processing.get_user_input()
        self.assertTrue(h)
        self.assertTrue(d)


    def test_calc_geometrical_params(self):
        """Check if returned values is not zero"""
        s, c_0 = electric_processing.calc_geometrical_params(1.1, 12.5)
        self.assertTrue(s)
        self.assertTrue(c_0)


    # def test_data_reading(self):
    #     """Check if there is file to read"""
    #     raw_data_frame = electric_processing.data_reading()


if __name__ == '__main__':
    unittest.main()
