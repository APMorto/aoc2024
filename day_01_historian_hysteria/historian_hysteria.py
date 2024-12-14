from collections import Counter

from util.timer import get_results
from parser.parser import read_lines, read_line, read_grid, read_list_grid, read_line_blocks
from typing import List


def part1(lines):
    l1, l2 = zip(*(map(int, line.split()) for line in lines))
    return sum(abs(a-b) for a, b in zip(sorted(l1), sorted(l2)))

def part2(lines):
    l1, l2 = map(Counter, zip(*(map(int, line.split()) for line in lines)))
    return sum(amt * val * l2[val] for val, amt in l1.items())

if __name__ == '__main__':
    get_results("P1 Example", part1, read_lines, "example.txt", expected=11)
    get_results("P1", part1, read_lines, "input.txt")

    get_results("P2 Example", part2, read_lines, "example.txt", expected=31)
    get_results("P2", part2, read_lines, "input.txt")