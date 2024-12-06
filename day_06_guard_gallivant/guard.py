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
        ro, co = direction.offset()

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

def day2(fp):
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

    direction = Direction2D.UP
    startR = r
    startC = c

    visited = set()

    # Now, how many places can we put that result in a cycle?
    # Cycles are not necessarily rectangular
    # Could Simulate all and just check for cycle?
    # Furthermore, it only really matters to place it in the positions where the guard would already walk!
    # And, we can do this while walking!
    # For each step, if we would NOT hit the rock, try doing it anyways



    out = 0

    while True:
        visited.add((r, c, direction))

        ro, co = direction.offset()

        if not (0 <= r + ro < h and 0 <= c + co < w):
            break

        if grid[r + ro][c + co] == '#':
            direction = direction.turn_right()
        else:
            if grid[r+ro][c+co] != '^' and not any((r+ro, c+co, d2) in visited for d2 in Direction2D): # Cant place on start, or where we have already been.

                grid[r+ro][c+co] = '#'

                # Traverse.
                if check_cycle(r, c, direction.turn_right(), visited, grid):
                    out += 1

                    # Mark it as 'start' so we dont bother checking again.
                    grid[r+ro][c+co] = '^'

                grid[r+ro][c+co] = '*' if grid[r+ro][c+co] != '^' else '^'

            # Now go forwards
            r += ro
            c += co

    return out

def check_cycle(r, c, direction, visited, grid):
    local_visited = set()
    h, w = len(grid), len(grid[0])

    while True:
        #print(local_visited)
        if (r, c, direction) in visited or (r, c, direction) in local_visited:
            return True

        local_visited.add((r, c, direction))

        grid[r][c] = '*'  # Mark cur pos as visited.
        ro, co = direction.offset()

        # Left the grid
        if not (0 <= r + ro < h and 0 <= c + co < w):
            return False

        if grid[r + ro][c + co] == '#':
            direction = direction.turn_right()

        else:
            r += ro
            c += co






if __name__ == '__main__':
    print(day1('example.txt'))
    print(day1('input'))
    print(day2('example.txt'))
    print(day2('input'))
