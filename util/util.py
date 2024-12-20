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
    return list(zip(*(r for r in matrix[::-1])))