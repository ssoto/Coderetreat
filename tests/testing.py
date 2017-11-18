import unittest

from coderetreat.game import Universe, Cell, Location, DEAD, ALIVE


class TestUniverse(unittest.TestCase):

    def setUp(self):
        super(TestUniverse, self)
        self.initial_alive_cells = 5
        self.universe = Universe(cells_alive=self.initial_alive_cells)

    def test_check_universe_alive_cells(self):
        universe = Universe(cells_alive=3)
        assert len(universe.get_alive_cells()) == 3

    def test_all_cells_alive_right(self):
        for cell in self.universe.get_alive_cells():
            assert cell.is_alive()


class TestLocation(unittest.TestCase):

    def test_cells_location_x_and_y(self):
        location = Location(x=1, y=7)
        assert location.x == 1
        assert location.y == 7


class TestCell(unittest.TestCase):

    def test_if_cell_is_alive(self):
        cell = Cell(status=ALIVE)
        assert cell.is_alive()


if __name__ == '__main__':
    unittest.main()
