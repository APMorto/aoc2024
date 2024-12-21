import collections

from util.timer import get_results
from parser.parser import read_lines, read_line, read_grid, read_list_grid, read_line_blocks
from typing import List, Optional, Tuple

from util.util import pad_grid, seek_character

ACTIONS = ['^', 'A', '<',  'v', '>']
directional_keypad: List[List[Optional[str]]] = [[None, '^', 'A'],
                                                 ['<',  'v', '>']]

numeric_keypad: List[List[Optional[str]]] = [['7', '8', '9'],
                                             ['4', '5', '6'],
                                             ['1', '2', '3'],
                                            [None, '0', 'A']]
n_directional_tiles = 5
n_numeric_tiles = 10
pad_grid(directional_keypad, None)
pad_grid(numeric_keypad, None)
init_dir_rc = seek_character(directional_keypad, 'A')
init_num_rc = seek_character(numeric_keypad, 'A')






def result_keypad(action, r, c, keypad) -> Tuple[Optional[tuple], Optional[str]]:
    match action:
        case '^':
            r -= 1
        case '>':
            c += 1
        case 'v':
            r += 1
        case '<':
            c -= 1
        case 'A':
            return (r, c), keypad[r][c]

    if keypad[r][c] is None:
        return None, None
    return (r, c), None

# A state will be a tuple of (dr1, dc1, dr2, dc2, nr1, nc2, amt_typed)
def neighbors_p1(state_tuple, code):
    dr1, dc1, dr2, dc2, nr1, nc1, amt_typed = state_tuple

    for action in ACTIONS:
        #print("Human action", action)
        dr1_, dc1_, dr2_, dc2_, nr1_, nc1_, amt_typed_ = dr1, dc1, dr2, dc2, nr1, nc1, amt_typed
        # keypad 1
        new_pos, action_out = result_keypad(action, dr1, dc1, directional_keypad)
        #print("Directional 1:", new_pos, action_out)
        if new_pos is None:
            continue
        dr1_, dc1_ = new_pos

        if action_out is not None:
            # keypad 2
            new_pos_2, action_out_2 = result_keypad(action_out, dr2, dc2, directional_keypad)
            #print("Directional 2:", new_pos_2, action_out_2)
            if new_pos_2 is None:
                continue
            dr2_, dc2_ = new_pos_2

            if action_out_2 is not None:
                # Type!
                key_pos, key_press = result_keypad(action_out_2, nr1, nc1, numeric_keypad)
                #print("Keypad", key_pos, key_press)
                if key_pos is None:
                    continue
                nr1_, nc1_ = key_pos
                if key_press is not None:
                    if code[amt_typed] != key_press:
                        #print("Bad code type.", key_press)
                        continue
                    amt_typed_ += 1

        yield dr1_, dc1_, dr2_, dc2_, nr1_, nc1_, amt_typed_


def min_presses_for_code_p1(code):
    initial_state = (*init_dir_rc, *init_dir_rc, *init_num_rc, 0)
    seen = {initial_state}
    q = collections.deque([(0, initial_state)])

    while q:
        d, state = q.popleft()
        #print(d, state)
        for neighbor in neighbors_p1(state, code):
            if neighbor not in seen:
                if neighbor[6] == 4:
                    return d+1
                seen.add(neighbor)
                q.append((d + 1, neighbor))

    return None


def part1(lines):
    out = 0
    for code in lines:
        min_presses = min_presses_for_code_p1(code)
        if min_presses is None:
            print("Couldnt solve code", code)

        numeric_part = int(code[:-1])
        out += numeric_part * min_presses
    return out



def neighbors_p2(state, code):
    *directional_positions, num_position, amt_typed = state

    for action in ACTIONS:
        amt_ = amt_typed
        key_pos = num_position

        # Go through the actions of the keypads.
        valid = True
        diff_position_stack = []
        prev_action = action
        for i in range(25):
            in_position = directional_positions[i]
            out_position, out_action = result_keypad(prev_action, *in_position, directional_keypad)

            if out_position is None:
                valid = False
                break

            diff_position_stack.append(out_position)
            prev_action = out_action
            if out_action is None:
                break

        if not valid:
            continue

        # Go through the action of the keypad
        if prev_action is not None:
            key_pos, key_action = result_keypad(prev_action, *num_position, numeric_keypad)
            if key_pos is None:
                continue

            if key_action is not None:
                if code[amt_typed] != key_action:
                    continue
                amt_ += 1

        # Was valid. Yield state.
        new_dir_positions = (*diff_position_stack, *directional_positions[len(diff_position_stack):])
        yield (*new_dir_positions, key_pos, amt_)


def min_presses_for_code_p2(code):
    initial_state = (*[init_dir_rc]*25, init_num_rc, 0)
    seen = {initial_state}
    q = collections.deque([(0, initial_state)])

    while q:
        d, state = q.popleft()
        #print(d, state)
        for neighbor in neighbors_p2(state, code):
            if neighbor not in seen:
                if neighbor[6] == 4:
                    return d+1
                seen.add(neighbor)
                q.append((d + 1, neighbor))

    return None


def part2(lines):
    out = 0
    for code in lines:
        min_presses = min_presses_for_code_p2(code)
        if min_presses is None:
            print("Couldnt solve code", code)

        numeric_part = int(code[:-1])
        out += numeric_part * min_presses
    return out


# we move from r1, rc -> r2, c2
# There are abs(r1 - r2) Choose abs(c1 -c2) possible ways to get from r1, c1 -> r2, c2
# This is actually true for the first layer.
# This is however not useful for part 1.

# We can never aim at a gap

# Our keypad (press whatever, whenever. What is to be minimized.)
# robot directional keypad 1
# robot directional keypad 2
# robot numeric keypad

# directional keypad has 5 * 4 = 20 states
# numeric keypad has 10 * 4 = 40 states
# combining all of them we get 20 * 20 * 40 = 16000 states (not that many)
# For each pair of states, there is a shortest path of some length.
# However, computer Floyd-Warshalls for this is tough because its O(16000^3), which is simply too large.
# Furthermore, its not really clear what the state of the intermediate keypads should be.

# I was wrong, the robot has no 'direction'
# So we only have 5 * 5 * 10 = 250 states
# and 250 ^ 3 = 15,625,000, so its maybe floyd-warshall-able

# Robots are initialized to be on the A button.

# Anyways, we know the sequence of states of numeric keypad
# we could just bfs this, given the lack of states
# But, we also have the 5 states for amount of presses.
# (really, it can be 4 since on the 5th press, we're done)
# Giving us 1000 states (still utterly trivial)






if __name__ == '__main__':
    get_results("P1 Example", part1, read_lines, "example.txt", expected=126384)
    get_results("P1", part1, read_lines, "input.txt")

    get_results("P2 Example", part2, read_lines, "example.txt")
    get_results("P2", part2, read_lines, "input.txt")