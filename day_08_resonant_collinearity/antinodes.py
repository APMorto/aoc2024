import timeit
from collections import defaultdict
import math
from typing import List, Dict

from parser.parser import read_grid
from util.timer import get_results

def sq_dist(r1, c1, r2, c2):
    return (r1 - r2) ** 2 + (c1 - c2) ** 2

def read_antenna_positions(grid: List[str]) -> Dict[str, List[tuple]]:
    positions = defaultdict(list)
    for r, line in enumerate(grid):
        for c, char in enumerate(line):
            if char != '.':
                positions[char].append((r, c))

    return positions

def get_sq_position_distances(pos, positions: List[tuple]):
    r, c = pos
    return {sq_dist(r, c, r2, c2) for r2, c2 in positions}

def position_is_antinode(pos, positions):
    sq_distances = get_sq_position_distances(pos, positions)
    return 0 not in sq_distances and any(math.sqrt(d) % 1 == 0 and  d*4 in sq_distances for d in sq_distances)   # 2*d1 = d2 => 2*2*d1*d1 = d2*d2

def display_antinode_locations(grid, positions):
    new_grid = [list(line) for line in grid]
    for r, c in positions:
        new_grid[r][c] = "#"
    for line in new_grid:
        print("".join(line))

def antinode_positions_for_pair(r1, c1, r2, c2, h, w):
    dr = r2 - r1
    dc = c2 - c1

    return filter(lambda rc: 0 <= rc[0] < h and 0 <= rc[1] < w,
        ((r1 - dr, c1 - dc),
        (r2 + dr, c2 + dc))
    )

def antinode_positions_for_pair_p2(r1, c1, r2, c2, h, w):
    dr = r2 - r1
    dc = c2 - c1

    n_steps = math.gcd(abs(dr), abs(dc))
    r_step, c_step = dr // n_steps, dc // n_steps

    # Go off in both directions, and in between. And on top of them.
    # off p1
    r, c = r1, c1
    while 0 <= r < h and 0 <= c < w:
        yield r, c
        r -= r_step
        c -= c_step

    # off p2
    r, c = r2, c2
    while 0 <= r < h and 0 <= c < w:
        yield r, c
        r += r_step
        c += c_step

    # between
    r, c = r1 + r_step, c1 + c_step
    while r != r2 and c != c2:
        yield r, c
        r += r_step
        c += c_step

def antinode_positions_for_frequency(frequency_positions: List[tuple], acc: set, h, w):
    n = len(frequency_positions)
    for i in range(n):
        for j in range(i + 1, n):
            acc.update(antinode_positions_for_pair(*frequency_positions[i], *frequency_positions[j], h, w))

def antinode_positions_for_frequency_p2(frequency_positions: List[tuple], acc: set, h, w):
    n = len(frequency_positions)
    for i in range(n):
        for j in range(i + 1, n):
            acc.update(antinode_positions_for_pair_p2(*frequency_positions[i], *frequency_positions[j], h, w))


def part1(grid: List[str]):
    h = len(grid)
    w = len(grid[0])

    # Is distance Euclidean distance?
    all_positions = read_antenna_positions(grid)

    antinode_positions = set()
    for char, positions in all_positions.items():
        antinode_positions_for_frequency(positions, antinode_positions, h, w)

    #print(antinode_positions)
    #display_antinode_locations(grid, antinode_positions)

    return len(antinode_positions)


def part2(grid: List[str]):
    h = len(grid)
    w = len(grid[0])

    # Is distance Euclidean distance?
    all_positions = read_antenna_positions(grid)

    antinode_positions = set()
    for char, positions in all_positions.items():
        antinode_positions_for_frequency_p2(positions, antinode_positions, h, w)

    #print(antinode_positions)
    #display_antinode_locations(grid, antinode_positions)

    return len(antinode_positions)


if __name__ == '__main__':
    get_results("P1 example", part1, read_grid, "example.txt")
    get_results("P1", part1, read_grid, "input.txt")

    get_results("P2 example", part2, read_grid, "example.txt")
    get_results("P2", part2, read_grid, "input.txt")



