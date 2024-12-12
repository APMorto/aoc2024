from collections import defaultdict
from typing import List

from util.datastructures import DisJointSets
from parser.parser import read_grid
from util.timer import get_results


def part1(grid: List[str]):
    h = len(grid)
    w = len(grid[0])

    dsu = DisJointSets(h * w)

    # Set up connected components for areas
    for r in range(h):
        for c in range(w):
            for ro, co in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                if 0 <= r+ro < h and 0 <= c+co < w:
                    rr, cc = r + ro, c + co
                    if grid[rr][cc] == grid[r][c]:
                        dsu.join(r*w+c, rr*w+cc)

    # Perimeters of roots
    perimiters = defaultdict(int)

    # Count perimeters.
    for r in range(h):
        for c in range(w):
            for ro, co in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                #if not (0 <= r+ro < h and 0 <= c+co < w and grid[r+ro][c+co] != grid[r][c]):
                #    perimiters[dsu.find(r * w + c)] += 1
                if 0 <= r+ro < h and 0 <= c+co < w:
                    rr, cc = r + ro, c + co
                    if grid[rr][cc] != grid[r][c]:
                        perimiters[dsu.find(r * w + c)] += 1
                else:
                    perimiters[dsu.find(r * w + c)] += 1


    # Sum area * perimeter
    out = 0
    for root in dsu.componentRoots():
        #print(root, perimiters[dsu.find(root)], dsu.componentSize(root))
        out += perimiters[dsu.find(root)] * dsu.componentSize(root)
    return out

def part2(grid: List[str]):
    pass


if __name__ == '__main__':
    get_results("P1 Example Small", part1, read_grid, "examplesmall.txt")
    get_results("P1 Example", part1, read_grid, "example.txt")
    get_results("P1", part1, read_grid, "input.txt")

    get_results("P2 Example", part2, read_grid, "examplesmall.txt")
    get_results("P2", part2, read_grid, "input.txt")