from typing import List


def seek_character(grid: List[str], c: str):
    for r, l in enumerate(grid):
        for col, char in enumerate(l):
            if char == c:
                return r, col