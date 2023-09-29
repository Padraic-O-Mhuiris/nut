import unittest
from nut import nut_base


class TestCalculations(unittest.TestCase):
    def test_sum(self):
        self.assertEqual(9, 10, "The sum is wrong.")


if __name__ == "__main__":
    unittest.main()
