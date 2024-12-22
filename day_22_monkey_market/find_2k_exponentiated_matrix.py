from day_22_monkey_market.monkey_market import get_hash_matrix
from util.matrix_math import matrix_power_log

if __name__ == "__main__":
    hash_matrix = get_hash_matrix()
    # two_thousandth_hash_matrix = matrix_power_linear(hash_matrix, 2000)
    two_thousandth_hash_matrix = matrix_power_log(hash_matrix, 2000)
    two_thousandth_hash_matrix %= 2
    print(two_thousandth_hash_matrix)
