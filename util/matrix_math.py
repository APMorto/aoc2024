import numpy as np


def matrix_power_linear(matrix: np.ndarray, n: int):
    if n == 0:
        return np.eye(*matrix.shape)
    cur = matrix.copy()
    for _ in range(n - 1):
        cur @= matrix
    return cur

def matrix_power_log(matrix: np.ndarray, n: int):
    if n == 0:
        return np.eye(*matrix.shape)
    elif n == 1:
        return matrix

    call_stack_do_square = []
    cur_n = n
    while cur_n > 1:
        if cur_n % 2 == 1:
            call_stack_do_square.append(False)
            cur_n -= 1
        else:
            call_stack_do_square.append(True)
            cur_n //= 2

    cur = matrix.copy()
    for do_square in reversed(call_stack_do_square):
        if do_square:
            cur @= cur
        else:
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


def left_shift_of_matrix(matrix: np.ndarray, shift: int):
    # We apply the matrix to a row vector
    # Thus, we shift down the matrix.
    shift_matrix = left_shift_matrix(matrix.shape[0], shift)
    return np.matmul(matrix, shift_matrix) % 2


def left_shift_matrix(n: int, shift: int):
    matrix = np.eye(n, n, dtype=np.uint8)
    shifted_matrix = np.zeros(matrix.shape, dtype=np.uint8)
    shifted_matrix[:n-shift, :] = matrix[shift:, :]
    return shifted_matrix


def right_shift_of_matrix(matrix: np.ndarray, shift: int):
    shift_matrix = right_shift_matrix(matrix.shape[0], shift)
    return np.matmul(matrix, shift_matrix) % 2


def right_shift_matrix(n: int, shift: int):
    matrix = np.eye(n, n, dtype=np.uint8)
    shifted_matrix = np.zeros(matrix.shape, dtype=np.uint8)
    shifted_matrix[shift:, :] = matrix[:n-shift, :]
    return shifted_matrix
