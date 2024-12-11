import math
from functools import reduce
from operator import add
from typing import List
import multiprocessing as mp

from parser.parser import read_lines
from util.infix import Infix
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


# We could go right to left.
def backtracking_solver_p2(result, operands, i, cur):
    if i == len(operands):
        return result == cur

    # operands are > 0, and we only +/*
    #if cur > result:
    #    return False

    # Infix usage was 2.33s
    # Infix normal calling was 1.5s
    # no infix usage was 1.3s
    return (
            backtracking_solver_p2(result, operands, i + 1, cur+operands[i]) or
            backtracking_solver_p2(result, operands, i + 1, cur*operands[i]) or
            backtracking_solver_p2(result, operands, i + 1, cat(cur, operands[i]))
            #backtracking_solver_p2(result, operands, i + 1, cur |CAT| operands[i]))
            #backtracking_solver_p2(result, operands, i + 1, CAT(cur, operands[i])))
    )


def can_solve_equation_p2(result, operands):
    return backtracking_solver_p2(result, operands, 1, operands[0])

def eq_value_p2(resultoperands):
    result, operands = resultoperands
    return can_solve_equation_p2(result, operands) * result


def part2(equations: List[tuple]) -> int:
    out = 0
    for result, operands in equations:
        if can_solve_equation_p2(result, operands):
            out += result
    return out

def part2_parallel(equations: List[tuple]) -> int:
    with mp.Pool() as pool:
        return reduce(add, pool.imap_unordered(eq_value_p2, equations))


@Infix
def CAT(a, b):
    return int(str(a)+str(b))

def cat(a, b):
    return a * 10**len(str(b)) + b
    #return a * 10**math.ceil(math.log10(b)) + b    # slower than len, and doesnt even work properly


# We only get at most 12 elements, so we can easily brute force this.

if __name__ == '__main__':
    get_results("P1 Example", part1, read_equations, "example.txt")
    get_results("P1", part1, read_equations, "input.txt")

    get_results("P2 Example", part2, read_equations, "example.txt")
    get_results("P2", part2, read_equations, "input.txt")

    get_results("P2 Parallel", part2_parallel, read_equations, "input.txt")