from util.point2d import Point2D
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

replace_strs = {
    "#": "##",
    ".": "..",
    "@": "@.",
    "O": "[]"
}

def score_grid(grid: List[List[str]]) -> int:
    h = len(grid)
    w = len(grid[0])
    out = 0
    for r in range(h):
        for c in range(w):
            if grid[r][c] == 'O':
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
    return ["".join(replace_strs[c] for c in line) for line in grid_str]

def part2(line_blocks):
    grid_str = widen_grid(line_blocks[0])
    move_sequence = "".join(line_blocks[1])
    grid = Grid2DDense([list(line) for line in grid_str])
    h, w = grid.shape

    bot_pos = None
    for r, c in grid.row_major_indexes():
        if grid_str[r][c] == '@':
            bot_pos = Point2D(c, r)
            break
    print(bot_pos)
    grid.set(bot_pos, '.')
    grid.display()

    for move in move_sequence:
        #grid.set(bot_pos, '.')
        direction = direction_map[move]

        initial_pos = bot_pos + direction
        cur_pos = initial_pos

        # L/R
        if direction.y == 0:
            # Move across boxes.
            while grid.get(cur_pos) in '[]':
                cur_pos = cur_pos + direction

            # If empty after boxes (if any)
            if grid.get(cur_pos) == '.':
                # Shift it down.
                p = cur_pos
                while p.x != initial_pos.x:
                    next_p = p - direction
                    grid.set(p, grid.get(next_p))
                    p = next_p
                grid.set(p, '.')
                bot_pos = initial_pos

                #grid.set(bot_pos, '@')
                grid.display()
                print("Shifted LR")
                print("new bot pos", bot_pos)

        #grid.set(bot_pos, '@')
        #grid.display()


if __name__ == '__main__':
    get_results("P1 Example", part1, read_line_blocks, "examplesmall.txt", expected=2028)
    get_results("P1 Example", part1, read_line_blocks, "example.txt", expected=10092)
    get_results("P1", part1, read_line_blocks, "input.txt")

    get_results("P2 Example", part2, read_line_blocks, "example.txt", expected=9021)
    #get_results("P2", part2, read_line_blocks, "input.txt")