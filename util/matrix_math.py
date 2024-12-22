import numpy as np


def matrix_power_linear(matrix: np.ndarray, n: int):
    if n == 0:
        return np.eye(*matrix.shape)
    cur = matrix.copy()
    for _ in range(n - 1):
        cur @= matrix
    return cur

def row_vector_of_integer(val: int, n: int):
    out = np.zeros(n, dtype=np.uint8)
    for i in range(n):
        if val & (1 << i):
            out[i] = 1
    return out

def integer_of_row_vector(row_vector: np.ndarray):
    n = len(row_vector)
    out = 0
    for i in range(n):
        out += int(row_vector[i]) << i
    return out