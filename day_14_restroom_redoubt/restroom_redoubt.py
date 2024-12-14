import operator
from collections import defaultdict
from functools import reduce
from itertools import chain
from typing import List
import matplotlib.pyplot as plt

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

    STEPS = 100

    quadrant_counts = [[0, 0], [0, 0]]
    for px, py, vx, vy in read_robots(lines):
        final_x = (px + vx * STEPS) % w
        final_y = (py + vy * STEPS) % h

        # Positions on the exact middle dont count.
        if final_x == half_w or final_y == half_h:
            continue

        quadrant_counts[final_x < half_w][final_y < half_h] += 1
    return reduce(operator.mul, chain(*quadrant_counts), 1)


def part2(lines: List[str]):
    w = int(lines[0][2:])
    h = int(lines[1][2:])
    half_w = w // 2 if w % 2 == 1 else None
    half_h = h // 2 if h % 2 == 1 else None
    #print(half_w, half_h)
    bot_positions = tuple(read_robots(lines))
    BLOCKSIZE = 5
    blocks_w = w // BLOCKSIZE + 1
    blocks_h = h // BLOCKSIZE + 1
    num_evaluated = 1
    total = 0
    scores = []

    for steps in range(134, 10509):
        final_position_counts = defaultdict(int)
        blocks = [[0] * blocks_w for _ in range(blocks_h)]
        for px, py, vx, vy in bot_positions:

            final_x = (px + vx * steps) % w
            final_y = (py + vy * steps) % h
            final_position_counts[(final_x, final_y)] += 1
        # I assert that things will be pretty grouped for a tree
        for r in range(h):
            for c in range(w):
                if final_position_counts[(c, r)] > 0:
                    blocks[r // BLOCKSIZE][c // BLOCKSIZE] += 1

        block_score = 0
        for block_amt in chain(*blocks):
            block_score += block_amt ** 2


        # We have block counts
        # take the square and whatver
        print("Steps =", steps)

        if block_score * 0.5 > total / num_evaluated:
            for r in range(h):
                for c in range(w):
                    if final_position_counts[(c, r)] > 0:
                        print("#", end="")
                    else:
                        print(" ", end="")
                if r != h-1:
                    print()
            plt.hist(scores.copy(), bins=100)
            plt.show()
            input()
            print()
        num_evaluated += 1
        total += block_score
        scores.append(block_score)

# > 134
# < 10509

if __name__ == '__main__':
    get_results("P1 Example", part1, read_lines, "example.txt", expected=12)
    get_results("P1", part1, read_lines, "input.txt")

    #get_results("P2 Example", part2, read_lines, "example.txt")
    get_results("P2", part2, read_lines, "input.txt")