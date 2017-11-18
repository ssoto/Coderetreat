#!/usr/bin/env python

ALIVE = 1

class Universe(object):

    def __init__(self, dimension):
        self.dimension = dimension

        grid_list = list()
        grid_list.append(tuple(self.dimension * [[None] * self.dimension]))
        self.grid = tuple(grid_list)

    def get_height(self):
        return len(self.grid)

    def get_width(self):
        return self.dimension

    def set_status(self, x, y, state):
        if x < self.dimension and y < self.dimension:
            self.grid[x][y] = state

    def get_status(self, x, y):
        if x < self.dimension and y < self.dimension:
            return self.grid[x][y]
