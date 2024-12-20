import collections

from util.timer import get_results
from parser.parser import read_lines, read_line, read_grid, read_list_grid, read_line_blocks
from typing import List
from util.datastructures import DisJointSets

import numpy as np


def part1(lines: List[str]):
    # lines[0] = size (0 - that)
    # Once something is corrupted, you cant go there.
    l = int(lines[0]) + 1
    #arr = np.zeros((l, l), dtype=bool)
    #arr[0, 0] = True

    available = np.ones((l, l), dtype=bool)
    for i in range(1, min(len(lines), 1024+1)):
        r, c = map(int, lines[i].split(','))
        available[r, c] = False

    # bfs
    q = collections.deque()
    q.append((0, 0, 0))
    seen = {(0, 0)}
    while q:
        cost, r, c = q.popleft()
        #print(cost, r, c)
        for rr, cc in ((r-1, c), (r+1, c), (r, c-1), (r, c+1)):
            if 0 <= rr < l and 0 <= cc < l and available[rr, cc] and (rr, cc) not in seen:
                if rr == l-1 and cc == l-1:
                    return cost+1
                q.append((cost+1, rr, cc))
                seen.add((rr, cc))

    return -1





def part2(lines: List[str]):
    l = int(lines[0]) + 1
    available = np.ones((l, l), dtype=bool)
    for i in range(1, len(lines)):
        r, c = map(int, lines[i].split(','))
        available[r, c] = False

    # From Back forwards, reconnect stuff.
    dsu = DisJointSets(l*l)

    # Initial connection.
    for r in range(l):
        for c in range(l):
            if available[r, c]:
                for rr, cc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                    if 0 <= rr < l and 0 <= cc < l and available[rr, cc]:
                        dsu.join(r*l+c, rr*l+cc)



    for i in range(len(lines)-1, 0, -1):
        r, c = map(int, lines[i].split(','))
        available[r, c] = True
        for rr, cc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
            if 0 <= rr < l and 0 <= cc < l and available[rr, cc]:
                dsu.join(r * l + c, rr * l + cc)
        if dsu.connected(0, l*l-1):
            return f"{r},{c}"
    return "No Solution Found."


if __name__ == '__main__':
    get_results("P1 Example", part1, read_lines, "example.txt", expected=22)
    get_results("P1", part1, read_lines, "input.txt")

    get_results("P2 Example", part2, read_lines, "example.txt", expected="6,1")
    get_results("P2", part2, read_lines, "input.txt")