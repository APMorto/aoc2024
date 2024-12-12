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

    def __getitem__(self, item):
        return self.grid[item]
        #return lambda next_item: self.grid[item][next_item]

    def row_major_indexes(self):
        return ((r, c) for r in range(self.h) for c in range(self.w))

    def row_major_points(self):
        return (Point2D(r, c) for r in range(self.h) for c in range(self.w))

    def __len__(self):
        return self.h * self.w
        #return len(self.grid)

