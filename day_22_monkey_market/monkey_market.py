from collections import defaultdict

from util.timer import get_results
from parser.parser import read_lines, read_line, read_grid, read_list_grid, read_line_blocks
from typing import List

MOD = 16777216 # 1 << 24
#PRUNE_MASK = (1 << 24) - 1  # 0b[1]^24
P1_ITERS = 2000


#cur = (cur ^ (cur << 6) ^ (cur >> 5) ^ (cur << 11)) & PRUNE_MASK  # is WRONG! Because we need to update cur between uses.

def kth_secret_number(initial_secret_number: int, k: int) -> int:
    PRUNE_MASK = (1 << 24) - 1  # 0b[1]^24
    cur = initial_secret_number
    for _ in range(k):
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


# If we start part way into the sequence, we don't take it.
# We get to choose ONE sequence of four price changes.
# When the monkey sees that sequence (in its entirety), we buy the banana!
# We wish to maximize bananas.
# Simply store all sequences we've seen, packed into some integer.
# Then take the max.

def make_sequence_integer(*args):
    sequence_integer = 0
    CHANGE_WIDTH = 5
    SEQUENCE_MASK = (1 << (CHANGE_WIDTH * 4)) - 1
    for change in args:
        sequence_integer = ((sequence_integer << CHANGE_WIDTH) | (change+10)) & SEQUENCE_MASK
    return sequence_integer


def part2(lines: List[str]):
    PRUNE_MASK = (1 << 24) - 1  # 0b[1]^24
    CHANGE_WIDTH = 5
    SEQUENCE_MASK = (1 << (CHANGE_WIDTH * 4)) - 1
    #SECOND_SHIFT_MASK = ~((1<<23) | (1<<22) | (1<<21) | (1<<20) | (1<<19))  # 5 leftmost bits are to be gone
    #THIRD_SHIFT_MASK =
    counts = defaultdict(int)
    for line in lines:
        already_sold = set()
        cur = int(line)
        sequence_integer = 0

        # Initialize sequence with first four changes.
        prev = cur % 10
        for i in range(3):
            cur = (cur ^ (cur << 6)) & PRUNE_MASK  # We iteratively mix and prune it.
            cur = (cur ^ (cur >> 5)) & PRUNE_MASK
            cur = (cur ^ (cur << 11)) & PRUNE_MASK
            cur_price = (cur % 10)
            change = cur_price - prev + 10 # Change in range [0..18]
            sequence_integer = ((sequence_integer << CHANGE_WIDTH) | change) & SEQUENCE_MASK
            prev = cur_price

        for k in range(3, 2000):
            # Takes like 0.06s
            cur = (cur ^ (cur << 6)) & PRUNE_MASK  # We iteratively mix and prune it.
            cur = (cur ^ (cur >> 5)) # & PRUNE_MASK # No need to prune.
            cur = (cur ^ (cur << 11)) & PRUNE_MASK

            #cur = (cur ^ (cur << 6) ^ ((cur << 1) & SECOND_SHIFT_MASK) ^ (cur << 12)) & PRUNE_MASK

            cur_price = (cur % 10)
            change = cur_price - prev + 10  # Change in range [0..18]
            sequence_integer = ((sequence_integer << CHANGE_WIDTH) | change) & SEQUENCE_MASK
            prev = cur_price

            if sequence_integer not in already_sold:
                counts[sequence_integer] += cur_price
                already_sold.add(sequence_integer)  # Takes 0.2 seconds. Like 40% of the time.

    return max(counts.values())


# Maybe to speed up hashing, we look at each output bit as a sequence of the input bits.
# This defines some sort of a matrix with entries in integers modulo 2 (thats what XOR is)
# And we could use fast matrix exponentiation to do this
# Assuming that you can do that



if __name__ == '__main__':
    get_results("P1 Example", part1, read_lines, "example.txt", expected=37327623)
    get_results("P1", part1, read_lines, "input.txt", expected=20506453102)

    get_results("P2 Example", part2, read_lines, "example2.txt", expected=23)
    get_results("P2", part2, read_lines, "input.txt", expected=2423)