import math
from functools import cache
from typing import List

from parser.parser import read_line_blocks
from util.timer import get_results

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

        # Decrement B
        B -= 1
        cur_x -= bx
        cur_y -= by

    return best

    #seen = {}
    #def min_cost_helper(x, y, a_presses, b_presses):
    #    if (x, y) in seen:
    #        return seen[(x, y)]
    #    if x == prizex and y == prizey:
    #        return 0
    #    elif x > prizex or y > prizey or a_presses > 100 or b_presses > 100:
    #        return math.inf
    #    else:
    #        return min(
    #            min_cost_helper(x + ax, y + ax, a_presses+1, b_presses) + 3,
    #            min_cost_helper(x + ay, y + ay, a_presses, b_presses+1) + 1,
    #        )
    #return min_cost_helper(0, 0, 0, 0)


def parse_machine_blocks(blocks: List[List[str]]):
    return map(parse_machine_block, blocks)


def part1(line_blocks: List[List[str]]):

    # We are solving each of these on their own, no combination.
    out = 0
    for offsets in parse_machine_blocks(line_blocks):
        cost = min_cost_to_get_prize(*offsets)
        #print(cost)
        out += cost if cost < math.inf else 0
    return out


def part2(line_blocks: List[List[str]]):
    pass

# Each button does not need to be pressed any more than 100 times.
# A costs 3, B costs 4

if __name__ == '__main__':
    get_results("P1 Example", part1, read_line_blocks, "example.txt")
    get_results("P1", part1, read_line_blocks, "input.txt")

    get_results("P2 Example", part2, read_line_blocks, "example.txt")
    get_results("P2", part2, read_line_blocks, "input.txt")