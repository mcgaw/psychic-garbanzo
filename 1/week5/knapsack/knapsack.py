# Uses python3
import sys
import random

def max_in_sorted(max, sorted):
    last = None
    for e in sorted:
        if e > max:
            break
        last = e

    return last

def optimal_weight(W, weights):
    w = weights

    knapsack_matrix = []

    for i in range(1, len(w)+1):
        row = [0]
        knapsack_matrix.append(row)
        current_bar = w[i-1]
        for x in range(1, W+1):
            # if weight is not enough to hold a bar
            if i == 1 and current_bar >  x:
                knapsack_matrix[i-1].append(0)
                continue

            # if weight not previously used
            if i == 1:
                knapsack_matrix[i-1].append(current_bar)
                continue

            not_used = knapsack_matrix[i-2][x]

            # if used then get optimal for knapsack without that weight
            # then add it
            used = 0
            previous_weight = x - current_bar
            if previous_weight >= 0:
                used = knapsack_matrix[i-2][x - current_bar] + current_bar

            # solution to sub-problem is just the maximal
            if used > not_used and used <= W:
                knapsack_matrix[i-1].append(used)
            else:
                knapsack_matrix[i-1].append(not_used)
        #print(knapsack_matrix)
    return knapsack_matrix[len(w)-1][W]


def random_ints(num, max):
    ints = []
    count = 0
    while count < num:
        ints.append(random.randint(1, max))
        count += 1
    return ints


if __name__ == '__main__':
    input = sys.stdin.read()
    W, n, *w = list(map(int, input.split()))

    #ints = random_ints(100000, 300)
    #for i in ints:
        #print(str(i), end=' ')
    print(optimal_weight(W, w))
