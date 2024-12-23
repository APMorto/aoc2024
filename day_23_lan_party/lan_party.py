import math
from collections import defaultdict

from util.timer import get_results
from parser.parser import read_lines, read_line, read_grid, read_list_grid, read_line_blocks
from typing import List

# This question requires us to obtain the intersection between two sets very frequently.
# Bitsets achieve this very nicely. However, getting the values out is annoying.
# n & (n-1) sets the rightmost 1 bit to a 0. So, n ^ (n & (n-1)) returns the rightmost 1 bit only.
# This lets us efficiently iterate through the set bits.

def read_computer_connections(lines: List[str]):
    edges = defaultdict(list)
    for line in lines:
        a, b = line[:2], line[3:]
        edges[a].append(b)
        edges[b].append(a)
    return edges

def get_bitset_edges(edges, node_indices):
    n = len(edges)
    # Get neighbor sets as integers.
    bitset_edge_sets = [0] * n
    for node, neighbors in edges.items():
        bitset = 0
        for neighbor in neighbors:
            bitset |= (1 << node_indices[neighbor])
        bitset_edge_sets[node_indices[node]] = bitset
    return bitset_edge_sets

# List of bidirectional connections between computers
# Look at sets of three connected computers
# Can there be intermediate computers? Or must it be direct? I think it must be direct.
# And at least one computer's name starts with t
def part1(lines: List[str]):
    edges = read_computer_connections(lines)

    # Map each edge to an integer.
    node_indices = {node: i for i, node in enumerate(edges.keys())}

    # Get neighbor sets as integers.
    bitset_edge_sets = get_bitset_edges(edges, node_indices)

    triplets = set()
    for node, neighbors in edges.items():
        # Every triplet must have at least 1 t*, so consider only those starting from t.
        if node[0] != 't':
            continue

        i1 = node_indices[node]
        neighbor_bitset = bitset_edge_sets[i1]
        for neighbor in neighbors:
            i2 = node_indices[neighbor]
            other_neighbor_bitset = bitset_edge_sets[i2]
            intersection = neighbor_bitset & other_neighbor_bitset

            # Iterate over all set bits in the intersection.
            while intersection != 0:
                next_intersection = intersection & (intersection-1) # Sets rightmost 1 bit to 0
                common = intersection ^ next_intersection
                intersection = next_intersection

                triplets.add((1 << i1) | (1 << i2) | common)
    return len(triplets)

def part2(lines: List[str]):
    edges = read_computer_connections(lines)
    n = len(edges)
    # n = 520

    # Map each edge to an integer.
    nodes_at_indices = sorted(edges.keys(), key=lambda node: len(edges[node]), reverse=True)  # Lookup for end solution.
    # Im not sure if sorting is the play. The variance is > the difference by sorting this.
    #nodes_at_indices = tuple(edges.keys())
    node_indices = {node: i for i, node in enumerate(nodes_at_indices)}
    bitset_edge_sets = get_bitset_edges(edges, node_indices)

    # Largest fully connected set of computers.
    best = 0
    best_val = 0
    def max_fully_connected_component(contained: int, candidates: int, tried: int):
        nonlocal best, best_val, bitset_edge_sets

        # No more to add. We're done.
        if candidates == 0:
            amt = contained.bit_count()
            if amt > best:
                best = amt
                best_val = contained
            return

        # Check if this is hopeless. Pretty good time save.
        if (contained | (candidates & ~tried)).bit_count() <= best:
            return

        # Consider adding each candidate. (which we have not tried)
        cur_candidates = candidates & ~tried
        while cur_candidates != 0:
            # Remove the rightmost 1 bit.
            next_candidates = cur_candidates & (cur_candidates - 1)
            candidate = cur_candidates ^ next_candidates
            cur_candidates = next_candidates

            # Dont try this again. Without this, it's too slow.
            tried |= candidate

            candidate_index = int(math.log2(candidate))
            #assert candidate == (1 << candidate_index), f"{candidate_index}, {candidate}"

            # Add candidate. Filter the remaining possible edges.
            max_fully_connected_component(contained | candidate, candidates & bitset_edge_sets[candidate_index], tried)

    all_set_bits = (1 << n) - 1
    max_fully_connected_component(0, all_set_bits, 0)

    # Reassemble the output.
    out_strings = []
    while best_val != 0:
        next_val = best_val & (best_val - 1)
        diff = best_val ^ next_val
        i = int(math.log2(diff))
        out_strings.append(nodes_at_indices[i])
        best_val = next_val
    out_strings.sort()
    return ",".join(out_strings)


if __name__ == '__main__':
    get_results("P1 Example", part1, read_lines, "example.txt", expected=7)
    get_results("P1", part1, read_lines, "input.txt", expected=1000)

    get_results("P2 Example", part2, read_lines, "example2.txt", expected="co,de,ka,ta")
    get_results("P2", part2, read_lines, "input.txt", expected="cf,ct,cv,cz,fi,lq,my,pa,sl,tt,vw,wz,yd")