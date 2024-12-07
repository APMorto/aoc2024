import timeit
from itertools import chain
from typing import List, Optional

from parser.parser import read_grid, read_list_grid
from util.directions import Direction2D, offset_2D

TOT_CHECK_STEPS = 0
TOT_REC_CHECKS = 0
MAX_TURNS = 0
CUR_TURNS = 0


def day1(fp):
    grid = read_list_grid(fp)
    h = len(grid)
    w = len(grid[0])

    # Find initial position.
    r = -1
    c = -1
    for i in range(h):
        for j in range(w):
            if grid[i][j] == '^':
                r = i
                c = j
                break

    # Guard eventually leaves.
    # thus no need for complicated cycle detection
    direction = Direction2D.UP
    while True:
        grid[r][c] = '*'    # Mark cur pos as visited.
        ro, co = direction.offset()

        # Left.
        if not (0 <= r + ro < h and 0 <= c + co < w):
            break

        if grid[r + ro][c + co] == '#':
            direction = direction.turn_right()

        else:
            r += ro
            c += co

    # Just count how many places we went to
    return sum(ch == '*' for ch in chain(*grid))

def day2(fp):
    global CUR_TURNS
    grid = read_list_grid(fp)
    h = len(grid)
    w = len(grid[0])

    # Find initial position.
    r = -1
    c = -1
    for i in range(h):
        for j in range(w):
            if grid[i][j] == '^':
                r = i
                c = j
                break

    direction = Direction2D.UP
    visited = set()

    # Now, how many places can we put that result in a cycle?
    # Cycles are not necessarily rectangular
    # Could Simulate all and just check for cycle?
    # Furthermore, it only really matters to place it in the positions where the guard would already walk!
    # And, we can do this while walking!
    # For each step, if we would NOT hit the rock, try doing it anyways
    out = 0

    while True:
        visited.add((r, c, direction))

        ro, co = direction.offset()

        if not (0 <= r + ro < h and 0 <= c + co < w):
            break

        if grid[r + ro][c + co] == '#':
            CUR_TURNS += 1
            direction = direction.turn_right()
        else:
            if grid[r+ro][c+co] != '^' and not any((r+ro, c+co, d2) in visited for d2 in Direction2D): # Cant place on start, or where we have already been.

                grid[r+ro][c+co] = '#'

                # Traverse.
                if check_cycle(r, c, direction.turn_right(), visited, grid):
                    out += 1

                grid[r+ro][c+co] = '^'  # Even if not cycle, we cant check it later, as we would just have hit it earlier.

            # Now go forwards
            r += ro
            c += co

    return out

def check_cycle(r, c, direction, visited, grid):
    local_visited = set()
    h, w = len(grid), len(grid[0])

    global TOT_CHECK_STEPS, TOT_REC_CHECKS, MAX_TURNS, CUR_TURNS
    TOT_REC_CHECKS += 1
    cur_turns = CUR_TURNS

    while True:
        TOT_CHECK_STEPS += 1
        #print(local_visited)
        if (r, c, direction) in visited or (r, c, direction) in local_visited:
            MAX_TURNS = max(MAX_TURNS, cur_turns)
            return True

        local_visited.add((r, c, direction))

        grid[r][c] = '*'  # Mark cur pos as visited.
        ro, co = direction.offset()

        # Left the grid
        if not (0 <= r + ro < h and 0 <= c + co < w):
            MAX_TURNS = max(MAX_TURNS, cur_turns)
            return False

        if grid[r + ro][c + co] == '#':
            direction = direction.turn_right()
            cur_turns += 1

        else:
            r += ro
            c += co



# There exists another optimization wherein:
# After turning, you move in a straight direction, so you will go the same place
# Unless the new thing is there
# In which case, you can just update by checking if its in the ray propagating
# and thats it
# You could then do some fancy graph stuff
# (its all a graph, and always has been)

# Consider: We always turn right
# Thus, if we turn four times, we end up in the same direction
# and there exists a bounding box where we we existed within that path
# And the next four turns are also a bounding box
# Which we can combine
# and then 4
# ... etc
# => Binary lifting (two 'adjacent' graph bounding boxes are combined by taking the maximum)
# So, we find the largest distance where the bounding box does not intersect with the new stone
# Given the bounding boxes are non-decreasing, we can apply binary search

# What is more discriminating than a bounding box is something is 100% accurate
# So, we could have like sets of intervals here


# The placed stone intersects at most four edges in the graph of turn -> turn
# (the tile is traversed in at most 4 directions)

# Consider placing a stone and then turning
# If we dont interact with the stone:
# Its all just downstream, unchanged


# So we have some graph
# The 'canonical' / original path all leads to terminal states
# But there would still exist some cyclic nodes

# Suppose we number our canonical path edges
# in ascending order from the origin
#

# can it EVER happen that after first hit of new obstacle, our next (if any) hit of the obstacle is from the same direction?
# Yes.
# You may think it would need to be cyclic,
# but after the first direction we diverge.

# our terminal states are: OOB, and {pre existing cycles}, and {newly created cycles}

# We have some path we follow
# And we want to know if some coordinate lies on this path.

# This can be done weakly via bounding boxes (or other shapes)
# Strongly, quick to lookup, but expensive (money & time) to construct sets of positions
# Logarithmically in lookup, pretty bad in space&time with row/col indexed intervals (still prob faster than map)

# To Summarize, we have the pre-existing graph
# From some state, knowing whether it will be terminal or not (whether we go to OOB or existing cycle)
# Let The edges be turn -> turn
# Binary lifting can be performed on this.

# By adding a stone, we are changing at most 4 edges.
# And we wish to know whether we are terminal or not

# Let us name the flavours of terminal
# So, originally each edge is part of 1 and only 1 terminal (if any)
# Furthermore, we give them a 'dist' number, of how far they are from terminal
# (for now we assume we are not dealing with cycles)
# So now were on some edge
# and we know which edges were changed (their terminal flavor and dist)
# So clearly, our path is only effected if the modified paths include a same flavoured terminal with a lower dist! ********

# What of cycles?
# A cycle (a position which leads back to itself) is terminal.
# And a position is coterminal / cocyclic at dist 0 with another position if:
#   Both points are cycle members, and:
#   One point leads to another (order irrelevent)
# All coterminal / cocyclic points that are in the cycle are 'identical' in the that they:
#   1. Share a flavour (obviously)
#   2. Are of distance 0

# A state is cylic iff:
#   it leads to iself

# Two states are cocyclic iff:
#   they are both cyclic, and one point leads to the other

# A superflavour is:
#   The set of flavours of cocyclic states

# However, individual states in the cycle are given unique flavours.
# This is because two feeder paths may be unique, so it should be harmful for them to share a flavour.

# We will say that two flavours are coflavoured iff:
#   Their dist 0 point of their flavours are cocyclic
#   (They both end up at the same cycle)
#   Or, they are of the same flavour.

# A state is downstream of another if:
#   they are the same flavor, and it is of lower dist
#   or, the state is cyclic, and coflavoured with it

# So, given that we have hit the new obstacle (in a valid manner)
# We find ourself in a new state, and:
# Four edges are modified
# These edges have known flavours and distances.

# Lets say the modified edge/state is state pointing at the new obstacle

# Case A:
# No modified edges are downstream
# Return the original terminality (OOB if OOB, or cyclic if cyclic)

# Case B:
# a modified edge is downstream (and not cyclic)
# Choose the downstream edge with the largest dist, and then start again from there

# Case C:
# a modified edge/state is downstream (and is cyclic)
# Can there be multiple downstream, cyclic modified edges?
# Yes
# If so, just handle it by traversal, IDGAF
# So, suppose single cyclic downstream
# Given this is not our entry to the cycle,
# we just take the edge going into it and repeat

# Now, we can cycle in these recursive state changes
# But just like, remember with modified edges we have been hitting?
# and cycle detect in that manner

# So, some issues on the flavours
# multiple states can be upstream, which themselves dont share a path

# Lets imagine like an inverted forest
# Each terminal state is a root
# Then each state leads to where it leads
# and has a distance from cycle/termination
# And we can do binary lifting here? maybe?
# At any rate, we can store the root.

# To check if A -> B (B is downstream of A)
# we move along the higher dist point until is of the dist of lower
# then check for equality
# We can apply conservative binary lifting (Dont skip over potentially equal modified edges)

# We could compress unbranching nodes together to reduce distance travelled.

# So, we have a map from
# State -> Tree Node {dist, child, rootID}


# So, cool thing:
# I think a state can have at most two parents
#   1. That by moving backwards
#   2. That by having turned right
# So, if an obstacle is to our right, thats a branching point
# and that is the only branching point
# and of course we stop if we run into a boulder, because you cant exit from a boulder
# So, this is a binary tree!

# Consider the humble arrayed binary heap
# It too is a binary tree!
# Its pretty fast to check if something is a child, no?
# This method may yield too large of numbers though
# Anyways, a parent is given by //2, or >>1
# So the nth parent is >>n

# In this sense, the index is seen as a sort of set of binary L/R decisions
# We end up encountering at most 145 turns
# So like, almost able to be fit into a 128 bit number (16 bytes oof)
# but this is python so who really cares
# we can do 192 turns in like a 24 byte number

# 12 of these comparisons must be carried out, worst case.
# (4*3)//2*2 == 4*3 = 12 (all pairs)
#

# So, TreeNode(dist, child, rootID, indexID)
# def downstream(A, B):
#   # Is A -> B (B downstream of A)
#   if A.rootID != B.rootID:
#       return B.dist = 0 and A.rootID is coflavoured with B.rootID
#
#   diff = A.dist - B.dist
#   if diff < 0:
#       return False
#   return A.indexID >> diff == B.indexID   # Check the diff-th child for equality.

class StateNode:
    def __init__(self, dist: int, child, rootID: int, indexID: int):
        self.dist: int = dist
        self.child: Optional[StateNode] = child
        self.rootID: int = rootID
        self.indexID: int = indexID

    def downstream_of(self, other: "StateNode") -> bool:



def day2_graph(grid: List[str]):
    h = len(grid)
    w = len(grid[0])









if __name__ == '__main__':
    print(timeit.timeit(lambda: day2('input'), number=1))
    print("total recursive checks:", TOT_REC_CHECKS)
    print("total check steps:", TOT_CHECK_STEPS)
    print("average check steps:", TOT_CHECK_STEPS / TOT_REC_CHECKS)
    print("max turns", MAX_TURNS)

    print(day1('example.txt'))
    print(day1('input'))
    print(day2('example.txt'))
    print(day2('input'))



