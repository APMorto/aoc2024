from collections import defaultdict
from typing import List, Dict

from parser.parser import read_grid
from util.timer import get_results

def sq_dist(r1, c1, r2, c2):
    return (r1 - r2) ** 2 + (c1 - c2) ** 2

def read_antenna_positions(grid: List[str]) -> Dict[str, List[int]]:
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
    return 0 not in sq_distances and any(d*4 in sq_distances for d in sq_distances)   # 2*d1 = d2 => 2*2*d1*d1 = d2*d2

def display_antinode_locations(grid, positions):
    new_grid = [list(line) for line in grid]
    for r, c in positions:
        new_grid[r][c] = "#"
    for line in new_grid:
        print("".join(line))

def part1(grid: List[str]):
    h = len(grid)
    w = len(grid[0])

    # Is distance Euclidean distance?
    all_positions = read_antenna_positions(grid)

    antinode_positions = set()
    for char, positions in all_positions.items():
        for r in range(h):
            for c in range(w):
                if (r, c) in positions:
                    continue
                if position_is_antinode((r, c), positions):
                    antinode_positions.add((r, c))

    print(antinode_positions)
    display_antinode_locations(grid, antinode_positions)

    return len(antinode_positions)


if __name__ == '__main__':
    get_results("P1 example", part1, read_grid, "example.txt")




