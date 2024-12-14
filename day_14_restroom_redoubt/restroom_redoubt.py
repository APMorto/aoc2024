import operator
from collections import defaultdict
from functools import reduce
from itertools import chain
from typing import List

from parser.parser import read_lines
from util.timer import get_results

# place this at the start of input files
# w=WIDTH
# h=HEIGHT

# Robots can share the same tile.
# Robots wrap around upon hitting the edge

def read_robots(input_lines: List[str]):
    # input_lines[0:2] is w, h
    for i in range(2, len(input_lines)):
        p, v = input_lines[i][2:].split(' v=')
        px, py = map(int, p.split(','))
        vx, vy = map(int, v.split(','))
        yield px, py, vx, vy


def part1(lines: List[str]):
    w = int(lines[0][2:])
    h = int(lines[1][2:])
    half_w = w // 2 if w % 2 == 1 else None
    half_h = h // 2 if h % 2 == 1 else None
    #print(half_w, half_h)

    STEPS = 100

    #final_position_counts = defaultdict(int)
    quadrant_counts = [[0, 0], [0, 0]]
    for px, py, vx, vy in read_robots(lines):
        final_x = (px + vx * STEPS) % w
        final_y = (py + vy * STEPS) % h
        #final_position_counts[(final_x, final_y)] += 1

        # Positions on the exact middle dont count.
        if final_x == half_w or final_y == half_h:
            continue

        #print(final_x // half_w)
        #print(final_y // half_h)
        quadrant_counts[final_x < half_w][final_y < half_h] += 1
    return reduce(operator.mul, chain(*quadrant_counts), 1)


def part2(lines: List[str]):
    return None

if __name__ == '__main__':
    get_results("P1 Example", part1, read_lines, "example.txt", expected=12)
    get_results("P1", part1, read_lines, "input.txt")

    get_results("P2 Example", part2, read_lines, "example.txt")
    get_results("P2", part2, read_lines, "input.txt")