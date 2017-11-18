import unittest

from coderetreat.game import Universe


class TestUniverse(unittest.TestCase):

    def test_universe_alives_cells(self):
        universe = Universe(width=4, height=4, alive_cells=2)
        assert len(universe.get_alive_cells()) == 2

    def test_cells_with_alive_neighbours(self):
        univers =  Universe(width=4, height=4, alive_cells=8)
        assert len(univers.get_cells_with_alive_neighbours()) > 0
if __name__ == '__main__':
    unittest.main()
