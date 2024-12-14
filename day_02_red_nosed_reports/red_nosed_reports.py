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


if __name__ == '__main__':
    get_results("P1 Example", part1, read_lines, "example.txt", expected=2)
    get_results("P1", part1, read_lines, "input.txt")

    get_results("P2 Example", part2, read_lines, "example.txt", expected=4)
    get_results("P2", part2, read_lines, "input.txt")