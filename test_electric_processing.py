import unittest
import pytest
import electric_processing


class ElectricTastCase(unittest.TestCase):
    """Tests for electric_processing.py """

    def test_get_user_input(self):
        """Check if user input is not zero"""
        h, d = electric_processing.get_user_input()
        self.assertTrue(h)
        self.assertTrue(d)


if __name__ == '__main__':
    unittest.main()
