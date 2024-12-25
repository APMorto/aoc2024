import math
from array import array
from collections import defaultdict

import numpy as np

from util.timer import get_results
from parser.parser import read_lines
from typing import List
from util.matrix_math import row_vector_of_integer, integer_of_row_vector, left_shift_of_matrix, \
    right_shift_of_matrix, matrix_power_linear, matrix_power_log

# The process of cycling the secret number / hashing represents a linear operation, and thus can be represented as a matrix.
#   (Where entries are binary / integers modulo 2)
#   (XOR is equivalent to addition in integers modulo 2)
# Thus the two-thousandth number is given by INITIAL * M^2000, where M is our secret number cycling matrix.
# I have precomputed M^2000, and have implemented 'fast' bitwise operations to apply the matrix.

def part1_binary_matrix_operations(lines: List[str]):
    out = 0
    for line in lines:
        num = int(line)
        out += raise_to_2k_power(num)
    return out

# This is just [ROW VECTOR] * [MATRIX], but entries are in integers modulo 2, and we've fixed the matrix.
def raise_to_2k_power(num):
    out = 0
    for i, col_val in enumerate(COLUMN_VALUES):
        bin_val = num & col_val         # dot product.
        bin_val ^= bin_val >> 16        # Sum of values % 2
        bin_val ^= bin_val >> 8         # Repeated addition mod 2 in accumulators of the least significant bit portions.
        bin_val ^= bin_val >> 4         # Eg 0b1010|1001 -> 0bXXXX0011, where | denotes the separation,
        bin_val ^= bin_val >> 2         # and 0, 0, 1, 1 in the result are all accumulators representing 1+1, 0+0, 0+1, 1+0, all % 2
        bin_val ^= bin_val >> 1         # Values to the left of our accumulator are junk.
        out += (bin_val & 1) << i       # Place this result in the ith row (bit)
    return out

# Old part 1.
def part1(lines: List[str]):
    out = 0
    for line in lines:
        num = int(line)
        two_thousands_secret = kth_secret_number(num, 2000)
        #print(num, two_thousands_secret)
        out += two_thousands_secret
    return out

#cur = (cur ^ (cur << 6) ^ (cur >> 5) ^ (cur << 11)) & PRUNE_MASK  # is WRONG! Because we need to update cur between uses.
def kth_secret_number(initial_secret_number: int, k: int) -> int:
    PRUNE_MASK = (1 << 24) - 1  # 0b[1]^24
    cur = initial_secret_number
    for _ in range(k):
        cur = (cur ^ (cur << 6)) & PRUNE_MASK   # We iteratively mix and prune it.
        cur = (cur ^ (cur >> 5)) & PRUNE_MASK
        cur = (cur ^ (cur << 11)) & PRUNE_MASK
    return cur

# Inspiration from https://old.reddit.com/r/adventofcode/comments/1hjroap/2024_day_22_solutions/m3915dk/
# https://github.com/mkern75/AdventOfCodePython/blob/main/year2024/Day22.py
# It was fast and used arrays.
def part2_array(lines: List[str]):
    PRUNE_MASK = (1 << 24) - 1  # 0b[1]^24
    SEQUENCE_MOD = 19 ** 4  # I don't know why everybody uses 20 instead of 19.

    # TIL about array.array in python. Faster than lists!
    counts = array('H', [0] * SEQUENCE_MOD) # 'H' = unsigned short.
    # Now, allocating big arrays is slow! And resetting them also seems cumbersome, so I just remember the last one.
    # Functions identically to a boolean array that we just reset a bunch
    last_sold = array('H', [0] * SEQUENCE_MOD)
    for line_number, line in enumerate(lines, start=1): # Must start at 0, otherwise first line is completely ignored.
        cur = int(line)
        sequence_integer = 0

        # Initialize sequence with first four changes.
        prev = cur % 10
        for i in range(3):
            cur = (cur ^ (cur << 6)) & PRUNE_MASK  # We iteratively mix and prune it.
            cur = (cur ^ (cur >> 5)) # & PRUNE_MASK
            cur = (cur ^ (cur << 11)) & PRUNE_MASK
            cur_price = (cur % 10)
            change = cur_price - prev + 10 # Change in range [0..18]
            sequence_integer = (sequence_integer * 19 + change) % SEQUENCE_MOD
            prev = cur_price

        for k in range(3, 2000):
            # Takes like 0.06s
            cur = (cur ^ (cur << 6)) & PRUNE_MASK  # We iteratively mix and prune it.
            cur = (cur ^ (cur >> 5)) # & PRUNE_MASK # No need to prune.
            cur = (cur ^ (cur << 11)) & PRUNE_MASK

            cur_price = (cur % 10)
            change = cur_price - prev + 10  # Change in range [0..18]
            sequence_integer = (sequence_integer * 19 + change) % SEQUENCE_MOD
            prev = cur_price

            if last_sold[sequence_integer] < line_number:
                counts[sequence_integer] += cur_price
                last_sold[sequence_integer] = line_number

    return max(counts)


# Nothing special for part 2, as we actually need to see the intermediate values.
def part2(lines: List[str]):
    PRUNE_MASK = (1 << 24) - 1  # 0b[1]^24
    CHANGE_WIDTH = 5
    SEQUENCE_MASK = (1 << (CHANGE_WIDTH * 4)) - 1
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


def get_hash_matrix():
    # This matrix represents Taking a row vector of the bits, and applying this will yield the next hash state.
    cur = np.eye(24, 24, dtype=np.uint8)
    left_shift_6 = left_shift_of_matrix(cur, 6)
    cur ^= left_shift_6
    right_shift_5 = right_shift_of_matrix(cur, 5)
    cur ^= right_shift_5
    left_shift_11 = left_shift_of_matrix(cur, 11)
    cur ^= left_shift_11
    return cur

def part1_matrix(lines: List[str]):
    #hash_matrix = get_hash_matrix()
    #two_thousandth_hash_matrix = matrix_power_linear(hash_matrix, 2000)
    #two_thousandth_hash_matrix = matrix_power_log(hash_matrix, 2000)
    two_thousandth_hash_matrix = TWO_THOUSANDTH_EXPONENTIATED_MATRIX
    shifted_base = (1 << np.arange(24))

    out = 0
    for line in lines:
        num = int(line)
        #num_row_vector = row_vector_of_integer(num, N)

        # https://stackoverflow.com/questions/37580272/numpy-boolean-array-representation-of-an-integer
        #num_row_vector = (num & (1 << np.arange(24))) > 0  # SLOWER!!
        num_row_vector = num & shifted_base > 0
        #print(num_row_vector.dtype)

        #print(num_row_vector)
        num_row_vector = num_row_vector @ two_thousandth_hash_matrix
        num_row_vector &= 1

        #out += integer_of_row_vector(num_row_vector)
        out += np.sum(num_row_vector * shifted_base)    # Faster.
    return out


TWO_THOUSANDTH_EXPONENTIATED_MATRIX = np.array([
 [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1],
 [1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0],
 [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0],
 [1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0],
 [0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0],
 [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0],
 [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1],
 [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1],
 [1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1],
 [1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1],
 [1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1],
 [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0],
 [0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
 [1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1],
 [1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0],
 [1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0],
 [0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1],
 [0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0],
 [0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
 [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1],
 [1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0],
 [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1],
 [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0],
 [1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0]], dtype=np.uint)

# values of the columns, going up vertically.
COLUMN_VALUES = [11593647, 115592, 9650831, 11935952, 464073, 1874787, 8943425, 6826032, 5526809, 5714711, 9844545, 10663580, 9219426, 7597282, 491792, 9818029, 7423510, 8679750, 6442813, 10841274, 900302, 10889424, 14239094, 2959297]





if __name__ == '__main__':
    get_results("P1 Example", part1, read_lines, "example.txt", expected=37327623)
    get_results("P1", part1, read_lines, "input.txt", expected=20506453102)
    get_results("P1 Matrix Example", part1_matrix, read_lines, "example.txt", expected=37327623)
    get_results("P1 Matrix", part1_matrix, read_lines, "input.txt", expected=20506453102)
    get_results("P1 Binary Matrix", part1_binary_matrix_operations, read_lines, "input.txt", expected=20506453102)

    get_results("P2 Example", part2, read_lines, "example2.txt", expected=23)
    get_results("P2", part2, read_lines, "input.txt", expected=2423)
    get_results("P2 Array", part2_array, read_lines, "input.txt", expected=2423)