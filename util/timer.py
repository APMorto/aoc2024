import time

def time_with_output(func):
    start = time.time()
    out = func()
    end = time.time()
    elapsed = end - start
    return out, elapsed

def get_results(name, solution, parse_fn, fp):
    input = parse_fn(fp)
    res, elapsed = time_with_output(lambda: solution(input))
    print(f"{name}:")
    print("   ", res)
    print("   ", elapsed, "s")

