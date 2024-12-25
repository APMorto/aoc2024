from util.timer import get_results
from parser.parser import read_lines, read_line, read_grid, read_list_grid, read_line_blocks
from typing import List

def is_monotonic(numbers):
    if len(numbers) < 2:
        return True
    if numbers[0] < numbers[1]:
        return all(numbers[i-1] < numbers[i] for i in range(2, len(numbers)))
    elif numbers[0] > numbers[1]:
        return all(numbers[i - 1] > numbers[i] for i in range(2, len(numbers)))
    else:
        return False

def is_safe(numbers, ignore=None):
    return is_monotonic(numbers) and all(1 <= abs(numbers[i-1] - numbers[i]) <= 3 for i in range(1, len(numbers)))

def part1(lines: List[str]):
    out = 0
    for line in lines:
        numbers = tuple(map(int, line.split()))
        if is_safe(numbers):
            out += 1
    return out

def part2(lines: List[str]):
    out = 0
    for line in lines:
        numbers = list(map(int, line.split()))
        if is_safe(numbers):
            out += 1
        else:
            n = len(numbers)
            hold = numbers.pop(n-1)
            if is_safe(numbers):
                out += 1
            else:
                for i in range(n-2, -1, -1):
                    hold, numbers[i] = numbers[i], hold
                    if is_safe(numbers):
                        out += 1
                        break

    return out

def both_parts(lines: List[str]):
    out1 = 0
    out2 = 0
    for line in lines:
        numbers = list(map(int, line.split()))
        n = len(numbers)

        # Its Possible that we may remove some of the first numbers.
        up = 0
        down = 0
        # Look at the first 3 deltas to determine the monotonicity (len(numbers)) >= 4
        for i in range(3):
            if numbers[i] < numbers[i + 1]:
                up += 1
            #elif numbers[i] > numbers[i + 1]:
            else:
                down += 1

        bad_connection1 = -2
        bad_connection2 = -2
        broken = False
        if up > down:
            # Monotonically increasing.
            for i in range(1, n):
                if numbers[i-1] >= numbers[i] or numbers[i] - numbers[i-1] > 3:
                    if bad_connection1 == -2:
                        bad_connection1 = i
                    else:
                        bad_connection2 = i
                        if bad_connection1 != i-1:
                            broken = True
                            break
            if broken:
                continue

            if bad_connection1 == -2:   # No bad connection
                out1 += 1
                out2 += 1
            elif bad_connection1 == bad_connection2 - 1:    # 2 bad connections
                # Is it fixed by removing value on bad connection 1?
                if numbers[bad_connection1-1] < numbers[bad_connection2] and numbers[bad_connection2] - numbers[bad_connection1-1] <= 3:
                    out2 += 1
            else: # Remove either bad_connection1 or bad_connection1-1
                if (bad_connection1 < n-1 and numbers[bad_connection1-1] < numbers[bad_connection1+1] and numbers[bad_connection1+1] - numbers[bad_connection1-1] <= 3) or \
                    (bad_connection1 > 1 and  numbers[bad_connection1-2] < numbers[bad_connection1]   and numbers[bad_connection1] -   numbers[bad_connection1-2] <= 3) or \
                        bad_connection1 == 1 or bad_connection1 == n-1:
                    out2 += 1

        else:
            # Monotonically decreasing.
            for i in range(1, n):
                if numbers[i-1] <= numbers[i] or numbers[i-1] - numbers[i] > 3:
                    if bad_connection1 == -2:
                        bad_connection1 = i
                    else:
                        bad_connection2 = i
                        if bad_connection1 != i-1:
                            broken = True
                            break
            if broken:
                continue

            if bad_connection1 == -2:   # No bad connection
                out1 += 1
                out2 += 1
            elif bad_connection1 == bad_connection2 - 1:    # 2 bad connections
                # Is it fixed by removing value on bad connection 1?
                if numbers[bad_connection1-1] > numbers[bad_connection2] and numbers[bad_connection1-1] - numbers[bad_connection2] <= 3:
                    out2 += 1
            else: # Remove either bad_connection1 or bad_connection1-1
                if (bad_connection1 < n-1 and numbers[bad_connection1-1] > numbers[bad_connection1+1] and numbers[bad_connection1-1] - numbers[bad_connection1+1] <= 3) or \
                    (bad_connection1 > 1 and  numbers[bad_connection1-2] > numbers[bad_connection1]   and numbers[bad_connection1-2] - numbers[bad_connection1]   <= 3) or \
                        bad_connection1 == 1 or bad_connection1 == n-1:
                    out2 += 1

    return out1, out2

if __name__ == '__main__':
    get_results("P1 Example", part1, read_lines, "example.txt", expected=2)
    get_results("P1", part1, read_lines, "input.txt")

    get_results("P2 Example", part2, read_lines, "example.txt", expected=4)
    get_results("P2", part2, read_lines, "input.txt")

    get_results("Both parts Faster", both_parts, read_lines, "input.txt", expected=(359, 418))