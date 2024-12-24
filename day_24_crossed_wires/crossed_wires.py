from functools import cache
from itertools import chain

from util.timer import get_results
from parser.parser import read_lines, read_line, read_grid, read_list_grid, read_line_blocks
from typing import List, Dict, Tuple, Optional

# It seems we are defining a binary tree with operator internal node and initial operand leaf nodes
# Kind of. Subtrees can be duplicated (one output can be connectesd to many inputs)

def parse_gates(gates: List[str]) -> Dict[str, Tuple[str, str, str]]:
    outputs = {}
    for gate in gates:
        l, output = gate.split(" -> ")
        input1, operator, input2 = l.split(" ")
        outputs[output] = operator, input1, input2
        #assert not (operator == "XOR" and input1 == input2), gate  # No obvious dont cares.
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


# https://graph-visualizer-with-ts.netlify.app/
def format_graph_leetcode_style(outputs):
    out = []
    for output, (op, in1, in2) in outputs.items():
        op_str = " ".join([in1, op, in2])
        out.append([op_str, output])
        out.append([in1, op_str])
        out.append([in2, op_str])
    return out

def get_outputs_by_gate(gates: List[str]):
    output_by_gate = {}
    for gate in gates:
        l, output = gate.split(" -> ")
        input1, operator, input2 = l.split(" ")
        input1, input2 = sorted([input1, input2])
        #assert not (operator == "XOR" and input1 == input2), gate  # No obvious dont cares.
        output_by_gate[(input1, operator, input2)] = output
    return output_by_gate

def part2(line_blocks: List[List[str]]):
    initial_values_list, gates = line_blocks
    #print(format_graph_leetcode_style(outputs))

    outputs_by_gate = get_outputs_by_gate(gates)
    def outputted_by(t):    # a OP b -> Optional[output]
        in1, op, in2 = t
        assert in1 is not None and in2 is not None, "Input wire is None." + str(t)
        in1, in2 = sorted([in1, in2])
        return outputs_by_gate.get((in1, op, in2), None)

    # Given WIRE OP ?, what (if any) can ? be
    def find_other_input(needed_in, needed_op):
        for in1, op, in2 in outputs_by_gate.keys():
            if op == needed_op:
                if in1 == needed_in:
                    return in2
                elif in2 == needed_in:
                    return in1
        return None

    swaps = []

    # We enforce the ripple adder structure, from lowest to highest bits.
    carry_in = outputs_by_gate[("x00", "AND", "y00")]   # By manual inspection, level 0 is correct.
    for num in range(1, 45):
        x = f"x{num:02}"
        y = f"y{num:02}"
        #print("On ripple adder", num, x, y)

        # These gates MUST exist. (can't swap literal inputs)
        xANDy_out = outputted_by((x, "AND", y))
        xXORy_out = outputted_by((x, "XOR", y))

        possible_out: Optional[str] = outputted_by((carry_in, "XOR", xXORy_out))
        possible_carry_AND_xor = outputted_by((carry_in, "AND", xXORy_out))

        # Given both above have the same inputs, both should be wrong at the same time.
        assert not ((possible_out is None) ^ (possible_carry_AND_xor is None))

        if possible_out is None:
            # Either carry_in or xXORy is wrong.
            possible_corrected_carry_in_via_AND = find_other_input(xXORy_out, "AND")
            possible_corrected_carry_in_via_XOR = find_other_input(xXORy_out, "XOR")
            assert possible_corrected_carry_in_via_AND == possible_corrected_carry_in_via_XOR   # Two results should be the same.

            possible_corrected_XOR_via_AND = find_other_input(carry_in, "AND")
            possible_corrected_XOR_via_XOR = find_other_input(carry_in, "XOR")
            assert possible_corrected_XOR_via_AND == possible_corrected_XOR_via_XOR

            assert possible_corrected_carry_in_via_AND is not None or possible_corrected_XOR_via_AND is not None

            if possible_corrected_carry_in_via_AND is not None:
                assert possible_corrected_XOR_via_AND is None

                swaps.append((carry_in, possible_corrected_carry_in_via_AND))   # Swap carry_in with this value.
                carry_in = possible_corrected_carry_in_via_AND

            elif possible_corrected_XOR_via_AND is not None:
                assert possible_corrected_carry_in_via_AND is None

                swaps.append((xXORy_out, possible_corrected_XOR_via_AND))   # Swap xXORy with this value.
                xXORy_out = possible_corrected_XOR_via_AND

            # Update those values.
            #possible_out = outputted_by((carry_in, "XOR", xXORy_out))      # Unused. We should check for z, but I didnt need to.
            possible_carry_AND_xor = outputted_by((carry_in, "AND", xXORy_out))


        # If Either of the above are wrong, this will fail.
        possible_carry_out = outputted_by((xANDy_out, "OR", possible_carry_AND_xor))
        if possible_carry_out is None:
            # Either xAndY_out is wrong, or possible_carry_AND_xor is wrong.
            diff_lower_and = find_other_input(possible_carry_AND_xor, "OR")
            diff_higher_and = find_other_input(xANDy_out, "OR")

            if diff_lower_and is not None:
                assert diff_higher_and is None

                swaps.append((xANDy_out, diff_lower_and))   # Swap xANDy_out and this
                xANDy_out = diff_lower_and

            elif diff_higher_and is not None:
                assert diff_lower_and is None

                swaps.append((possible_carry_AND_xor, diff_higher_and)) # swap possible_carry_AND_xor and this
                possible_carry_AND_xor = diff_higher_and

            possible_carry_out = outputted_by((xANDy_out, "OR", possible_carry_AND_xor))

        # Update carry.
        carry_in = possible_carry_out


    # Remove duplicates. Because if we swap one thing, we will just end up swapping it again.
    non_duplicate_swaps = set(tuple(sorted(t)) for t in swaps)
    return ",".join(sorted(chain(*non_duplicate_swaps)))



# We have 222 output wires.
# To check all pairs, we have 222 Choose 8 / 2^4, or like (222*221/2)(220)... so like something E 15, too big
# => Checking all pairs is ostensibly computationally infeasible

# By manual input inspection, (and gate counting) this is a pretty bog standard ripple adder.
# => We go lower to higher bits, updating our structure.
# The only thing we really carry over from previous layers is the carry bit (which can be wrong)
# So, just assume that we only have 1 thing wrong per gate (as otherwise this would be complicated)

# If we don't utilize the underlying ripple adder structure, this is a VERY complicated problem (to make fast)
# (In general you can brute force by just checking all swap pairs and then verifying correctness, too slow)
# Below are my messy notes working through the problem.


# So, we know what the z wires outputs should look like as logical expressions of the inputs
# If the logic is equivalent, we are good.

# Can we say that if some portion is correct, we should not swap it?
# It may be the case that >= 1 swap may yield a correct result.
# One thing we can say is that a more significant bit should never actually be able to impact a less significant bit.
# Its possible it may end up in the tree as a don't care?
# Well, its always possible that some wire outputs a 0, or outputs a 1 (not sure one 1, given xor) (a ^ a = 0)
# Im just gonna assume we dont have any dont cares.

# If the output of some z is INCORRECT
# Then at least one change MUST occur downstream
# We can iterate from least to most significant digit, and try to make it work.
# Since logically, less significant outputs can be relevent.

# output zi MUST have downstream: x[0..i], y[0..i]
# and (probably) only those.

# The final z output wires can be swapped.

# Assume: there are no useless (connected) outputs in the final solution.

# https://en.wikipedia.org/wiki/Binary_decision_diagram
# It is ordered. (Eric claims it)
# And it will remain ordered. *
# Is this reduced? If its not reduced, can we do anything about it? Not really.
# Equivalence checking is, in general, NP-complete.

# At least can just assume that the inputs from previous Z's are accurate.
# Given only 222 output wires with 45 outputs, we have just under 5 gates per output.
# z is NEVER used as input value.
# 222 = 45 * 45 - 3
#

# In a standard adder, you have out = in1 ^ in2 ^ carry_in
# and carry_out = (carry_in and (in1 ^ in2)) OR (in1 & in2)
# So carry and 1 op, or both ops
# The structure seems to be that of a ripple adder.
# z45 exists.

# z00 is correct.
# adder 0 has 2 gates = 5 - 3
# So all other gates are just bog standard ripple adders.
# We can enforce the ripple adder structure onto it.

# the following gates MUST exist:
# xn AND yn
# xn XOR yn
# We assume for now that x0, y0 is correct.
# We dont know if the output is correct, but we do know they output.

# the x AND y goes into the OR carry guy

# Can we assume to have identified the carry wire?
# well, we know a carry wire.
# While we cant change out inputs, we can change our outputs.

#



# z39 is wrong.
# z32 is wrong. (AND)


if __name__ == '__main__':
    get_results("P1 Example", part1, read_line_blocks, "example.txt", expected=4)
    get_results("P1 Example Larger", part1, read_line_blocks, "example2.txt", expected=2024)
    get_results("P1", part1, read_line_blocks, "input.txt")

    get_results("P2", part2, read_line_blocks, "input.txt")