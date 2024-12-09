from sortedcontainers import SortedList

from util.timer import get_results
from parser.parser import read_line

# from right to left
# move each disk to the leftmost free space

# sometimes we will be adding a new leftmost space
# so the end of the (array) list should be the 'left'

# would do this in O(n^2)

def read_disk_state(disk, nums) -> None:
    m = len(nums)
    j = 0
    for i, num in enumerate(nums):
        if i % 2 == 0:
            for k in range(j, j+num):
                disk[k] = i // 2
        j += num
    return None


def part1(line: str):
    s_len = len(line)

    nums = list(map(int, line))
    disk = [None] * sum(nums)

    read_disk_state(disk, nums)
    #print(disk)

    # Shift down.

    # l, r are initially valid
    l = 0
    r = len(disk) - 1
    while disk[r] == None:
        r -= 1
    while disk[l] != None:
        l += 1

    while l < r:
        # Shift.
        disk[l] = disk[r]
        disk[r] = None

        # Make r, valid
        while disk[r] == None:
            r -= 1
        while disk[l] != None:
            l += 1

    # get out value
    out = 0
    for i, id in enumerate(disk):
        if id == None:
            break
        out += i * id
    return out


# In part 2 we move the entire files.
# So, we just have free blocks at some positions
# and blocks at some positions
# and we attempt moving in decreasing id
def part2(line: str):
    s_len = len(line)
    nums = list(map(int, line))

    available_blocks_of_size = [SortedList() for _ in range(10)]  # [0] == [] should always hold
    initial_block_positions = []    # (id, pos, size)

    j = 0
    #for i in range(s_len-1, -1, -1):
    #    num = nums[i]
    for i, num in enumerate(nums):
        if i % 2 == 0:
            initial_block_positions.append((i // 2, j, num))
        else:
            if num > 0:
                available_blocks_of_size[num].add(j)
        j += num

    out = 0
    for id, pos, size in reversed(initial_block_positions):
        # Dest is the smallest value, not the smallest value of the smallest space.
        dest = pos
        chosen_size = -1
        for candidate_size in range(size, 10):
            sl = available_blocks_of_size[candidate_size]
            if len(sl) == 0:
                continue
            #dest = min(dest, sl[0])
            if sl[0] < dest:
                chosen_size = candidate_size
                dest = sl[0]

        if dest < pos:
        #for candidate_size in range(size, 10):
        #    sl = available_blocks_of_size[candidate_size]
        #    if len(sl) == 0:
        #        continue
        #    # We can put it somwhere!
        #    dest = sl.pop(0)
            available_blocks_of_size[chosen_size].pop(0)
            #print(f"Putting {(id, pos, size)} at {dest}")

            # Put the remaining space back in
            remaining_size = chosen_size - size
            if remaining_size > 0:
                available_blocks_of_size[remaining_size].add(dest + size)

            # Free up where we were
            available_blocks_of_size[size].add(pos)

            # Add the results from this
            for k in range(dest, dest+size):
                out += k * id

        else:
            #print(f"Could not put {(id, pos, size)} anywhere. leaving")
            # We cannot put it anywhere.
            # Just add the results from this
            for k in range(pos, pos+size):
                out += k * id

    return out




if __name__ == '__main__':
    get_results("P1 Example", part1, read_line, "example.txt")
    get_results("P1", part1, read_line, "input.txt")

    get_results("P2 Example", part2, read_line, "example.txt")
    get_results("P2", part2, read_line, "input.txt")