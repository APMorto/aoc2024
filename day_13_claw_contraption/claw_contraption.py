import math
from email.base64mime import body_decode
from functools import cache
from typing import List

from parser.parser import read_line_blocks
from util.timer import get_results

PART_2_OFFSET = 10_000_000_000_000

def parse_machine_block(block: List[str]):
    # All A and B offsets are 2 digit numbers.
    a_move_str, b_move_str, prize_location_str = block
    a_offset = int(a_move_str[12:14]), int(a_move_str[18:20])
    b_offset = int(b_move_str[12:14]), int(b_move_str[18:20])

    # prize location has variable number of digits.
    # X always starts on index 9
    prize_x_str, prize_y_str = prize_location_str[9:].split(", Y=")
    prize_offset = int(prize_x_str), int(prize_y_str)
    return a_offset, b_offset, prize_offset


def parse_machine_blocks(blocks: List[List[str]]):
    return map(parse_machine_block, blocks)

def min_cost_to_get_prize(a_offset, b_offset, prize_offset):
    ax, ay = a_offset
    bx, by = b_offset

    prizex, prizey = prize_offset

    # We want to find min{3A + 1B : A*ax + B*bx == prizex and A*ay + B*by == prizey}
    # Insight: The order does not matter!
    # So we can just 'slide' across with our amounts of A and B

    B = max(math.ceil(prizex / bx), math.ceil(prizey / by))
    A = 0
    cur_x, cur_y = bx * B, by * B
    best = math.inf

    while B >= 0:
        # Increase A to make it work
        while cur_x < prizex or cur_y < prizey:
            cur_x += ax
            cur_y += ay
            A += 1
        if cur_x == prizex and cur_y == prizey:
            best = min(best, 3*A + B)
            #print(f"(normal) A: {A}, B: {B}")
            break       # Apparently there is only one solution!

        # Decrement B
        B -= 1
        cur_x -= bx
        cur_y -= by

    return best


def part1(line_blocks: List[List[str]]):

    # We are solving each of these on their own, no combination.
    out = 0
    for offsets in parse_machine_blocks(line_blocks):
        cost = min_cost_to_get_prize(*offsets)
        cost2 = min_cost_to_get_prize_part_2(*offsets)
        if (cost2 < math.inf) ^ (cost < math.inf):
            print(cost, cost2)
        #print(cost)
        out += cost if cost < math.inf else 0
    return out


def min_cost_to_get_prize_part_2(a_offset, b_offset, prize_offset):
    ax, ay = a_offset
    bx, by = b_offset
    prizex, prizey = prize_offset

    # We know that each addition does something
    # Are these cyclic?
    # Now, part 1 had only 1 solution.

    # We want to find min{3A + 1B : A*ax + B*bx == prizex and A*ay + B*by == prizey}
    # So, A*ax = prizex - B*bx
    #     A = prizex / ax - B*bx/ax
    #     A = prizey / ay - B*by/ay
    #     0 = (prizex/ax - prizey/ay) + B (by/ay - bx/ax)
    #     B = (prizex/ax - prizey/ay) / (bx/ax - by/ay)
    B = (prizex/ax - prizey/ay) / (bx/ax - by/ay)
    B = round(B)
    if B < 0:
        return math.inf

    A = round(prizex / ax - B*bx/ax)
    #print(f"A: {A}, B: {B}")
    if A*ax + B*bx == prizex and A*ay + B*by == prizey:
        return 3*A + B
    else:
        return math.inf

    # Look at X - Y
    # Our final X - Y must be correct
    # and each addition of A and B change this
    # If one is pos, and one is negative, its free
    a_delta = ax - ay
    b_delta = bx - by
    if (a_delta > 0) ^ (b_delta > 0):
        # Differing Deltas!
        # Now we have another annoying linear combination
        pass


    else:
        print("Opposite delta signs failing")
        print(a_offset, b_offset, prize_offset)
        print(a_delta, b_delta)
    return math.inf


def part2(line_blocks: List[List[str]]):
    # We are solving each of these on their own, no combination.
    out = 0
    for offsets in parse_machine_blocks(line_blocks):
        cost = min_cost_to_get_prize_part_2(offsets[0], offsets[1], (offsets[2][0] + PART_2_OFFSET, offsets[2][1] + PART_2_OFFSET))
        #print(cost)
        out += cost if cost < math.inf else 0
    return out

# Each button does not need to be pressed any more than 100 times.
# A costs 3, B costs 4

# 46316532262826 too low
# 49374249917308 too low

if __name__ == '__main__':
    get_results("P1 Example", part1, read_line_blocks, "example.txt")
    get_results("P1", part1, read_line_blocks, "input.txt")

    get_results("P2 Example", part2, read_line_blocks, "example.txt")
    get_results("P2", part2, read_line_blocks, "input.txt")