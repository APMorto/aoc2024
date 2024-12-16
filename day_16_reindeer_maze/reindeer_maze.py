import collections
import heapq
import math
from util.timer import get_results
from parser.parser import read_lines, read_line, read_grid, read_list_grid, read_line_blocks
from typing import List, Tuple
from util.util import seek_character
from util.point2d import Point2D
from util.grid2d import Grid2DDense
from util.directions import Direction2DCR

def part1(grid_list):
    grid = Grid2DDense(grid_list)
    start_pos = Point2D(*reversed(seek_character(grid_list, 'S')))
    end_pos = Point2D(*reversed(seek_character(grid_list, 'E')))
    initial_state = (start_pos, Direction2DCR.RIGHT)   # (cost, pos, dir

    heap: List[Tuple[int, int, Point2D, Direction2DCR]] = []    # heap[i] = (A* cost, real cost, pos, dir
    heapq.heappush(heap, (0 + start_pos.manhattan_distance(end_pos), 0, start_pos, Direction2DCR.RIGHT)) #

    best_seen = collections.defaultdict(lambda: math.inf)
    best_seen[initial_state] = 0

    while len(heap) > 0:
        a_cost, cost, pos, direction = heapq.heappop(heap)
        if pos == end_pos:
            return cost
        if best_seen[(pos, direction)] < cost:
            continue

        # Try moving forward
        fwd = pos + direction.point_offset()
        if grid.get(fwd) != '#' and best_seen[(fwd, direction)] > cost+1:
            best_seen[(fwd, direction)] = cost+1
            heapq.heappush(heap, (cost+1 + fwd.manhattan_distance(end_pos), cost+1, fwd, direction))

        # Try turning
        left = direction.turn_left()
        if best_seen[(pos, left)] > cost+1000:
            best_seen[(pos, left)] = cost+1000
            heapq.heappush(heap, (a_cost + 1000, cost+1000, pos, left))

        right = direction.turn_right()
        if best_seen[(pos, right)] > cost+1000:
            best_seen[(pos, right)] = cost+1000
            heapq.heappush(heap, (a_cost+1000, cost+1000, pos, right))

    return math.inf


def part2(grid_list):
    # Which tiles are part of ANY best path?
    # we could do one forward and one reverse path
    # and then any states which have sum of cost from + to being best is ok
    grid = Grid2DDense(grid_list)
    start_pos = Point2D(*reversed(seek_character(grid_list, 'S')))
    end_pos = Point2D(*reversed(seek_character(grid_list, 'E')))

    heap: List[Tuple[int, Point2D, Direction2DCR]] = []
    heapq.heappush(heap, (0, start_pos, Direction2DCR.RIGHT)) # minheap

    best_seen_forward = collections.defaultdict(lambda: math.inf)
    best_seen_forward[(start_pos, Direction2DCR.RIGHT)] = 0
    end_cost = math.inf

    while len(heap) > 0:
        cost, pos, direction = heapq.heappop(heap)
        if pos == end_pos:
            end_cost = cost
        if cost > end_cost:
            break
        if best_seen_forward[(pos, direction)] < cost:
            continue

        # Try moving forward
        fwd = pos + direction.point_offset()
        if grid.get(fwd) != '#' and best_seen_forward[(fwd, direction)] > cost+1:
            best_seen_forward[(fwd, direction)] = cost+1
            heapq.heappush(heap, (cost+1, fwd, direction))

        # Try turning
        left = direction.turn_left()
        if best_seen_forward[(pos, left)] > cost+1000:
            best_seen_forward[(pos, left)] = cost+1000
            heapq.heappush(heap, (cost+1000, pos, left))

        right = direction.turn_right()
        if best_seen_forward[(pos, right)] > cost+1000:
            best_seen_forward[(pos, right)] = cost+1000
            heapq.heappush(heap, (cost+1000, pos, right))

    best_path_cost = end_cost


    # REVERSE
    heap.clear()
    best_seen_reverse = collections.defaultdict(lambda: math.inf)
    end_cost = math.inf
    for direction in Direction2DCR:
        heapq.heappush(heap, (0, end_pos, direction))
        best_seen_reverse[(end_pos, direction)] = 0

    while len(heap) > 0:
        cost, pos, direction = heapq.heappop(heap)
        if pos == start_pos and direction == Direction2DCR.RIGHT:
            end_cost = cost
        if cost > end_cost:
            break
        if best_seen_reverse[(pos, direction)] < cost:
            continue

        # Try moving forward
        fwd = pos - direction.point_offset()
        if grid.get(fwd) != '#' and best_seen_reverse[(fwd, direction)] > cost+1:
            best_seen_reverse[(fwd, direction)] = cost+1
            heapq.heappush(heap, (cost+1, fwd, direction))

        # Try turning
        left = direction.turn_left()
        if best_seen_reverse[(pos, left)] > cost+1000:
            best_seen_reverse[(pos, left)] = cost+1000
            heapq.heappush(heap, (cost+1000, pos, left))

        right = direction.turn_right()
        if best_seen_reverse[(pos, right)] > cost+1000:
            best_seen_reverse[(pos, right)] = cost+1000
            heapq.heappush(heap, (cost+1000, pos, right))

    out = 0
    for p in grid.pos_iter():
        if grid.get(p) != '#':
            for direction in Direction2DCR:
                state = (p, direction)
                if best_seen_forward[state] + best_seen_reverse[state] == best_path_cost:
                    out += 1
                    break
    return out

if __name__ == '__main__':
    get_results("P1 Example", part1, read_grid, "example.txt", expected=7036)
    get_results("P1 Example", part1, read_grid, "example2.txt", expected=11048)
    get_results("P1", part1, read_grid, "input.txt")

    get_results("P2 Example", part2, read_grid, "example.txt", expected=45)
    get_results("P2 Example", part2, read_grid, "example2.txt", expected=64)
    get_results("P2", part2, read_grid, "input.txt")