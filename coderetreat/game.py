#!/usr/bin/env python
import random


DEAD = 0
ALIVE = 1

MAX_LOCATION_VALUE = 30


class DuplicatedLocationCells(Exception):
    pass


class Location(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return '{}, {}'.format(self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


class Cell(object):

    def __init__(self, status=ALIVE, x=None, y=None):
        self.status = status
        if not x and not y:
            self.location = Location(
                random.randint(0, MAX_LOCATION_VALUE),
                random.randint(0, MAX_LOCATION_VALUE))
        elif not x or not y:
            raise ValueError(
                'Parameters x and y should appear two or not of both')
        else:
            self.location = Location(x, y)

    def __str__(self):
        if self.status:
            status = 'ALIVE'
        else:
            status = 'DEAD'

        return 'Cell {}: ({})'.format(
            status, self.location
        )

    def __eq__(self, other):
        return self.location == other.location and self.status == other.status

    def is_alive(self):
        return self.status == ALIVE


class Universe(object):

    def __init__(self, cells_alive=None):
        self.cells = dict()
        if cells_alive:
            for i in range(cells_alive):
                cell = Cell(status=ALIVE)
                self.add_cell(cell)

    def __str__(self):
        return str([
            '{}'.format(cell) for cell in self.cells.values()
        ])

    def get_alive_cells(self):
        return [
            cell for cell in self.cells.values() if cell.is_alive()
        ]

    def add_cell(self, cell):
        if self.cells.get(cell.location):
            raise DuplicatedLocationCells('Duplicated cell: {}'.format(cell))
        self.cells[cell.location] = cell

    def add_cells(self, cells):
        for cell in cells:
            self.add_cell(cell)

    def get_neighbours(self, cell):
        neighbours = []
        for location in Universe.neighbours_locations(cell):
            neighbour = self.cells.get(location)
            if neighbour:
                neighbours.append(neighbour)
        return neighbours

    def get_alive_neighbours(self, cell):
        return [cell for cell in self.get_neighbours(cell)
                if cell.is_alive()]

    @staticmethod
    def __validate_neighbour_location(i, j, location):
        result = True
        if location.x == i and location.y == j:
            result = False
        elif i < 0 or j < 0:
            result = False
        elif i > MAX_LOCATION_VALUE or j > MAX_LOCATION_VALUE:
            result = False
        return result

    @staticmethod
    def neighbours_locations(cell):
        locations = []
        for i in range(cell.location.x - 1, cell.location.x + 2):
            for j in range(cell.location.y-1, cell.location.y + 2):
                if Universe.__validate_neighbour_location(i, j, cell.location):
                    locations.append(Location(x=i, y=j))
        return locations

    def rule_1(self):
        """
        An alive cell in contact with less than two cells will die

        :return:
        """
        for cell in self.get_alive_cells():
            if len(self.get_neighbours()) >= 2:
                cell.status = DEAD

    def rule_2(self):
        """
        An alive cell in contact with two or three alive cells will live
        """
        for cell in self.get_alive_cells():
            if len(self.get_alive_neighbours(cell)) in (2, 3):
                cell.status = ALIVE

    def rule_3(self):
        """
        An alive cell in contact with more than three cells will die
        """
        for cell in self.get_alive_cells():
            if len(self.get_alive_neighbours(cell)) > 3:
                cell.status = DEAD

    def rule_4(self):
        """
        If a dead cell come in contact with three or more alive cells, will come
        alive again
        :return:
        """
        for cell in self.get_alive_neighbours()

