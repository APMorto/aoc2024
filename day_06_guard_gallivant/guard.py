from itertools import chain

from parser.parser import read_grid, read_list_grid
from util.directions import Direction2D, offset_2D


def day1(fp):
    grid = read_list_grid(fp)
    h = len(grid)
    w = len(grid[0])

    # Find initial position.
    r = -1
    c = -1
    for i in range(h):
        for j in range(w):
            if grid[i][j] == '^':
                r = i
                c = j
                break

    # Guard eventually leaves.
    # thus no need for complicated cycle detection
    direction = Direction2D.UP
    while True:
        grid[r][c] = '*'    # Mark cur pos as visited.
        ro, co = offset_2D(direction)

        # Left.
        if not (0 <= r + ro < h and 0 <= c + co < w):
            break

        if grid[r + ro][c + co] == '#':
            direction = direction.turn_right()

        else:
            r += ro
            c += co

    # Just count how many places we went to
    return sum(ch == '*' for ch in chain(*grid))



if __name__ == '__main__':
    print(day1('example.txt'))
    print(day1('input'))