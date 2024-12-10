from typing import List
import numpy as np

from parser.parser import read_grid
from util.timer import get_results


# A good hiking trail:
#   Starts at 0
#   ends at 9
#   increases by 1 at each (orthogonal) step

# A trailhead starts 1 or more hiking trails
# The trailheads score is the number of 9 height positions available
# Sum of scores of all trailheads

def num_9s_accessible(r, c, num_masks: List[np.ndarray]):
    h, w = num_masks[0].shape
    cur = np.zeros((h, w), dtype=bool)
    cur[r][c] = True


    for i in range(1, 10):
        new = np.zeros((h, w), dtype=bool)
        new[:-1]    |= cur[1:]
        new[1:]     |= cur[:-1]
        new[:, :-1] |= cur[:, 1:]
        new[:, 1:]  |= cur[:, :-1]
        new &= num_masks[i]
        cur = new
        if np.sum(cur) == 0:
            return 0
    return np.sum(cur)

def num_ways_to_get_9s(r, c, num_masks: List[np.ndarray]):
    h, w = num_masks[0].shape
    cur = np.zeros((h, w), dtype=np.long)
    cur[r][c] = 1

    for i in range(1, 10):
        new = np.zeros((h, w), dtype=np.long)
        new[:-1]    += cur[1:]
        new[1:]     += cur[:-1]
        new[:, :-1] += cur[:, 1:]
        new[:, 1:]  += cur[:, :-1]
        new *= num_masks[i]
        cur = new
        if np.sum(cur) == 0:
            return 0
    return np.sum(cur)

def part1(grid: List[str]):
    h = len(grid)
    w = len(grid[0])

    heights = [list(map(int, line)) for line in grid]
    heights_arr = np.array(heights)

    # We dont want to duplicate this tuff

    # we could do some bitshift stuff here
    # If it was number of paths, I could make this really fast.

    num_masks = [np.zeros((h, w), dtype=bool) for _ in range(10)]
    for i in range(10):
        num_masks[i] |= heights_arr == i

    out = 0
    for r, c in zip(*np.nonzero(num_masks[0])):
        out += num_9s_accessible(r, c, num_masks)
        #num_paths_to_9s = num_ways_to_get_9s(r, c, num_masks)
        #if num_paths_to_9s > 1:
        #    available = num_9s_accessible(r, c, num_masks)
        #    print(available)
        #    out += available

    return out


def part2(grid: List[str]):
    return None

if __name__ == '__main__':
    get_results("P1 Example", part1, read_grid, "example.txt")
    get_results("P1 Example 2", part1, read_grid, "example2.txt")
    get_results("P1", part1, read_grid, "input.txt")

    get_results("P2 Example", part2, read_grid, "example.txt")
    get_results("P2", part2, read_grid, "input.txt")