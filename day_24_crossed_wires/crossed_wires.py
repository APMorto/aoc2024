from functools import cache

from util.timer import get_results
from parser.parser import read_lines, read_line, read_grid, read_list_grid, read_line_blocks
from typing import List, Dict, Tuple
import re

# It seems we are defining a binary tree with operator internal node and initial operand leaf nodes
# Kind of. Subtrees can be duplicated (one output can be connected to many inputs)

def parse_gates(gates: List[str]) -> Dict[str, Tuple[str, str, str]]:
    outputs = {}
    for gate in gates:
        l, output = gate.split(" -> ")
        input1, operator, input2 = l.split(" ")
        outputs[output] = operator, input1, input2
    return outputs

def parse_initial_values(initial_values_list: List[str]):
    initial_values = {}
    for line in initial_values_list:
        wire, value_str = line.split(": ")
        initial_values[wire] = bool(int(value_str))
    return initial_values

def part1(line_blocks: List[List[str]]):
    initial_values_list, gates = line_blocks
    outputs = parse_gates(gates)
    initial_values = parse_initial_values(initial_values_list)

    @cache
    def get_wire_value(wire: str):
        if wire in initial_values:
            return initial_values[wire]

        operand, in1, in2 = outputs[wire]
        val1, val2 = get_wire_value(in1), get_wire_value(in2)
        match operand:
            case "AND":
                return val1 and val2
            case "OR":
                return val1 or val2
            case "XOR":
                return val1 ^ val2

    # Build output.
    out = 0

    # There are no z wires in the initially given states.
    for output_wire in outputs:
        if output_wire[0] == 'z':
            wire_output = get_wire_value(output_wire)
            out |= int(wire_output) << int(output_wire[1:])
    return out






def part2(_):
    pass


if __name__ == '__main__':
    get_results("P1 Example", part1, read_line_blocks, "example.txt", expected=4)
    get_results("P1 Example Larger", part1, read_line_blocks, "example2.txt", expected=2024)
    get_results("P1", part1, read_line_blocks, "input.txt")

    get_results("P2 Example", part2, read_line_blocks, "example.txt")
    get_results("P2", part2, read_line_blocks, "input.txt")