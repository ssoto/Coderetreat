#!/usr/bin/env python

DEAD = 0
ALIVE = 1


class TwoDimensionsUniverse(object):

    def __init__(self, x, y):
        self.width = x
        self.height = y
        self.grid = []

    def cell_at(self, x, y):
        return DEAD

    def initialize(self, x, y, status):
