from typing import List

from parser.parser import read_grid
from util.timer import get_results


def part1(grid):

    h = len(grid)
    w = len(grid[0])

    target = "XMAS" # May be backwards
    rev_target = target[::-1]   # != target, crucially

    accept_set = (target, rev_target)   # two elements, so no need for fancy set
    m = len(target)

    out = 0

    for r in range(h):
        for c in range(w):
            if w - c >= m and grid[r][c:c+m] in accept_set: # Right/left
                out += 1
            if h - r >= m and "".join(grid[rr][c] for rr in range(r, r+m)) in accept_set:   # up/down
                out += 1
            if h - r >= m and w - c >= m and "".join(grid[r+i][c+i] for i in range(m)) in accept_set:   # \
                out += 1
            if h - r >= m and w - c >= m and "".join(grid[r+m-1-i][c+i] for i in range(m)) in accept_set:   # /
                out += 1

    return out

# 0.013 vs 0.033 for above (pypy)
def part1_faster(grid: List[str]):
    h = len(grid)
    w = len(grid[0])

    out = 0
    for r in range(h):
        for c in range(w):
            if grid[r][c] == 'X':
                if c >= 3 and grid[r][c-3:c] == "SAM":   # <-
                    out += 1
                if c + 4 <= w and grid[r][c+1:c+4] == "MAS": # ->
                    out += 1
                if r >= 3 and grid[r-1][c] == 'M' and grid[r-2][c] == 'A' and grid[r-3][c] == 'S':  # ^
                    out += 1
                if r + 4 <= h and grid[r+1][c] == 'M' and grid[r+2][c] == 'A' and grid[r+3][c] == 'S': # v
                    out += 1
                if r + 4 <= h and c + 4 <= w and grid[r+1][c+1] == 'M' and grid[r+2][c+2] == 'A' and grid[r+3][c+3] == 'S': # down right
                    out += 1
                if r + 4 <= h and c >= 3 and grid[r+1][c-1] == 'M' and grid[r+2][c-2] == 'A' and grid[r+3][c-3] == 'S': # down left
                    out += 1
                if r >= 3 and c + 4 <= w and grid[r-1][c+1] == 'M' and grid[r-2][c+2] == 'A' and grid[r-3][c+3] == 'S':  # up right
                    out += 1
                if r >= 3 and c >= 3 and grid[r-1][c-1] == 'M' and grid[r-2][c-2] == 'A' and grid[r-3][c-3] == 'S': # up left
                    out += 1
    return out


def part2(grid):
    h = len(grid)
    w = len(grid[0])

    # Can we enumerate all possible 3x3 grids?
    # Or perhaps, since were already constructing, just enumerate all possible 5 letter sequences

    # 0_1
    # _2_
    # 3_4

    accept_set = set()
    base_state = list('MMASS')
    for flip1 in (True, False):
        for flip2 in (True, False):
            if flip1:
                base_state[0], base_state[4] = base_state[4], base_state[0]
            if flip2:
                base_state[1], base_state[3] = base_state[3], base_state[1]

            accept_set.add(tuple(base_state))

            # These flip operations define an abelian group with the order of each (non identity) element/operation being two
            # Thus, doing the same action unsets it.
            if flip1:
                base_state[0], base_state[4] = base_state[4], base_state[0]
            if flip2:
                base_state[1], base_state[3] = base_state[3], base_state[1]

    # Now just get all these 5-letter states and check for acceptance.
    out = 0
    for r in range(h-2):
        for c in range(w-2):
            if (grid[r][c], grid[r][c+2], grid[r+1][c+1], grid[r+2][c], grid[r+2][c+2]) in accept_set:
                out += 1

    return out


if __name__ == "__main__":
    get_results("P1 Example", part1, read_grid, "example.txt")
    get_results("P1", part1, read_grid, "input.txt")
    get_results("P1 Faster", part1_faster, read_grid, "input.txt")

    get_results("P2 Example", part2, read_grid, "example.txt")
    get_results("P2", part2, read_grid, "input.txt")
