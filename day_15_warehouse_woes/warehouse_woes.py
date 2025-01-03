from util.timer import get_results
from parser.parser import read_lines, read_line, read_grid, read_list_grid, read_line_blocks
from typing import List
from util.grid2d import Grid2DDense
from util.point2d import Point2D

direction_map = {
    '>': Point2D(1, 0),
    '<': Point2D(-1, 0),
    '^': Point2D(0, -1),
    'v': Point2D(0, 1),
}

replace_strs_p2_expansion = {
    "#": "##",
    ".": "..",
    "@": "@.",
    "O": "[]"
}

def score_grid(grid: List[List[str]], desired='O') -> int:
    h = len(grid)
    w = len(grid[0])
    out = 0
    for r in range(h):
        for c in range(w):
            if grid[r][c] == desired:
                out += 100 * r + c
    return out

def part1(line_blocks):
    grid_str = line_blocks[0]
    grid = Grid2DDense([list(line) for line in grid_str])
    move_sequence = "".join(line_blocks[1])
    h, w = grid.shape

    bot_pos = None
    for r, c in grid.row_major_indexes():
        if grid_str[r][c] == '@':
            bot_pos = Point2D(r, c)
            break
    print(bot_pos)
    grid.set(bot_pos, '.')

    for move in move_sequence:
        grid.set(bot_pos, '.')
        direction = direction_map[move]

        # Can we move that way?
        # Propagate until we see a . or #
        # If its a . first, we move
        # if its a # first, we don't move.
        initial_pos = bot_pos + direction
        cur_pos = initial_pos
        while grid.get(cur_pos) == 'O':
            cur_pos = cur_pos + direction

        # We can actually move.
        if grid.get(cur_pos) == '.':
            grid.swap(initial_pos, cur_pos)
            bot_pos = initial_pos

        grid.set(bot_pos, '@')
        #grid.display()

    return score_grid(grid.grid)

def widen_grid(grid_str: List[str]):
    return ["".join(replace_strs_p2_expansion[c] for c in line) for line in grid_str]

def check_if_can_move_UD_p2(grid: Grid2DDense, pos: Point2D, direction: Point2D, seen=None):
    seen = set() if seen is None else seen
    if pos in seen:
        return True
    seen.add(pos)
    c = grid.get(pos)
    if c == '#':
        return False
    elif c == '.':
        return True

    # []
    if c == '[':
        return check_if_can_move_UD_p2(grid, pos + direction, direction, seen) and check_if_can_move_UD_p2(grid, pos + Point2D(1, 0), direction, seen)
    elif c == ']':
        return check_if_can_move_UD_p2(grid, pos + direction, direction, seen) and check_if_can_move_UD_p2(grid, pos + Point2D(-1, 0), direction, seen)
    else:
        raise ValueError("Somehow propagated to invalid value: " + str(c))

def move_UD_p2_set(grid: Grid2DDense, direction: Point2D, seen):
    sorted_seen = sorted(seen, key=lambda p: p.y, reverse=direction.y > 0)
    for p in sorted_seen:
        before = p - direction
        if before in seen:
            grid.set(p, grid.get(before))
        else:
            grid.set(p, '.')


def move_UD_p2_non_set(grid: Grid2DDense, pos, direction: Point2D):
    c = grid.get(pos)
    if c == '#':
        raise ValueError("Somehow propagated to invalid value in moving: " + str(c))
    elif c == '.':
        grid.set(pos, grid.get(pos - direction))
    elif c == '[':
        move_UD_p2_non_set(grid, pos + direction, direction)
        move_UD_p2_non_set(grid, pos + direction + Point2D(1, 0), direction)
    else:
        move_UD_p2_non_set(grid, pos + direction, direction)
        move_UD_p2_non_set(grid, pos + direction + Point2D(-1, 0), direction)

# We may move multiple times.
def check_if_can_move_UD_p2_non_set(grid: Grid2DDense, pos: Point2D, direction: Point2D):
    # Exponential worst case
    c = grid.get(pos)
    if c == '#':
        return False
    elif c == '.':
        return True
    elif c == '[':
        # Check both above.
        return check_if_can_move_UD_p2_non_set(grid, Point2D(pos.x, pos.y+direction.y), direction) and check_if_can_move_UD_p2_non_set(grid, Point2D(pos.x+1, pos.y+direction.y), direction)
    else: # c == ']'
        # Basic check to not branch on perfect aligned boxes
        if grid.get(pos - direction) == ']':
            return True
        return check_if_can_move_UD_p2_non_set(grid, Point2D(pos.x-1, pos.y + direction.y), direction) and check_if_can_move_UD_p2_non_set(grid, Point2D(pos.x, pos.y + direction.y), direction)



def part2(line_blocks):
    grid_str = widen_grid(line_blocks[0])
    move_sequence = "".join(line_blocks[1])
    grid = Grid2DDense([list(line) for line in grid_str])
    #h, w = grid.shape

    bot_pos = None
    for r, c in grid.row_major_indexes():
        if grid_str[r][c] == '@':
            bot_pos = Point2D(c, r)
            break
    grid.set(bot_pos, '.')

    for move in move_sequence:
        direction = direction_map[move]
        initial_pos = bot_pos + direction

        # L/R
        if direction.y == 0:
            # Move across boxes.
            cur_pos = initial_pos
            while grid.get(cur_pos) in '[]':
                cur_pos = cur_pos + direction

            # If empty after boxes (if any)
            if grid.get(cur_pos) == '.':
                # Shift it down. Takes ~0.006s
                p = cur_pos
                while p.x != initial_pos.x:
                    next_p = p - direction
                    grid.set(p, grid.get(next_p))
                    p = next_p
                grid.set(p, '.')
                #if cur_pos != initial_pos:
                #    grid.horizontal_shift(cur_pos.y, initial_pos.x, cur_pos.x, direction.x, '.')
                bot_pos = initial_pos

        else:   # U/D (takes like 2/3 of the total time)
            # 2 approaches:
            # Check all with set, then move the set
            # Or, check all (maybe set), then move with standard dfs
            if grid.get(initial_pos) != '.':
                seen = set()
                if check_if_can_move_UD_p2(grid, initial_pos, direction, seen):
                    move_UD_p2_set(grid, direction, seen)   # Takes 0.004s
                    bot_pos = initial_pos
            else:
                bot_pos = initial_pos

            # Would be faster, but there is a branching issue with checking, and a correctness duplication issue with actually moving
            #if check_if_can_move_UD_p2_non_set(grid, cur_pos, direction):
            #    move_UD_p2_non_set(grid, cur_pos, direction)
            #    bot_pos = initial_pos


    return score_grid(grid.grid, desired='[')


if __name__ == '__main__':
    get_results("P1 Example", part1, read_line_blocks, "examplesmall.txt", expected=2028)
    get_results("P1 Example", part1, read_line_blocks, "example.txt", expected=10092)
    get_results("P1", part1, read_line_blocks, "input.txt")

    get_results("P2 Example", part2, read_line_blocks, "example.txt", expected=9021)
    get_results("P2", part2, read_line_blocks, "input.txt")