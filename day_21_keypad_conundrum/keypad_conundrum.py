import collections
from util.timer import get_results
from util.util import seek_character
from parser.parser import read_lines
from typing import List, Optional


ACTIONS = ['^', 'A', '<',  'v', '>']
directional_keypad: List[List[Optional[str]]] = [[None, '^', 'A'],
                                                 ['<',  'v', '>']]

numeric_keypad: List[List[Optional[str]]] = [['7', '8', '9'],
                                             ['4', '5', '6'],
                                             ['1', '2', '3'],
                                            [None, '0', 'A']]

def solution(lines, n):
    paths_map = get_paths_map(directional_keypad, ACTIONS)
    path_costs = collections.defaultdict(lambda: 0) # It costs the human nothing to move from button to button.

    for i in range(n):
        new_path_costs = {}

        for a in ACTIONS:
            for b in ACTIONS:
                new_path_costs[(a, b)] = min(
                    get_next_path_cost(path_costs, middle_path)
                    for middle_path in paths_map[a, b]  # We try all the possible paths to get between them
                )
        path_costs = new_path_costs

    number_paths_map = get_paths_map(numeric_keypad, "0123456789A")

    out = 0
    for code in lines:
        min_presses = min_presses_for_code(code, number_paths_map, path_costs)
        numeric_part = int(code[:-1])
        out += numeric_part * min_presses
    return out

def part1(lines):
    return solution(lines, 2)

def part2(lines):
    return solution(lines, 25)

# https://www.reddit.com/r/adventofcode/comments/1hj2odw/comment/m35t63r/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
# Similar approach to hrunt
def get_paths_map(keypad: List[List[Optional[str]]], buttons):
    paths_map = {}
    for a in buttons:
        r1, c1 = seek_character(keypad, a)
        for b in buttons:
            r2, c2 = seek_character(keypad, b)

            dr, dc = r2 - r1, c2 - c1

            x_moves = ('<' if dc < 0 else '>'), abs(dc)
            y_moves = ('^' if dr < 0 else 'v'), abs(dr)

            if dr == 0: # Horizontal
                paths_map[a, b] = [[x_moves]]
            elif dc == 0:   # Vertical
                paths_map[a, b] = [[y_moves]]
            elif keypad[r1][c2] is None:    # Initially moving horizontally would shove us off the map
                paths_map[a, b] = [[y_moves, x_moves]]
            elif keypad[r2][c1] is None:    # Initially moving vertically would put os off the map
                paths_map[a, b] = [[x_moves, y_moves]]
            else:                                       # We may move V, H or H, V
                paths_map[a, b] = [[x_moves, y_moves], [y_moves, x_moves]]
    return paths_map

def get_next_path_cost(path_costs, middle_path):
    out = 0
    # Get to the first one
    prev = 'A'
    for tile, amt in middle_path:
        if amt == 0:
            continue
        out += path_costs[prev, tile]   # Cost to get to this tile
        out += amt                      # Cost of pushing it that many times
        prev = tile
    out += path_costs[prev, 'A']    # Cost of returning to A.
    return out

def min_presses_for_code(code, number_paths_map, direction_path_costs):
    out = 0
    for a, b in zip('A' + code, code):
        out += min(get_next_path_cost(direction_path_costs, path) for path in number_paths_map[a, b]) + 1
    return out


if __name__ == '__main__':
    get_results("P1 Example", part1, read_lines, "example.txt", expected=126384)
    get_results("P1", part1, read_lines, "input.txt")

    get_results("P2 Example", part2, read_lines, "example.txt")
    get_results("P2", part2, read_lines, "input.txt", expected=216668579770346)
