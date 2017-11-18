#!/usr/bin/env python
import random

class Universe(object):

    def __init__(self, width, height, alive_cells):
        self.width = width
        self.height = height
        self.alive_cells = alive_cells
        self.grid = self.get_grid_default()
        self.setalivecells()

    def get_grid_default(self):
        grid = list()
        for i in range(self.width):
            grid.append([0]*self.height)
        return grid

    def setalivecells(self):
        for i in range(self.alive_cells):
            x = random.randint(0,self.width-1)
            y = random.randint(0,self.height-1)
            self.grid[x][y] = 1;

    def get_alive_cells(self):
        alive_cells = list()
        for i in range(self.width):
            for u in range(self.height):
                if self.grid[i][u] == 1:
                    alive_cells.append([i, u])

        return alive_cells;