import collections
import math

import numpy as np

from util.point2d import Point2D
from util.timer import get_results
from parser.parser import read_lines, read_line, read_grid, read_list_grid, read_line_blocks
from typing import List
from util.util import seek_character, seek_character_point, rotate_matrix
from util.grid2d import Grid2DDense

from sortedcontainers import SortedList

def distances_from_pos(maze_grid: Grid2DDense, start_pos: Point2D):
    h, w = maze_grid.shape
    distances  = [[math.inf] * w for _ in range(h)]
    distances[start_pos.y][start_pos.x] = 0
    q = collections.deque([(start_pos, 0)])

    while q:
        pos, d = q.popleft()
        assert distances[pos.y][pos.x] == d
        for adj in pos.get_adjacent_ortho():
            if distances[adj.y][adj.x] >= math.inf and maze_grid.get(adj) != '#':
                distances[adj.y][adj.x] = d+1
                q.append((adj, d + 1))
    return distances



def part1(list_grid: List[str]):
    start_pos = seek_character_point(list_grid, 'S')
    end_pos =   seek_character_point(list_grid, 'E')

    maze_grid = Grid2DDense(list_grid)

    # Standard , 1 move = 1 ps
    # But, once during the race, you may disable collision for (up to) 2 ps
    # Cheats have a distinct start and end position.
    # How many cheats would save at least 100 picoseconds?

    # We will first use BFS / Dijkstras to get the distance of each (unobstructed) tile to the end.
    # And also distance of each (unobstructed) tile from the start.
    # From this, we easily obtain the best uncheated time.
    start_distances = distances_from_pos(maze_grid, start_pos)
    end_distances = distances_from_pos(maze_grid, end_pos)

    best_non_cheated = start_distances[end_pos.y][end_pos.x]
    #print("Best non cheated:", best_non_cheated)
    assert end_distances[start_pos.y][start_pos.x] == best_non_cheated

    num_cheats = 0
    save_amount = 100
    for pos in maze_grid.row_major_points():
        if maze_grid.get(pos) == '#':
            continue
        start_cost = start_distances[pos.y][pos.x]
        #assert start_cost + end_distances[pos.y][pos.x] >= best_non_cheated

        for adj in pos.adjacent_within_2_manhatten_distance():
            if maze_grid.in_bounds(adj) and start_cost + end_distances[adj.y][adj.x] + pos.manhattan_distance(adj) <= best_non_cheated - save_amount:
                num_cheats += 1
            #if maze_grid.in_bounds(adj) and start_cost + end_distances[adj.y][adj.x] + pos.manhattan_distance(adj) == best_non_cheated - 64:
            #    num_cheats += 1
    return num_cheats

def part2(list_grid: List[str]):
    start_pos = seek_character_point(list_grid, 'S')
    end_pos =   seek_character_point(list_grid, 'E')
    maze_grid = Grid2DDense(list_grid)

    start_distances = distances_from_pos(maze_grid, start_pos)
    end_distances = distances_from_pos(maze_grid, end_pos)

    best_non_cheated = start_distances[end_pos.y][end_pos.x]
    #print("Best non cheated:", best_non_cheated)
    assert end_distances[start_pos.y][start_pos.x] == best_non_cheated

    num_cheats = 0
    save_amount = 100
    for pos in maze_grid.row_major_points():
        if maze_grid.get(pos) == '#':
            continue
        start_cost = start_distances[pos.y][pos.x]

        # Hopeless to even try to cheat here.
        if start_cost > best_non_cheated - save_amount:
            continue
        #assert start_cost + end_distances[pos.y][pos.x] >= best_non_cheated

        # You may choose to only look in this manhatten radius.
        #distance_possible_to_cheat = min(20, best_non_cheated - start_cost - save_amount)
        for adj in pos.points_within_manhatten_distance(20):
            if maze_grid.in_bounds(adj) and start_cost + end_distances[adj.y][adj.x] + pos.manhattan_distance(adj) <= best_non_cheated - save_amount:
                num_cheats += 1
            #if maze_grid.in_bounds(adj) and start_cost + end_distances[adj.y][adj.x] + pos.manhattan_distance(adj) == best_non_cheated - 76:
            #    num_cheats += 1
    return num_cheats

def part2_inline(list_grid: List[str]):
    start_pos = seek_character_point(list_grid, 'S')
    end_pos = seek_character_point(list_grid, 'E')
    maze_grid = Grid2DDense(list_grid)
    start_distances = distances_from_pos(maze_grid, start_pos)
    end_distances = distances_from_pos(maze_grid, end_pos)
    best_non_cheated = start_distances[end_pos.y][end_pos.x]
    assert end_distances[start_pos.y][start_pos.x] == best_non_cheated
    h, w = len(list_grid), len(list_grid[0])

    num_cheats = 0
    save_amount = 100
    for r, c in maze_grid.row_major_indexes():
        if list_grid[r][c] == '#': continue
        start_cost = start_distances[r][c]
        if start_cost > best_non_cheated - save_amount: continue    # Hopeless to even try to cheat here.

        d = 20
        for rr in range(max(0, r-20), min(h, r+20+1)):
            abs_d_y = abs(r - rr)
            width_available = abs(d - abs_d_y)
            for cc in range(max(0, c-width_available), min(w, c+width_available+1)):
                if start_cost + end_distances[rr][cc] + abs_d_y + abs(c - cc) <= best_non_cheated - save_amount:
                    num_cheats += 1
    return num_cheats


def part2_sliding_window(list_grid: List[str]):
    start_pos = seek_character_point(list_grid, 'S')
    end_pos = seek_character_point(list_grid, 'E')
    maze_grid = Grid2DDense(list_grid)

    start_distances = distances_from_pos(maze_grid, start_pos)
    end_distances = distances_from_pos(maze_grid, end_pos)

    best_non_cheated = start_distances[end_pos.y][end_pos.x]
    assert end_distances[start_pos.y][start_pos.x] == best_non_cheated

    out = 0
    out += sliding_window(start_distances, end_distances, best_non_cheated)
    for _ in range(3):
        start_distances = rotate_matrix(start_distances)
        end_distances = rotate_matrix(end_distances)
        out += sliding_window(start_distances, end_distances, best_non_cheated)

    return out


def sliding_window(to_costs: List[List], from_costs: List[list], best_distance: int):
    h, w = len(from_costs), len(from_costs[0])
    assert len(to_costs) == h and len(to_costs[0]) == w

    out = 0
    SAVE_AMT = 100
    DIST = 20

    # We say the value of to_costs[r][c] = to_costs[r][c] - r + c

    # For each row, perform the sliding window, using this rows values as sources.
    for main_row in range(h):
        frontier = SortedList() # May contain duplicate values.

        # Add in the initial values.
        for init_row in range(max(main_row - DIST, 0), main_row+1):
            width_available = DIST - abs(main_row - init_row)
            for init_col in range(0, width_available):              # Note we actually stop 1 before the allotted width.
                if (val := to_costs[init_row][init_col]) < math.inf:
                    frontier.add(val - init_row + init_col)
                #assert abs(init_row - main_row) + abs(0 - init_col) < DIST

        for c in range(w):

            # Discard values which are vertically inline with c
            for discard_row in range(max(main_row - DIST+1, 0), main_row+1):    # We dont remove the top value because it was never added. (1-wide)
                if (val := to_costs[discard_row][c]) < math.inf:
                    frontier.remove(val - discard_row + c)

            # Add in values on the right edge of the frontier.
            for add_row in range(max(main_row - DIST+1, 0), main_row+1):    # Dont add the top because we dont need to.
                width_available = DIST - main_row + add_row                 # add_row <= main_row, so no abs needed.
                add_col = c + width_available
                if add_col >= w:
                    break

                #assert abs(add_row - main_row) + abs(c - add_col) <= DIST
                if (val := to_costs[add_row][add_col]) < math.inf:
                    frontier.add(val - add_row + add_col)

            start_dist = from_costs[main_row][c]
            if start_dist < math.inf:
                # Frontier now contains all possible locations that we could reach.
                start_manhatten_potential = c - main_row

                # start_dist + to_dist + (manhatten_dist) <= best_distance - SAVE_AMT
                # to_dist <= best_distance - SAVE_AMT - start_dist - manhatten_dist
                # to_dist <= best_distance - SAVE_AMT - start_dist - (dest_manhatten_potential - start_manhatten_potential)
                # to_dist + dest_manhatten_potential <= best_distance - SAVE_AMT - start_dist + start_manhatten_potential
                cutoff = best_distance - SAVE_AMT - start_dist + start_manhatten_potential
                insertion_point = frontier.bisect_right(cutoff)
                out += insertion_point

        #assert len(frontier) == 0, frontier

    return out




# The major bottleneck in this problem reduces to the following:
# In this manhatten-radius region, how many values are <= some value?
# We can almost do an integral histogram type approach to count values in the region
# and then just only have sufficiently low cost to end paths in that thing
# But then we also have to consider the manhatten distance to that point
# So its not clear how you would do this
# One possible approach is to just use a spatial grid where we store the costs and positions of each end path in a sorted list
# Then we just check all path costs <= some threshold for completeness, of course filtering for cheat path cost and manhatten distance

# The crux of this problem is reducing the amount of possible cheats that we check.

# Promising.
# https://www.reddit.com/r/adventofcode/comments/1hicdtb/comment/m2y6zvg/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
# https://github.com/bharadwaj-raju/aoc-2024/blob/main/day20/2.py

# It seems that there exists 1 and only 1 optimal path
#

#l = SortedList()
#l.add(2)
#l.add(2)
#l.remove(2)
#print(l)


# Consider the four quadrants of our neighbors
# We will solve for just one of those quadrants in a sliding window approach.
# Consider that we can add in the cost of the vertical and horizontal distance of the points as we add them to the window
# and like, we just ALWAYS DECREMENT THE DISTANCE BY 1 as we slide them left (we move right)
# Then Supposing that we just have the set of valid, its a length check, which is trivial.
# We can remove values when they become directly overhead
# and add numbers on the right
# Then if we maintain the numbers in a sorted container
# We just query the values in the container <= some value

# Crucially, we only move up and to the right
# So manhatten distance is just he sum of row + column
# and we just offset it by the source row + col

# Can we use an integral histogram-esque approach?
# Given how our target value keeps changing, not very well.


if __name__ == '__main__':
    get_results("P1 Example", part1, read_grid, "example.txt")
    get_results("P1", part1, read_grid, "input.txt", expected=1365)

    get_results("P2 Example", part2, read_grid, "example.txt")
    get_results("P2 Inline", part2_inline, read_grid, "input.txt", expected=986082)
    get_results("P2 Sliding Window", part2_sliding_window, read_grid, "input.txt", expected=986082)
    get_results("P2", part2, read_grid, "input.txt", expected=986082)
