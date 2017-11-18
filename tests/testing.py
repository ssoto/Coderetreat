import unittest
import random

from coderetreat.game import TwoDimensionsUniverse
from coderetreat.game import DEAD, ALIVE


class TestStringMethods(unittest.TestCase):

    def test_universe_dimensions(self):
        u = TwoDimensionsUniverse(2, 4)
        assert u.width == 2
        assert u.height == 4

    def test_new_universe_has_no_living_cells(self):
        u = TwoDimensionsUniverse(1, 1)
        assert u.cell_at(0, 0) == DEAD

    def test_universe_creation(self):
        u = TwoDimensionsUniverse(2, 2)
        u.initialize(x=0, y=1, status=ALIVE)
        assert u.cell_at(x=0, y=1) == ALIVE


if __name__ == '__main__':
    unittest.main()
