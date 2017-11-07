# Uses python3
import sys

def get_optimal_value(capacity, weights, values):
    weighted_items = {}
    for item in list(zip(weights, values)):
        weighted_value = item[1]/item[0]
        weighted_items[weighted_value] = item

    remaining = capacity
    value = 0
    for k in sorted(weighted_items)[::-1]:
        item = weighted_items[k]
        if remaining >= item[0]:
            remaining -= item[0]
            value += item[1]
        else:
            value += remaining * k
            break

    return value


if __name__ == "__main__":
    data = list(map(int, sys.stdin.read().split()))
    n, capacity = data[0:2]
    values = data[2:(2 * n + 2):2]
    weights = data[3:(2 * n + 2):2]
    opt_value = get_optimal_value(capacity, weights, values)
    print("{:.10f}".format(opt_value))
