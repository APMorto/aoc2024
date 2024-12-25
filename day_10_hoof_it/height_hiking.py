from math import ceil
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

# Lets speed up part 1. 0.111s is pathetic.
# A path has a manhatten distance <= 9
# So, we could do the same approach to a 19x19 squared centered on the point
# Or, just do bitsets to represent where we came from
# bits can be reused, provided they are based >= 20 manhatten distance apart.
# At 201 zeros, we can MAYBE achieve this. Only 157 9s though, so that should be easier.
# But at 44x44, the square approach kinda sucks.
# We could also just like, not bother with the optimal packing and just do it 4x64 bit / 2x128 bit (if available) or even just 256 bit.

def part1_bitwise(grid: List[str]):
    h = len(grid)
    w = len(grid[0])

    heights = [list(map(int, line)) for line in grid]
    heights_arr = np.array(heights)

    # num_masks[height][r, c] = 1 if heights[r, c] == height else 0
    num_masks = [np.zeros((h, w), dtype=bool) for _ in range(10)]
    for i in range(10):
        num_masks[i] |= heights_arr == i
    out = 0

    # We can only go up to 64 bits per integer.
    NUM_BITS = 64

    # Each ending position is represented by some bit index number. It is crucial that these never overlap.
    # For a quick check, they wont ever overlap if their manhatten distance is >= 20, as they can only propagate so far.
    # I don't do that because its possible doing that semi optimally would take longer. For a larger grid, it would make sense.
    nine_rows, nine_cols = np.where(num_masks[9])
    num_9s = len(nine_rows)
    for block in range(ceil(num_9s / NUM_BITS)):
        # Set each of up to 64 9s to their own bit index.
        start_array = np.zeros((h, w), dtype=np.uint64)
        block_length = min(64, num_9s - block * NUM_BITS)
        start_array[nine_rows[block*NUM_BITS : (block+1)*NUM_BITS], nine_cols[block*NUM_BITS : (block+1)*NUM_BITS]] = 1 << np.arange(block_length)
        cur = start_array

        # Bitwise OR all adjacent ones together, then mask with the next level.
        for i in range(8, -1, -1):
            new = np.zeros((h, w), dtype=np.uint64)
            new[:-1]    |= cur[1:]
            new[1:]     |= cur[:-1]
            new[:, :-1] |= cur[:, 1:]
            new[:, 1:]  |= cur[:, :-1]
            new *= num_masks[i]
            cur = new
        # https://stackoverflow.com/questions/63954102/numpy-vectorized-way-to-count-non-zero-bits-in-array-of-integers
        out += np.unpackbits(cur.view('uint8')).sum()   # Total number of 1 bits (on 0s)
    return out

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

    # DP, duplicates are allowed.
    # The one concern here is how much wasted we have.
    # Luckily no overflow.

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

    # We dont want to duplicate this stuff

    # we could do some bitshift stuff here
    # If it was number of paths, I could make this really fast.

    num_masks = [np.zeros((h, w), dtype=bool) for _ in range(10)]
    for i in range(10):
        num_masks[i] |= heights_arr == i

    out = 0
    for r, c in zip(*np.nonzero(num_masks[0])):
        # Number of distinct destinations
        out += num_9s_accessible(r, c, num_masks)

    return out


def part2(grid: List[str]):
    h = len(grid)
    w = len(grid[0])

    heights = [list(map(int, line)) for line in grid]
    heights_arr = np.array(heights)

    # It's faster to do everything in 1 array now, since we don't care about duplication
    cur = heights_arr * heights_arr==0
    for i in range(1, 10):
        new = np.zeros((h, w), dtype=np.long)
        new[:-1]    += cur[1:]
        new[1:]     += cur[:-1]
        new[:, :-1] += cur[:, 1:]
        new[:, 1:]  += cur[:, :-1]
        new *= heights_arr==i
        cur = new
    return np.sum(cur)

    #num_masks = [np.zeros((h, w), dtype=bool) for _ in range(10)]
    #for i in range(10):
    #    num_masks[i] |= heights_arr == i
#
    #out = 0
    #for r, c in zip(*np.nonzero(num_masks[0])):
    #    # Number of ways to get
    #    out += num_ways_to_get_9s(r, c, num_masks)
#
    #return out


# So the notion of a trailhead is just nothing. Here I thought it was important, but no.


if __name__ == '__main__':
    get_results("P1 Example", part1, read_grid, "example.txt")
    get_results("P1 Example 2", part1, read_grid, "example2.txt")
    get_results("P1", part1, read_grid, "input.txt")
    get_results("P1 Bitwise", part1_bitwise, read_grid, "input.txt")

    get_results("P2 Example", part2, read_grid, "example.txt")
    get_results("P2 Example 2", part2, read_grid, "example2.txt")
    get_results("P2", part2, read_grid, "input.txt")

    get_results("P2 Custom 500x500", part2, read_grid, "custom_500.txt")
    get_results("P2 Custom 1000x1000", part2, read_grid, "custom_1000.txt")
    #get_results("P2 Custom 10000x10000", part2, read_grid, "custom_10000.txt")

    get_results("P1 Challenge", part1, read_grid, "challenge.txt")
    get_results("P2 Challenge", part2, read_grid, "challenge.txt")