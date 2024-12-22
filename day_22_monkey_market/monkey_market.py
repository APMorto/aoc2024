from collections import defaultdict

import numpy as np

from util.timer import get_results
from parser.parser import read_lines
from typing import List
from util.matrix_math import row_vector_of_integer, integer_of_row_vector, left_shift_of_matrix, \
    right_shift_of_matrix, matrix_power_linear, matrix_power_log

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
N = 24


def get_hash_matrix():
    # This matrix represents Taking a row vector of the bits, and applying this will yield the next hash state.
    cur = np.eye(N, N, dtype=np.uint8)
    left_shift_6 = left_shift_of_matrix(cur, 6)
    cur ^= left_shift_6
    right_shift_5 = right_shift_of_matrix(cur, 5)
    cur ^= right_shift_5
    left_shift_11 = left_shift_of_matrix(cur, 11)
    cur ^= left_shift_11
    return cur

def part1_matrix(lines: List[str]):
    hash_matrix = get_hash_matrix()
    #two_thousandth_hash_matrix = matrix_power_linear(hash_matrix, 2000)
    two_thousandth_hash_matrix = matrix_power_log(hash_matrix, 2000)

    out = 0
    for line in lines:
        num = int(line)
        num_row_vector = row_vector_of_integer(num, N)
        num_row_vector = num_row_vector @ two_thousandth_hash_matrix
        num_row_vector %= 2

        out += integer_of_row_vector(num_row_vector)
    return out



if __name__ == '__main__':
    get_results("P1 Example", part1, read_lines, "example.txt", expected=37327623)
    get_results("P1", part1, read_lines, "input.txt", expected=20506453102)
    get_results("P1 Matrix Example", part1_matrix, read_lines, "example.txt", expected=37327623)
    get_results("P1 Matrix", part1_matrix, read_lines, "input.txt", expected=20506453102)

    get_results("P2 Example", part2, read_lines, "example2.txt", expected=23)
    get_results("P2", part2, read_lines, "input.txt", expected=2423)