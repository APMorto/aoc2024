from util.timer import get_results
from parser.parser import read_lines, read_line, read_grid, read_list_grid, read_line_blocks
from typing import List

def can_make(pattern, pattern_set, lengths):
    n = len(pattern)
    dp = [False] * (n+1)
    dp[0] = True
    for i in range(1, n+1):
        for l in lengths:
            if l > i:
                break
            if dp[i-l] and pattern[i-l: i] in pattern_set:
                dp[i] = True
                break

    return dp[n]


def part1(blocks: List[str]):
    pattern_set = set(blocks[0][0].split(", "))
    pattern_lengths = sorted(set(len(p) for p in pattern_set))

    out = 0
    for pattern in blocks[1]:
        if can_make(pattern, pattern_set, pattern_lengths):
            out += 1
    return out


def num_ways_to_make(pattern, pattern_set, lengths):
    n = len(pattern)
    dp = [0] * (n+1)
    dp[0] = 1
    for i in range(1, n+1):
        for l in lengths:
            if l > i:
                break
            if dp[i-l] and pattern[i-l: i] in pattern_set:
                dp[i] += dp[i-l]

    return dp[n]


def part2(blocks):
    pattern_set = set(blocks[0][0].split(", "))
    pattern_lengths = sorted(set(len(p) for p in pattern_set))

    out = 0
    for pattern in blocks[1]:
        out += num_ways_to_make(pattern, pattern_set, pattern_lengths)
    return out


if __name__ == '__main__':
    get_results("P1 Example", part1, read_line_blocks, "example.txt", expected=6)
    get_results("P1", part1, read_line_blocks, "input.txt")

    get_results("P2 Example", part2, read_line_blocks, "example.txt", expected=16)
    get_results("P2", part2, read_line_blocks, "input.txt")