from collections import defaultdict

from util.timer import get_results
from parser.parser import read_lines, read_line, read_grid, read_list_grid, read_line_blocks
from typing import List, Tuple


# Keys are filled at the top, schematics are filled at the bottom
# Just find the ones that fit together, pretty easy.
# We need non overlapping, not all that perfectly fit...
# And there are 500

def read_schematic(schematic: List[str]) -> Tuple[bool, tuple]:
    fill = schematic[0][0]  # '.' for key, '#' for lock
    code = [0] * 5
    for c in range(5):
        h = 6
        for r in range(1, 6):
            if schematic[r][c] != fill:
                h = r
                break
        code[c] = h
    return fill == '#', tuple(code)


def part1(line_blocks: List[List[str]]):
    keys = []
    locks = []
    for schematic in line_blocks:
        is_key, code = read_schematic(schematic)
        if is_key:
            keys.append(code)
        else:
            locks.append(code)
    # The whole sorting and cutting early barely saves ANYTHING, like 1ms at most.
    keys.sort()#key=lambda code: code[0])

    out = 0
    for lock in locks:
        for key in keys:    # Keys are filled from the bottom.
            if key[0] > lock[0]:    # Sorted by first value.
                break
            fits = True
            for c in range(1, 5):
                if key[c] > lock[c]:
                    fits = False
            if fits:
                out += 1
    return out

def part2(_):
    pass


if __name__ == '__main__':
    get_results("P1 Example", part1, read_line_blocks, "example.txt", expected=3)
    get_results("P1", part1, read_line_blocks, "input.txt", expected=3360)

    get_results("P2 Example", part2, read_line_blocks, "example.txt")
    get_results("P2", part2, read_line_blocks, "input.txt")