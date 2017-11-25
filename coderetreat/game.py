#!/usr/bin/env python
import copy
import os
import random
import time


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

    def __init__(self, cells_alive=None, cells=None):
        """

        :param cells_alive: integer with number of alive cells
        :param cells: list of cells that will be added to universe
        """
        if cells_alive and cells:
            raise Exception('Only one parameter is allowed')

        self.cells = dict()

        if cells_alive or cells:
            in_cells = []
            if cells_alive:
                for i in range(cells_alive):
                    in_cells.append(Cell(status=ALIVE))

            if cells:
                in_cells = cells

            for cell in in_cells:
                self.add_cell(cell)

    def __str__(self):
        return str([
            '{}'.format(cell) for cell in self.cells.values()
        ])

    def update(self, universe):
        self.cells = copy.deepcopy(universe.cells)

    def get_alive_cells(self):
        return [
            cell for cell in self.cells.values() if cell.is_alive()
        ]

    def get_cells(self):
        return list(self.cells.values())

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


class RuleApplier(object):

    def __init__(self):
        self.rules = [RuleOne(), RuleTwo(), RuleThree(), RuleFour(), ]

    def apply(self, universe):

        next_universe = Universe()

        for rule in self.rules:
            next_universe.update(rule.apply(universe))

        return next_universe


class Rule(object):

    def _run(self, universe):
        raise NotImplemented()

    def apply(self, universe):
        result = self._run(universe)
        if not isinstance(result, Universe):
            raise Exception(
                'Rule run method must return Universe, get a {}'.format(
                    type(result)))
        return result


class RuleOne(Rule):

    def _run(self, universe):
        """"
        An alive cell in contact with less than two cells will die
        """
        new_universe = Universe()
        for cell in universe.get_cells():
            changed_cell = copy.deepcopy(cell)
            if len(universe.get_neighbours(cell)) >= 2:
                changed_cell.status = DEAD
            new_universe.add_cell(changed_cell)
        return new_universe


class RuleTwo(Rule):

    def _run(self, universe):
        """
        An alive cell in contact with two or three alive cells will live
        """
        new_universe = Universe()
        for cell in universe.get_cells():
            changed_cell = copy.deepcopy(cell)
            if len(universe.get_alive_neighbours(cell)) not in (2, 3):
                changed_cell.status = DEAD
            new_universe.add_cell(changed_cell)
        return new_universe


class RuleThree(Rule):

    def _run(self, universe):
        """
        An alive cell in contact with more than three cells will die
        """
        new_universe = Universe()
        for cell in universe.get_alive_cells():
            changed_cell = copy.deepcopy(cell)
            if len(universe.get_alive_neighbours(cell)) > 3:
                changed_cell.status = DEAD
            new_universe.add_cell(changed_cell)
        return new_universe


class RuleFour(Rule):

    def _run(self, universe):
        """
        If a dead cell come in contact with three or more alive cells, will come
        alive again
        :return:
        """
        for cell in universe.get_cells():
            for n in universe.get_alive_neighbours(cell):
            # TODO
                pass
        return universe


class GamePrinter(object):

    alive_symbol = 'o'
    dead_symbol = '_'

    @staticmethod
    def build_grid(x, y, alive):
        text_to_print = str('\n')
        for i in range(x):
            text_to_print += '\t|'
            for j in range(y):
                if [i, j] in alive:
                    text_to_print += '{}|'.format(GamePrinter.alive_symbol)
                else:
                    text_to_print += '{}|'.format(GamePrinter.dead_symbol)
            text_to_print += '\n'
        return text_to_print


    @staticmethod
    def clear():
        os.system('clear')

    @staticmethod
    def next_phase(height, width, phase, specials, auto_mode=False):
        GamePrinter.clear()
        auto_str = ''
        if auto_mode:
            auto_str = 'in auto mode'

        header = '\nPrinting {} X {} grid{}. Step {} with specials: {}'
        header = header.format(height, width, auto_str, phase, specials)

        grid = GamePrinter.build_grid(height, width, alive=specials)

        to_print = '{}\n{}'.format(header, grid)
        print(to_print)
        if auto_mode:
            time.sleep(1)
        else:
            input('Intro to new step')


if __name__ == '__main__':

    # X = int(input('Insert number of rows: '))
    # Y = int(input('Insert number of columns: '))
    # auto_str = input('Do you want to play in auto mode?. Yes (y) or no(n): ')
    auto_str = 'y'

    auto_mode = False
    if auto_str.strip().lower() == 'y':
        auto_mode = True

    game = GamePrinter()
    cells = [
        Cell(status=ALIVE, x=3, y=3),
        Cell(status=ALIVE, x=1, y=3),
        Cell(status=ALIVE, x=2, y=3),
        Cell(status=ALIVE, x=10, y=3),
        Cell(status=ALIVE, x=10, y=4),
        Cell(status=ALIVE, x=10, y=5),
    ]
    universe = Universe(cells=cells)
    applier = RuleApplier()
    try:
        for phase in range(30):
            alives_coords = [
                [cell.location.x, cell.location.y] for cell in
                universe.get_alive_cells()
            ]
            game.next_phase(width=MAX_LOCATION_VALUE, height=MAX_LOCATION_VALUE,
                            phase=phase, auto_mode=auto_mode,
                            specials=alives_coords)
            universe = applier.apply(universe)
    except KeyboardInterrupt:
        print('Godbye!')
