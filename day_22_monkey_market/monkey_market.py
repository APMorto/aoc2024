from util.timer import get_results
from parser.parser import read_lines, read_line, read_grid, read_list_grid, read_line_blocks
from typing import List

MOD = 16777216 # 1 << 24
PRUNE_MASK = (1 << 24) - 1  # 0b[1]^24
P1_ITERS = 2000

def kth_secret_number(initial_secret_number: int, k: int) -> int:
    cur = initial_secret_number
    for _ in range(k):
        #cur = (cur ^ (cur << 6) ^ (cur >> 5) ^ (cur << 11)) & PRUNE_MASK
        cur = (cur ^ (cur << 6)) & PRUNE_MASK   # We iteratively mix and prune it.
        cur = (cur ^ (cur >> 5)) & PRUNE_MASK
        cur = (cur ^ (cur << 11)) & PRUNE_MASK
    return cur

def part1(lines: List[str]):
    out = 0
    for line in lines:
        num = int(line)
        two_thousands_secret = kth_secret_number(num, P1_ITERS)
        #print(num, two_thousands_secret)
        out += two_thousands_secret
    return out





def part2(_):
    pass

#for i in range(10):
#    print(kth_secret_number(123, i))

if __name__ == '__main__':
    get_results("P1 Example", part1, read_lines, "example.txt", expected=37327623)
    get_results("P1", part1, read_lines, "input.txt")

    get_results("P2 Example", part2, read_lines, "example.txt")
    get_results("P2", part2, read_lines, "input.txt")