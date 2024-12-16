#https://github.com/marcodelmastro/AdventOfCode2024/blob/main/Day16.ipynb

import numpy as np

WALL = 1

def read_input_16(filename):
    f = open(filename)
    lines = f.readlines()
    grid = np.zeros((len(lines), len(lines[0])-1),dtype=int)
    for r,l in enumerate(lines):
        for c,v in enumerate(l.strip()):
            if v=="#":
                grid[r][c] = WALL
            if v=="S":
                start = (r,c)
            if v=="E":
                end = (r,c)
    return grid, start, end
from queue import PriorityQueue, Queue
import math

def best_score(grid,start,end):
    dirs = [(0,+1), (+1,0), (0,-1), (-1,0)] # (Row, Column): E, S, W, N
    queue = PriorityQueue()
    queue.put( (0,start,0) ) # score, position, facing direction
    visited = set()
    while True:
        pos = queue.get()
        score, p, d = pos
        visited.add((p,d))
        for i in [0,-1,+1,+2]: # straight, left, right, backward
            dnew = (d+i)%4
            dr,dc = dirs[dnew]
            r,c = p
            r1,c1 = r+dr,c+dc
            if grid[r1][c1]==WALL:
                continue
            if ((r1,c1), dnew) in visited:
                continue
            scorenew = score+abs(i)*1000+1
            if (r1,c1)==end:
                return scorenew
            else:
                queue.put( (scorenew,(r1,c1),dnew) )

def part1_marco_del_maestro(filename):
    grid, start, end = read_input_16(filename)
    return best_score(grid,start,end)