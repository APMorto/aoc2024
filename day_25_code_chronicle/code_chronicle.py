from collections import defaultdict

from util.timer import get_results
from parser.parser import read_lines, read_line, read_grid, read_list_grid, read_line_blocks
from typing import List, Tuple


# Keys are filled at the top, schematics are filled at the bottom
# Just find the ones that fit together, pretty easy.

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
    return fill == '.', tuple(code)


def part1(line_blocks: List[List[str]]):
    key_counter = defaultdict(int)
    lock_counter = defaultdict(int)
    for schematic in line_blocks:
        is_key, code = read_schematic(schematic)
        print(schematic)
        print(is_key, code)
        if is_key:
            key_counter[code] += 1
        else:
            lock_counter[code] += 1
    return sum(key_amt * lock_counter[code] for code, key_amt in key_counter.items())



def part2(_):
    pass


if __name__ == '__main__':
    get_results("P1 Example", part1, read_line_blocks, "example.txt", expected=3)
    get_results("P1", part1, read_line_blocks, "input.txt")

    get_results("P2 Example", part2, read_line_blocks, "example.txt")
    get_results("P2", part2, read_line_blocks, "input.txt")