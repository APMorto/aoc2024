from collections import defaultdict
from typing import Iterable, Tuple, List, Dict, Collection

from parser.parser import read_line_blocks, read_line
from util.timer import get_results


def read_rules(rule_strings: List[str]) -> Iterable[Tuple[int, int]]:
    for l in rule_strings:
        a, b = l.split("|")
        yield int(a), int(b)

def read_orderings(list_strings):
    for l in list_strings:
        yield tuple(map(int, l.split(",")))

def is_valid_p1(ordering, successors: Dict[int, Collection[int]]):
    seen = set()
    for b in ordering:
        for a in successors[b]:
            if a in seen:
                return False
        seen.add(b)

    return True

def order_numbers(ordering, successors: Dict[int, Collection[int]]):
    # suppose a|b
    # and we have ..., b, ..., a, ...
    # -> ..., a, b, ...
    # and try again

    # First, we assume that ordering this is actually possible
    # That is, for each ai, we can put it somewhere.
    # that it either precedes some element, or some element is preceded by it

    # We also assume that is ordering is UNAMBIGUOUS! (AT least in the middle element)
    # That only 1 ordering is correct

    # Does this imply there exists an edge connectin all adjacent elements?

    # Anyways, the first element is not preceded, and the last element is not succeeded (in our subset)
    # So we place this element
    # and again, the new element is not preceded

    # It happens there are no duplicate elements

    # I understood it wrong
    # b must occur after a
    # thus a must occur before b?

    order_set = set(ordering)
    precede_counts = {a: 0 for a in ordering}

    # what the fuck is 75 preceded by
    # 97
    # 97

    # Count amount that precede it
    for a in ordering:
        for b in successors[a]:
            if b in order_set:
                precede_counts[b] += 1

    # Repeatedly get the zero element
    out = []
    chosen = None
    for val, count in precede_counts.items():
        if count == 0:
            chosen = val
            break
    for i in range(len(ordering)):
        for val, count in precede_counts.items():
            if count == 0:
                chosen = val

        del precede_counts[chosen]

        out.append(chosen)
        for b in successors[chosen]:
            if b in order_set:
                precede_counts[b] -= 1

    return out


def part1(line_blocks):
    rule_strings, list_strings = line_blocks

    # So, Something is only incorrect if a precedes b, and there is rule b|a
    successors = defaultdict(set)
    for a, b in read_rules(rule_strings):
        successors[a].add(b)

    out = 0

    for order in read_orderings(list_strings):
        if is_valid_p1(order, successors):
            out += order[len(order)//2]

    return out

def part2(line_blocks):
    rule_strings, list_strings = line_blocks

    # So, Something is only incorrect if a precedes b, and there is rule b|a
    successors = defaultdict(set)
    for a, b in read_rules(rule_strings):
        successors[a].add(b)

    out = 0

    for order in read_orderings(list_strings):
        #if (len(order) != len(set(order))):
        #    print("abdfabljf")
        if not is_valid_p1(order, successors):
            out += order_numbers(order, successors)[len(order)//2]

    return out

def midpoint_of_numbers(ordering, successors: Dict[int, Collection[int]]):
    n = len(ordering)
    mid_point = n // 2
    order_set = set(ordering)
    precede_counts = {a: 0 for a in ordering}

    # Count amount that precede it
    for a in ordering:
        for b in successors[a]:
            if b in order_set:
                precede_counts[b] += 1

    # Repeatedly get the zero element
    chosen = None
    for val, count in precede_counts.items():
        if count == 0:
            chosen = val
            break
    for i in range(len(ordering)):
        if i == mid_point:
            return chosen

        #del precede_counts[chosen]
        for b in successors[chosen]:
            if b in order_set:
                precede_counts[b] -= 1

                # Avoid searching the entire set when we can easily find it.
                if precede_counts[b] == 0:
                    chosen = b

def both_parts_faster(line_blocks: List[List[str]]):
    rule_strings, list_strings = line_blocks

    # So, Something is only incorrect if a precedes b, and there is rule b|a
    successors = defaultdict(set)
    for a, b in read_rules(rule_strings):
        successors[a].add(b)

    out1 = 0
    out2 = 0
    for order in read_orderings(list_strings):
        if is_valid_p1(order, successors):
            out1 += order[len(order) // 2]
        else:
            out2 += midpoint_of_numbers(order, successors)

    return out1, out2

if __name__ == '__main__':
    get_results("P1 Example", part1, read_line_blocks, "example.txt")
    get_results("P1", part1, read_line_blocks, "input.txt")

    get_results("P2 Example", part2, read_line_blocks, "example.txt")
    get_results("P2", part2, read_line_blocks, "input.txt")

    get_results("Both parts Faster", both_parts_faster, read_line_blocks, "input.txt", expected=(6034, 6305))
