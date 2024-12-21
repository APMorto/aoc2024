from typing import List

from util.point2d import Point2D


def seek_character(grid: List[str], c: str):
    """
    Note that this returns row column, or Y, X!!
    :param grid:
    :param c:
    :return:
    """
    for r, l in enumerate(grid):
        for col, char in enumerate(l):
            if char == c:
                return r, col

def seek_character_point(grid: List[str], c: str):
    return Point2D(*reversed(seek_character(grid, c)))

def rotate_matrix(matrix):
    return tuple(zip(*(r for r in matrix[::-1])))

def pad_grid(grid: List[list], padding):
    h, w = len(grid), len(grid[0])
    for l in grid:
        l.insert(0, padding)
        l.append(padding)
    grid.insert(0, [padding] * (w+2))
    grid.append([padding] * (w+2))