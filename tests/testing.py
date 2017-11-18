import unittest

from coderetreat.game import Universe, Cell, DEAD, ALIVE


class TestUniverse(unittest.TestCase):

    def test_check_universe_creation(self):
        universe = Universe(cells_alive=3)
        assert len(universe.get_alive_cells()) == 3

    def test_if_cell_is_alive(self):
        universe = Universe(cells_alive=3)
        for cell in universe.get_alive_cells():
            assert cell.is_alive()

    def test_cells_location_two_dimensions(self):
        universe = Universe(cells_alive=2)
        for cell in  universe.get_alive_cells():
            location = cell.get_location()
            assert isinstance(location.get_x(), int)
            assert isinstance(location.get_y(), int)

class TestCell(unittest.TestCase):

    def test_if_cell_is_alive(self):
        cell = Cell(status=ALIVE)
        assert cell.is_alive() == ALIVE

if __name__ == '__main__':
    unittest.main()
