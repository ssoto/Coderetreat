import unittest

from coderetreat.game import (Universe, Cell, Location, DEAD, ALIVE,
                              DuplicatedLocationCells)


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

    def test_cell_creation_with_location(self):
        universe = Universe()
        cell_test_1 = Cell(status=ALIVE, x=3, y=3)
        universe.add_cell(cell_test_1)
        universe_cells = universe.get_alive_cells()
        assert len(universe_cells) == 1
        assert universe_cells[0] == cell_test_1

    def test_universe_updating(self):
        original_universe = Universe()
        cell_test_1 = Cell(status=ALIVE, x=3, y=3)
        original_universe.add_cell(cell_test_1)

        universe = Universe()
        universe.update(original_universe)
        universe_cells = universe.get_alive_cells()

        assert len(universe_cells) == 1
        assert universe_cells[0] == cell_test_1

    def test_cell_add_with_listOfCells(self):
        universe = Universe()
        cells = [
            Cell(status=ALIVE, x=3, y=3),
            Cell(status=ALIVE, x=2, y=3), ]
        universe.add_cells(cells)
        assert (len(universe.get_alive_cells()) == 2)

    def test_universe_build_from_cells(self):
        cells = [
            Cell(status=ALIVE, x=3, y=3),
            Cell(status=DEAD, x=1, y=3),
            Cell(status=ALIVE, x=2, y=3), ]
        universe = Universe(cells=cells)
        assert cells[0] in universe.get_alive_cells()
        assert cells[1] not in universe.get_alive_cells()
        assert cells[2] in universe.get_alive_cells()

    def test_cell_add_with_listOfCells_duplicatedLocations(self):
        universe = Universe()
        cells = [
            Cell(status=ALIVE, x=2, y=2),
            Cell(status=ALIVE, x=2, y=2), ]
        with self.assertRaises(DuplicatedLocationCells):
            universe.add_cells(cells)

    def test_cell_neighbour(self):
        universe = Universe()
        cell_1 = Cell(status=ALIVE, x=3, y=3)
        cell_2 = Cell(status=ALIVE, x=2, y=3)
        universe.add_cells([cell_1, cell_2])
        neighbours = universe.get_neighbours(cell_1)
        assert len(neighbours) == 1
        assert neighbours[0] == cell_2

    def test_universe_neighbours_index_calculation_len(self):
        neighbour_locations = Universe.neighbours_locations(Cell(x=3, y=3))
        assert len(neighbour_locations) == 8
        assert Location(x=2, y=2) in neighbour_locations
        assert Location(x=2, y=3) in neighbour_locations
        assert Location(x=2, y=4) in neighbour_locations
        assert Location(x=3, y=2) in neighbour_locations
        assert Location(x=3, y=4) in neighbour_locations
        assert Location(x=4, y=2) in neighbour_locations
        assert Location(x=4, y=3) in neighbour_locations
        assert Location(x=4, y=4) in neighbour_locations

    def test_universe_get_alive_neigbours(self):
        """
                  2    3    4
              2        A    D
              3        A
              4   A
        """
        universe = Universe()
        cell_1 = Cell(status=ALIVE, x=2, y=3)
        cell_2 = Cell(status=DEAD, x=2, y=4)
        cell_3 = Cell(status=ALIVE, x=3, y=3)
        cell_4 = Cell(status=ALIVE, x=4, y=2)
        universe.add_cells([cell_1, cell_2, cell_3, cell_4])
        alive_neighbours = universe.get_alive_neighbours(cell_3)
        assert len(alive_neighbours) == 2
        assert cell_1 in alive_neighbours
        assert cell_2 not in alive_neighbours
        assert cell_4 in alive_neighbours


class TestLocation(unittest.TestCase):

    def test_cells_location_x_and_y(self):
        location = Location(x=1, y=7)
        assert location.x == 1
        assert location.y == 7


class TestCell(unittest.TestCase):

    def test_if_cell_is_alive(self):
        cell = Cell(status=ALIVE)
        assert cell.is_alive()

    def test_if_cell_is_dead(self):
        cell = Cell(status=DEAD)
        assert not cell.is_alive()

    def test_cell_location_withXandY(self):
        cell = Cell(status=ALIVE, x=8, y=30)
        assert cell.location.x == 8
        assert cell.location.y == 30

    def test_cell_location_raise_exception_yIsNone(self):
        with self.assertRaises(ValueError):
            Cell(status=DEAD, x=30)

    def test_cell_location_raise_exception_xIsNone(self):
        with self.assertRaises(ValueError):
            Cell(status=DEAD, y=92)

    def test_cell_location_withRandomValues(self):
        cell = Cell(status=DEAD)
        assert isinstance(cell.location.x, int)
        assert isinstance(cell.location.y, int)


if __name__ == '__main__':
    unittest.main()
