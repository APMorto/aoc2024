import timeit


def time_with_output(func):
    # timeit is much more accurate than time.time.
    res = [None]
    elapsed = timeit.timeit(lambda: res.__setitem__(0, func()), number=1)
    return res[0], elapsed

def get_results(name, solution, parse_fn, fp, **kwargs):
    if solution is None:
        print(f"{name}: N/A")
        return None, 0, 0
    try:
        input, parse_time = time_with_output(lambda: parse_fn(fp))
    except FileNotFoundError as e:
        print(e)
        return None, 0, 0

    res, elapsed = time_with_output(lambda: solution(input))

    if kwargs.get("dense", False):
        print(f"{name}: {str(res) : >14}, Ex: {elapsed:.3f}s, Prs: {parse_time:.4f}s")
    else:
        print(f"{name}:")
        if "expected" in kwargs and kwargs["expected"] != res:
            print(" ", res, "❌")
            print("  Expected:", kwargs["expected"])
        elif "expected" in kwargs and kwargs["expected"] == res:
            print(" ", res, "✅")
        else:
            print( " ", res)

        if elapsed > 1e-5:
            print(f"  {elapsed:.6f} s (Execution)")
            print(f"  {parse_time:.6f} s (Parsing)")
        else:
            print(f"  {elapsed:.12f} s (Execution)")
            print(f"  {parse_time:.12f} s (Parsing)")

    return res, elapsed, parse_time
