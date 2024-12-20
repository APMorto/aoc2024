import collections
import math

from fontTools.misc.plistlib import end_dict

from util.point2d import Point2D
from util.timer import get_results
from parser.parser import read_lines, read_line, read_grid, read_list_grid, read_line_blocks
from typing import List
from util.util import seek_character, seek_character_point
from util.grid2d import Grid2DDense

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
        #assert start_cost + end_distances[pos.y][pos.x] >= best_non_cheated

        for adj in pos.points_within_manhatten_distance(20):
            if maze_grid.in_bounds(adj) and start_cost + end_distances[adj.y][adj.x] + pos.manhattan_distance(adj) <= best_non_cheated - save_amount:
                num_cheats += 1
            #if maze_grid.in_bounds(adj) and start_cost + end_distances[adj.y][adj.x] + pos.manhattan_distance(adj) == best_non_cheated - 76:
            #    num_cheats += 1
    return num_cheats

# The major bottleneck in this problem reduces to the following:
# In this manhatten-radius region, how many values are <= some value?


if __name__ == '__main__':
    get_results("P1 Example", part1, read_grid, "example.txt")
    get_results("P1", part1, read_grid, "input.txt", expected=1365)

    get_results("P2 Example", part2, read_grid, "example.txt")
    get_results("P2", part2, read_grid, "input.txt", expected=986082)