import math
from collections import defaultdict

from parser.parser import read_line
from util.timer import get_results


# Rules:
#   0 -> 1
#   Even number of digits -> left half, right half
#   _ -> *= 2024

# after [25 / 75] blinks, how many stones will you have?

def get_stone_counts(line: str):
    counts = defaultdict(int)
    for num in map(int, line.split()):
        counts[num] += 1
    return counts

def blink_n_times(line, n):
    counts = get_stone_counts(line)

    for blink in range(n):
        # is dict faster? VERY slightly it seems, but it makes the code look terrible.
        new_counts = defaultdict(int)

        for num, amt in counts.items():
            if num == 0:
                new_counts[1] += amt
            elif (d := math.floor(math.log10(num)) + 1) % 2 == 0:
                power = (10 ** (d // 2))
                new_counts[num % power] += amt
                new_counts[num // power] += amt

            # elif (d := len(str(num))) % 2 == 0:   # String parsing is slower.
                #new_counts[int(s[:d//2])] += num
                #new_counts[int(s[d // 2:])] += num
            else:
                new_counts[num * 2024] += amt
        counts = new_counts

    #print("Average packing:", sum(counts.values()) / len(counts))   # Average packing: 58264724147.719986 for p2
    return sum(counts.values())

def part1(line):
    return blink_n_times(line, 25)

def part2(line):
    return blink_n_times(line, 75)

# Interestingly, I think this can be represented by a (potentially) infinitely sized matrix. Call it M
# Then our solutions is just sum(INPUT * M ^ 75)
# where M ^ 75 can be calculated recursively in logarithmic time
# or potentially in ~~linear time if it is diagonalizable.
# However we do not know what numbers will actually need to be present in the matrix.
# And the matrix is sufficiently large, with the number of multiplications being sufficiently small that this may not
#   be that beneficial.


if __name__ == '__main__':
    get_results("P1 Example", part1, read_line, "example.txt")
    get_results("P1 Example 2", part1, read_line, "example2.txt")
    get_results("P1", part1, read_line, "input.txt")

    get_results("P2 Example", part2, read_line, "example.txt")
    get_results("P2", part2, read_line, "input.txt")

    get_results("Reddit 1k", lambda line: blink_n_times(line, 1000), read_line, "example.txt")
    get_results("Reddit 10k", lambda line: blink_n_times(line, 10_000), read_line, "example.txt")