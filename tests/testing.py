import unittest

from coderetreat.game import Universe, ALIVE


class TestStringMethods(unittest.TestCase):

    def test_universe_dimensions(self):
        universe = Universe(dimension=23)
        assert universe.dimension == 23

    def test_universe_has_right_height(self):
        universe = Universe(dimension=23)

        assert universe.get_height() == universe.dimension

    def test_universe_has_right_height(self):
        universe = Universe(dimension=23)

        assert universe.get_height() == universe.dimension

    def test_universe_cells_initialization(self):
        universe = Universe(4)

        universe.set_status(2, 1, ALIVE)
        assert universe.get_status(2, 1) == ALIVE


if __name__ == '__main__':
    unittest.main()
