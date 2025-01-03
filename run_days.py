import os
import sys

from util.timer import get_results
from parser.parser import read_grid, read_list_grid, read_line, read_line_blocks, read_lines

import day_01_historian_hysteria.historian_hysteria as day_01
import day_02_red_nosed_reports.red_nosed_reports as day_02
import day_03_mull_it_over.mull_it_over         as day_03
import day_04_ceres_search.search               as day_04
import day_05_print_queue.print_order           as day_05
import day_06_guard_gallivant.guard             as day_06
import day_07_bridge_repair.calibration         as day_07
import day_08_resonant_collinearity.antinodes   as day_08
import day_09_disk_fragmenter.disk_moving       as day_09
import day_10_hoof_it.height_hiking             as day_10
import day_11_plutonian_pebbles.blinking_pebbles as day_11
import day_12_garden_groups.garden_groups       as day_12
import day_13_claw_contraption.claw_contraption as day_13
import day_14_restroom_redoubt.restroom_redoubt as day_14
import day_15_warehouse_woes.warehouse_woes     as day_15
import day_16_reindeer_maze.reindeer_maze       as day_16
import day_17_chronospatial_computer.chronospatial_computer as day_17
import day_18_ram_run.ram_run                   as day_18
import day_19_linen_layout.linen_layout         as day_19
import day_20_race_condition.race_condition     as day_20
import day_21_keypad_conundrum.keypad_conundrum as day_21
import day_22_monkey_market.monkey_market       as day_22
import day_23_lan_party.lan_party               as day_23
import day_24_crossed_wires.crossed_wires       as day_24
import day_25_code_chronicle.code_chronicle     as day_25

day_information = {
# DAY: (p1, p2, input_fn, [input_fn2], "dir")
    1: (day_01.part1,   day_01.part2,       read_lines,         "day_01_historian_hysteria"),
    2: (day_02.both_parts, day_02.both_parts, read_lines,       "day_02_red_nosed_reports"),
    #2: (day_02.part1,   day_02.part2,       read_lines,         "day_02_red_nosed_reports"),
    3: (day_03.part1,   day_03.part2,       read_lines,         "day_03_mull_it_over"),
    #4: (day_04.part1,   day_04.part2,       read_grid,          "day_04_ceres_search"),
    4: (day_04.part1_faster, day_04.part2,  read_grid,          "day_04_ceres_search"),
    #5: (day_05.part1,   day_05.part2,       read_line_blocks,   "day_05_print_queue"),
    5: (day_05.both_parts_faster,day_05.both_parts_faster, read_line_blocks,   "day_05_print_queue"),
    6: (day_06.part1,   day_06.part2_graph, read_list_grid,     "day_06_guard_gallivant"),
    7: (day_07.part1,   day_07.part2, day_07.read_equations,    "day_07_bridge_repair"),
    8: (day_08.part1,   day_08.part2,       read_grid,          "day_08_resonant_collinearity"),
    9: (day_09.part1,   day_09.part2,       read_line,          "day_09_disk_fragmenter"),
    10: (day_10.part1_bitwise,  day_10.part2,       read_grid,          "day_10_hoof_it"),  # p1 bitwise ~2ms from 100ms
    #10: (day_10.part1,  day_10.part2,       read_grid,          "day_10_hoof_it"),
    11: (day_11.part1,  day_11.part2,       read_line,          "day_11_plutonian_pebbles"),
    12: (day_12.both_parts_numpy,  day_12.both_parts_numpy, read_grid,          "day_12_garden_groups"),
    #12: (day_12.part1,  day_12.part2,       read_grid,          "day_12_garden_groups"),
    13: (day_13.part1,  day_13.part2,       read_line_blocks,   "day_13_claw_contraption"),
    14: (day_14.part1,  None,               read_lines,         "day_14_restroom_redoubt"),
    15: (day_15.part1,  day_15.part2,       read_line_blocks,   "day_15_warehouse_woes"),
    16: (day_16.part1_and_2,  day_16.part1_and_2,       read_grid,          "day_16_reindeer_maze"),
    #16: (day_16.part1,  day_16.part2,       read_grid,          "day_16_reindeer_maze"),
    17: (day_17.part1,  day_17.part2,       read_line_blocks,   "day_17_chronospatial_computer"),
    18: (day_18.part1,  day_18.part2,       read_lines,         "day_18_ram_run"),
    19: (day_19.part1,  day_19.part2,       read_line_blocks,   "day_19_linen_layout"),
    20: (day_20.part1,  day_20.part2_inline, read_grid,         "day_20_race_condition"),   # inline is faster than sliding window in pypy
    #20: (day_20.part1,  day_20.part2_sliding_window, read_grid, "day_20_race_condition"),
    21: (day_21.part1,  day_21.part2,       read_lines,         "day_21_keypad_conundrum"),
    22: (day_22.part1_binary_matrix_operations,  day_22.part2_array,       read_lines,         "day_22_monkey_market"),
    23: (day_23.part1,  day_23.part2,       read_lines,         "day_23_lan_party"),
    24: (day_24.part1,  day_24.part2,       read_line_blocks,   "day_24_crossed_wires"),
    25: (day_25.part1,  None,               read_line_blocks,   "day_25_code_chronicle"),

}


if __name__ == "__main__":
    print(sys.version, sys.argv, '\n')
    p1_results, p2_results = [], []
    p1_times, p2_times = [], []
    p1_parse_times, p2_parse_times = [], []

    days = sorted(day_information.keys())
    for day in days:
        # Get day info
        t = day_information[day]
        if len(t) == 4:
            p1, p2, parse, folder = t
            parse1 = parse2 = parse
        elif len(t) == 5:
            p1, p2, parse1, parse2, folder = t
        else:
            raise Exception("Expected 4 or 5 elements in day, not " + str(len(t)))

        file = os.path.join(folder, "input.txt")
        if p1 is p2:
            (res1, res2), time_b, parse_time_b = get_results(f"Day {day} P1&P1", p1, parse1, file, dense=True)
            # Uniformly distribute for now.
            time1 = time2 = time_b / 2
            parse_time1 = parse_time2 = parse_time_b / 2
        else:
            res1, time1, parse_time1 = get_results(f"Day {day} P1", p1, parse1, file, dense=True)
            res2, time2, parse_time2 = get_results(f"Day {day} P2", p2, parse2, file, dense=True)
        print()

        p1_results.append(res1)
        p2_results.append(res2)

        p1_times.append(time1)
        p2_times.append(time2)

        p1_parse_times.append(parse_time1)
        p2_parse_times.append(parse_time2)

    print()

    # Get total times.
    total_p1_time, total_p2_time, total_p1_parse_time, total_p2_parse_time = map(sum, (p1_times, p2_times, p1_parse_times, p2_parse_times))
    total_time = sum((total_p1_time, total_p2_time, total_p1_parse_time, total_p2_parse_time))
    total_times = list(map(sum, zip(p1_times, p2_times, p1_parse_times, p2_parse_times)))

    # Header.
    print("Total Time (All Days):", total_time, "(s)")
    print(f"Total part 1 (All Days): {total_p1_time:.3f}s | {total_p1_time / total_time: 3.1%}")
    print(f"Total part 2 (All Days): {total_p2_time:.3f}s | {total_p2_time / total_time: 3.1%}")
    print(f"Total parsing (P1&2): {total_p1_parse_time+total_p2_parse_time:.3f}s | {(total_p1_parse_time+total_p2_parse_time) / total_time: 3.1%}")
    print()

    # Print the days.
    for i in range(len(days)):
        day = days[i]
        day_str = str(day) if day >= 10 else f"0{day}"
        print(f"Day {day :2}: {total_times[i] :1.3f}s | {total_times[i] / total_time: 3.1%}")
