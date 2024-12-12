from collections import defaultdict
from typing import List

from util.datastructures import DisJointSets
from parser.parser import read_grid
from util.directions import Direction2D
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
    # But now, long sides count as 1
    for r in range(h):
        for c in range(w):
            for d in Direction2D:
                right = d.turn_right()
                ro, co = d.offset()
                above = grid[r+ro][c+co] if 0 <= r+ro < h and 0 <= c+co < w else None

                # If right is same, and above and right above are both distinct, dont count this.
                # In effect, only consider the rightmost edge.
                right_r, right_c = right.offset()
                if 0 <= r+right_r < h and 0 <= c+right_c < w:   # Right exists.
                    if grid[r + right_r][c + right_c] == grid[r][c]:    # and is the same
                        right_above = grid[r + right_r + ro][c + right_c + co] if 0 <= r + right_r + ro < h and 0 <= c + right_c + co < w else None
                        if above != grid[r][c] and right_above != grid[r][c]:
                            continue

                # We have now eliminated any 'duplicate' edge, and can procede as before
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

# 922223 too high

if __name__ == '__main__':
    get_results("P1 Example Small", part1, read_grid, "examplesmall.txt")
    get_results("P1 Example", part1, read_grid, "example.txt")
    get_results("P1", part1, read_grid, "input.txt")

    get_results("P2 Example Small", part2, read_grid, "examplesmall.txt")   # Should be 80
    get_results("P2 Example", part2, read_grid, "example.txt")
    get_results("P2 Example ABBA", part2, read_grid, "exampleABBA.txt")
    get_results("P2", part2, read_grid, "input.txt")