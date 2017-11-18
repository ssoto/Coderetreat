#!/usr/bin/env python
import random


DEAD = 0
ALIVE = 1


class Location(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Cell(object):

    def __init__(self, status, debug=False, x=None, y=None):
        self.status = status
        if not debug:
            self.location = Location(
                random.randint(1, 10), random.randint(1, 10))
        else:
            self.location = Location(x, y)

    def is_alive(self):
        return self.status == ALIVE

    def get_location(self):
        return self.location


class Universe(object):

    def __init__(self, cells_alive):
        self.number_cells_alive = cells_alive

    def get_alive_cells(self):
        cells_alive = []
        for i in range(self.number_cells_alive):
            cells_alive.append(Cell(ALIVE))
        return cells_alive
