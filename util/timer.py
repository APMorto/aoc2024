import timeit


def time_with_output(func):
    # timeit is much more accurate than time.time.
    res = [None]
    elapsed = timeit.timeit(lambda: res.__setitem__(0, func()), number=1)
    return res[0], elapsed

def get_results(name, solution, parse_fn, fp):
    input, parse_time = time_with_output(lambda: parse_fn(fp))
    res, elapsed = time_with_output(lambda: solution(input))
    print(f"{name}:")
    print( " ", res)
    if elapsed > 1e-5:
        print(f"  {elapsed:.6f} s (Execution)")
        print(f"  {parse_time:.6f} s (Parsing)")
    else:
        print(f"  {elapsed:.12f} s (Execution)")
        print(f"  {parse_time:.12f} s (Parsing)")