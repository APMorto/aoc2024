from collections import defaultdict
from itertools import chain
from typing import List

import numpy as np

from util.datastructures import DisJointSets
from parser.parser import read_grid
from util.directions import Direction2D
from util.timer import get_results
from util.grid2d import Grid2DDense
from util.point2d import Point2D


def part1_grid(grid: List[str]):
    h = len(grid)
    w = len(grid[0])
    grid = Grid2DDense(grid)

    dsu = DisJointSets(h * w)

    # Set up connected components.
    for p in grid.row_major_points():
        for adj in p.get_adjacent_ortho():
            if grid.get(p) == grid.get(adj):
                dsu.join(p.row_major(w), adj.row_major(w))

    # Perimeters of roots
    perimiters = defaultdict(int)

    # Count perimeters.
    for p in grid.row_major_points():
        for adj in p.get_adjacent_ortho():
            if grid.get(p) != grid.get(adj):
                perimiters[dsu.find(p.row_major(w))] += 1

    # Sum area * perimeter
    out = 0
    for root in dsu.componentRoots():
        out += perimiters[dsu.find(root)] * dsu.componentSize(root)
    return out

def part2_grid(list_of_strings: List[str]):
    grid = Grid2DDense(list_of_strings)
    h, w = grid.shape
    dsu = DisJointSets(h * w)

    # Set up connected components.
    for p in grid.row_major_points():
        for adj in p.get_adjacent_ortho():
            if grid.get(p) == grid.get(adj):
                dsu.join(p.row_major(w), adj.row_major(w))

    # Perimeters of roots
    perimiters = defaultdict(int)

    # Get adjacent
    for p in grid.row_major_points():
        here = grid.get(p)
        for direction in Point2D.DIRECTIONS:
            offset_point = p + direction
            if here != grid.get(offset_point):     # Is boundary in this direction
                right = direction.turn_right()
                right_val = grid.get(p + right)
                if not (here == right_val and right_val != grid.get(offset_point + right)):    # Boundary does not propagate right
                    perimiters[dsu.find(p.row_major(w))] += 1

    # Sum area * perimeter
    out = 0
    for root in dsu.componentRoots():
        out += perimiters[dsu.find(root)] * dsu.componentSize(root)
    return out


def both_parts_numpy(list_of_strings: List[str]):
    grid = Grid2DDense(list_of_strings)
    h, w = grid.shape
    dsu = DisJointSets(h * w)

    # Set up connected components.
    for r in range(h):
        for c in range(w):
            cur = list_of_strings[r][c]
            cur_i = r * w + c
            for rr, cc in ((r-1, c), (r+1, c), (r, c-1), (r, c+1)):
                if 0 <= rr < h and 0 <= cc < w and cur == list_of_strings[rr][cc]:
                    dsu.join(cur_i, rr*w+cc)

    # Get an array where arr[r, c] = component size of r, c
    root_lookup_array = np.array([dsu.find(i) for i in range(len(dsu._parents))])
    component_sizes = np.bincount(root_lookup_array)   #component_sizes[root_lookup_map] += 1  but 'pythonic'
    component_sizes_at_each_tile = component_sizes[root_lookup_array].reshape(h, w)

    # Use numpy to vectorize corner and edge finding.
    array = np.array([list(s) for s in list_of_strings])
    acc1 = np.zeros((h, w), dtype=np.int_)
    acc2 = np.zeros((h, w), dtype=np.int_)
    for rot in range(4):
        # Where there is fence.
        diff_down =  np.ones((h, w), dtype=bool)
        diff_right = np.ones((h, w), dtype=bool)
        diff_down[:h-1, :]  = array[1:, :] != array[:h-1, :]
        diff_right[:, :h-1] = array[:, 1:] != array[:, :h-1]

        # Check 1 direction for part 1.
        acc1 += diff_down   # This add is proper.

        # Find the 2 different kinds of corners.
        short_dr = (diff_down & diff_right)
        long_dr = ~(diff_down | diff_right)
        long_dr[:-1, :] &= diff_right[1:, :]

        acc2 += short_dr
        acc2 += long_dr

        # Rotate. It's done with views so it's pretty fast.
        acc1 = np.rot90(acc1)
        acc2 = np.rot90(acc2)
        if rot != 3:
            array = np.rot90(array)

    # And of course output = dot product of component size * len(fence)
    # The fence portions are split up, but its fine since area_size * total_fence = area_size * (fence_area_1 + ... + fence_area_n)
    out1 = int(np.sum(acc1 * component_sizes_at_each_tile))
    out2 = int(np.sum(acc2 * component_sizes_at_each_tile))

    return out1, out2

# Old, uglier. (And 2x as fast)
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

# Old, ugly.
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


if __name__ == '__main__':
    get_results("P1 Example Small", part1, read_grid, "examplesmall.txt")
    get_results("P1 Example", part1, read_grid, "example.txt")
    get_results("P1", part1, read_grid, "input.txt")
    get_results("P1 Grid", part1_grid, read_grid, "input.txt")

    get_results("P2 Example Small", part2, read_grid, "examplesmall.txt")   # Should be 80
    get_results("P2 Example", part2, read_grid, "example.txt")
    get_results("P2 Example ABBA", part2, read_grid, "exampleABBA.txt")
    get_results("P2", part2, read_grid, "input.txt")
    get_results("P2 Grid", part2_grid, read_grid, "input.txt")

    get_results("Both parts Array", both_parts_numpy, read_grid, "input.txt", expected=(1396562, 844132))

