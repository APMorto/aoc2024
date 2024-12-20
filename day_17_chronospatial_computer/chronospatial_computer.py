import math

from util.timer import get_results
from parser.parser import read_lines, read_line, read_grid, read_list_grid, read_line_blocks
from typing import List

# code[IP] = opcode
# code[IP+1] = operand
# if IP OOB -> Halt.

# literal operand v = v

# combo operand [0 - 3] = [0 - 3]
# combo operand [4, 5, 6] = [A, B, C]
# combo operand 7 is reserved and will not appear.

# opcode 0: adv. truncate(A / 2**[combo operand]) -> A
# opcode 1: bxl. (B ^ literal operand) -> B
# opcode 2: bst. (combo % 8) -> B  | (combo & 0b111) -> B
# opcode 3: jnz. If A != 0, literal operand -> IP, IP does not increment
# opcode 4: bxc. (B ^ C) -> B, Note: still reads an unused operand.
# opcode 5: out. (combo operand % 8) -> OUT
# opcode 6: bdv. truncate(A / 2**[combo operand]) -> B
# opcode 7: cdv. truncate(A / 2**[combo operand]) -> C

class ChronospatialComputer:
    def __init__(self, program: List[int], A: int, B: int, C: int):
        self.A: int = A
        self.B: int = B
        self.C: int = C
        self.IP: int = 0
        self.program: List[int] = program
        self.halted: bool = False
        self.n: int = len(program)
        self.output_list = []
        self.expected_output = None
        self.expects = False
        self.valid = True

    def expect(self, expected):
        self.expected_output = expected
        self.expects = True

    def run_to_halting(self):
        while not self.execute():
            pass
        return self.output_list

    def execute(self) -> bool:
        if not 0 <= self.IP < self.n - 1:
            self.halted = True
            return True

        opcode = self.program[self.IP]
        operand = self.program[self.IP + 1]

        combo_operand = operand if operand < 4 else (self.A, self.B, self.C, None)[operand - 4]

        match opcode:
            case 0: # 0b000
                self.A = math.trunc(self.A / (1 << combo_operand))
            case 1: # 0b001
                self.B = self.B ^ operand
            case 2: # 0b010
                self.B = combo_operand & 0b111
            case 3: # 0b011
                if self.A != 0:
                    self.IP = operand - 2   # Increments by 2 afterward.
            case 4: # 0b100
                self.B ^= self.C
            case 5: # 0b101
                self.output_list.append(combo_operand & 0b111)
                if self.expects:
                    l = len(self.output_list)
                    if l > len(self.output_list):
                        self.valid = False
                    elif self.output_list[l - 1] != self.expected_output[l-1]:
                        self.valid = False
                #self.outputs(combo_operand & 0b111)
            case 6: # 0b110
                self.B = math.trunc(self.A / (1 << combo_operand))
            case 7: # 0b111
                self.C = math.trunc(self.A / (1 << combo_operand))

        self.IP += 2
        return False

    def state(self):
        return self.A, self.B, self.C, self.IP, len(self.output_list)

    def outputs(self, val: int):
        self.output_list.append(val)

    def __repr__(self):
        return f"A: {self.A}, B: {self.B}, C: {self.C}, IP: {self.IP}, OUT: {self.output_list}"


def initialalize_computer(line_blocks):
    registers, program_string = line_blocks
    A = int(registers[0][len("Register _: "):])
    B = int(registers[1][len("Register _: "):])
    C = int(registers[2][len("Register _: "):])
    program = list(map(int, program_string[0][len("Program: "):].split(",")))
    return ChronospatialComputer(program, A, B, C)


def part1(line_blocks):
    computer = initialalize_computer(line_blocks)
    computer.run_to_halting()
    return ",".join(map(str, computer.output_list))


def part2(line_blocks):
    registers, program_string = line_blocks
    A = int(registers[0][len("Register _: "):])
    B = int(registers[1][len("Register _: "):])
    C = int(registers[2][len("Register _: "):])
    program = list(map(int, program_string[0][len("Program: "):].split(",")))

    seen_states = set()

    # For what value of A will this computer output itself?
    for A in range(0, 1 << 32):
        if A & 1 << 30:
            print("Iteration:", A)

        computer = ChronospatialComputer(program, A, B, C)
        computer.expect(program)

        while computer.valid:
            if computer.execute():
                assert computer.halted
                break
            state = computer.state()
            if state in seen_states:
                break
            seen_states.add(state)
        if computer.valid and len(computer.output_list) == len(program):
            return A

    return None



# not 2,3,1,2,4,3,5,2,2


if __name__ == '__main__':
    get_results("P1 Example", part1, read_line_blocks, "example.txt", expected="4,6,3,5,6,3,5,2,1,0")
    get_results("P1", part1, read_line_blocks, "input.txt")

    get_results("P2 Example", part2, read_line_blocks, "example2.txt", expected=117440)
    get_results("P2", part2, read_line_blocks, "input.txt")