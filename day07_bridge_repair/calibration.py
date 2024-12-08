from typing import List

from parser.parser import read_lines
from util.timer import get_results

def read_equations(fp):
    return [split_equation(line) for line in read_lines(fp)]

def split_equation(line: str):
    colon, numbers = line.split(": ")
    return int(colon), tuple(map(int, numbers.split()))


def backtracking_solver(result, operands, i, cur):
    if i == len(operands):
        return result == cur

    # operands are > 0, and we only +/*
    if cur > result:
        return False

    return backtracking_solver(result, operands, i + 1, cur+operands[i]) or backtracking_solver(result, operands, i + 1, cur*operands[i])


def can_solve_equation(result, operands):
    return backtracking_solver(result, operands, 1, operands[0])


def part1(equations: List[tuple]) -> int:
    out = 0
    for result, operands in equations:
        if can_solve_equation(result, operands):
            out += result
    return out


# We only get at most 12 elements, so we can easily brute force this.

if __name__ == '__main__':
    get_results("P1 Example", part1, read_equations, "example.txt")
    get_results("P1", part1, read_equations, "input.txt")