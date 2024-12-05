import sys
from itertools import chain

from parser.parser import read_grid


def day1(fp):
    grid = read_grid(fp)

    print(grid)

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

def day2(fp):
    grid = read_grid(fp)

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

            # These flip operations define an abelian group with the order of each element/operation being two
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
    print(day1("example.txt"))
    print(day1("p1.txt"))
    print(day2("example.txt"))
    print(day2("p1.txt"))
