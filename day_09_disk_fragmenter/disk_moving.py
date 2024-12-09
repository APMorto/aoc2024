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




if __name__ == '__main__':
    get_results("P1 Example", part1, read_line, "example.txt")
    get_results("P1", part1, read_line, "input.txt")