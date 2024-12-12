from typing import List, Iterable

from util.point2d import Point2D


class Grid2DDense:
    def __init__(self, grid: List):
        self.grid = grid
        self.h = len(grid)
        self.w = len(grid[0])

    def get(self, point: Point2D):
        return self.grid[point.y][point.x] if 0 <= point.y < self.h and 0 <= point.x < self.w else None

    def __getitem__(self, item):
        return lambda next_item: self.grid[item][next_item]

    def row_major_indexes(self):
        return (r, c for c in range(self.w) for r in range(self.h))
