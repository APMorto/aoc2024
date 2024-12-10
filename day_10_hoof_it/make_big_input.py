import random


def write_hiking_array(h, w, dest):
    strs = "0123456789"
    prev = 1

    grid = [[None] * w for _ in range(w)]
    for r in range(h):
        for c in range(w):
            prev_above = int(grid[r-1][c]) if r > 0 else 1
            #new_val = round(random.triangular(-0.5, 9.5, (prev + prev_above) / 2))
            possible_values = {prev_above-1, prev_above+1, prev-1, prev+1}
            new_val = random.choice(tuple(filter(lambda x: 0 <= x <= 9, possible_values)))
            #new_val = max(min(new_val, 9), 0)

            grid[r][c] = strs[new_val]
            prev = new_val

            #grid[r][c] = random.choice(strs)

    with open(dest, "w") as f:
        f.writelines(map(lambda l: "".join(l) + "\n", grid))

write_hiking_array(500, 500, "./custom_500.txt")
write_hiking_array(1000, 1000, "./custom_1000.txt")
write_hiking_array(10000, 10000, "./custom_10000.txt")