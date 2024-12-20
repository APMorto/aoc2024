from copy import copy
from typing import List, Iterable

from util.point2d import Point2D


class Grid2DDense:
    def __init__(self, grid: List):
        self.grid = grid
        self.h = len(grid)
        self.w = len(grid[0])
        self.shape = (self.h, self.w)

    def get(self, point: Point2D):
        return self.grid[point.y][point.x] if 0 <= point.y < self.h and 0 <= point.x < self.w else None

    def set(self, point: Point2D, value):
        self.grid[point.y][point.x] = value

    def swap(self, point1: Point2D, point2: Point2D):
        self.grid[point1.y][point1.x], self.grid[point2.y][point2.x] = self.grid[point2.y][point2.x], self.grid[point1.y][point1.x]

    def horizontal_shift(self, row: int, left: int, right: int, offset: int, fill):
        # Does not work.
        if offset == 0:
            return
        # Right is inclusive.
        left, right = min(left, right), max(left, right)
        lo = left + offset
        ro = right + offset
        line = self.grid[row]
        print(row, left, right, offset)
        print("line before offset", line)
        line[lo : ro+1] = line[left : right+1]
        if offset > 0:
            line[left : lo] = [fill] * offset
        else:
            line[ro+1 : right+1] = [fill] * (-offset)
        print("line post offset  ", line)

    def in_bounds(self, point: Point2D) -> bool:
        return 0 <= point.y < self.h and 0 <= point.x < self.w

    def __getitem__(self, item):
        return self.grid[item]
        #return lambda next_item: self.grid[item][next_item]

    def row_major_indexes(self):
        return ((r, c) for r in range(self.h) for c in range(self.w))

    def row_major_points(self):
        return (Point2D(r, c) for r in range(self.h) for c in range(self.w))

    def pos_iter(self):
        raise NotImplemented
        return (Point2D(c, r) for r in range(self.h) for c in range(self.w) )

    def __len__(self):
        return self.h * self.w
        #return len(self.grid)

    def display(self):
        for line in self.grid:
            print(line)

