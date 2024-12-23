from collections import defaultdict

from util.timer import get_results
from parser.parser import read_lines, read_line, read_grid, read_list_grid, read_line_blocks
from typing import List

# List of bidirectional connections between computers
# Look at sets of three connected computers
# Can there be intermediate computers? Or must it be direct? I think it must be direct.
# And at least one computer's name starts with t

def read_computer_connections(lines: List[str]):
    edges = defaultdict(list)
    for line in lines:
        a, b = line[:2], line[3:]
        edges[a].append(b)
        edges[b].append(a)
    return edges

def part1(lines: List[str]):
    edges = read_computer_connections(lines)
    n = len(edges)

    # Map each edge to an integer.
    node_indices = {node: i for i, node in enumerate(edges.keys())}

    # Get neighbor sets as integers.
    bitset_edge_sets = [0] * n
    for node, neighbors in edges.items():
        bitset = 0
        for neighbor in neighbors:
            bitset |= (1 << node_indices[neighbor])
        bitset_edge_sets[node_indices[node]] = bitset

    triplets = set()
    for node, neighbors in edges.items():
        # Every triplet must have at least 1 t?, so consider only those starting from t.
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
    #for triplet in triplets:
    #    print(bin(triplet))
    return len(triplets)



    # This isgnores whether the 3 are all connected.
    # We can start with only one t?
    # and then 2 t?, /2 (as double counted)
    # and then 3 t? /3, (as triple counted)
    single = 0
    double = 0
    triple = 0

    for node, neighbors in edges.items():
        if node[0] != 't':
            continue
        ts = 0
        non_ts = 0
        for neighbor in neighbors:
            if neighbor[0] == 't':
                ts += 1
            else:
                non_ts += 1

        single += non_ts * (non_ts-1) // 2   # non_ts Choose 2
        double += ts * non_ts
        triple += ts * (ts-1) // 2

    #print(single, double, triple)
    out = single + (double // 2) + (triple // 3)
    return out




def part2(_):
    pass


if __name__ == '__main__':
    get_results("P1 Example", part1, read_lines, "example.txt", expected=7)
    get_results("P1", part1, read_lines, "input.txt")

    get_results("P2 Example", part2, read_lines, "example.txt")
    get_results("P2", part2, read_lines, "input.txt")