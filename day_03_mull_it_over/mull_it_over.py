from util.timer import get_results
from parser.parser import read_lines
import re

def part1(lines):
    line = "\n".join(lines)
    out = 0
    for x in re.findall(r"mul\((\d+),(\d+)\)", line):
        out +=int(x[0]) * int(x[1])
    return out


def part2(lines):
    line = "\n".join(lines)
    out = 0
    allowed = True
    for x in re.findall(r"mul\(\d+,\d+\)|do\(\)|don't\(\)", line):
        if x == "don't()":
            allowed = False
        elif x == "do()":
            allowed = True
        elif allowed:
            y = re.findall(r"mul\((\d+),(\d+)\)", x)[0]
            out +=int(y[0]) * int(y[1])
    return out

if __name__ == '__main__':
    get_results("P1 Example", part1, read_lines, "example.txt", expected=161)
    get_results("P1", part1, read_lines, "input.txt")

    get_results("P2 Example", part2, read_lines, "example2.txt", expected=48)
    get_results("P2", part2, read_lines, "input.txt")