# Uses python3
import sys


def get_fibonacci_huge(n, m):
    # calculate the Pisano period by looking for a repeat
    # of '0 1' in the modulo sequence
    modulo_seq = [0, 1]
    last = 0 
    current = 1
    pos = 1
    while True:
        temp = current
        current = last + current
        last = temp
        modulo_seq.append(current %  m)
        pos += 1
        if modulo_seq[pos] == 1 and modulo_seq[pos-1] == 0:
            break

    period = pos-1
    # perform simple lookup from the repeated sequence
    return modulo_seq[n % (period)]

def fibonacci_sum_naive(n):
    if n <= 1:
        return n

    previous = 0
    current  = 1
    sum_last_digit = 1 

    for _ in range(n - 1):
        previous, current = current, (previous + current) % 10
        sum_last_digit = (sum_last_digit + current) % 10

    return sum_last_digit

def fibonacci_sum(n):
    return (get_fibonacci_huge(n+2, 10) - 1) % 10

if __name__ == '__main__':
    input = sys.stdin.read()
    n = int(input)
    print(fibonacci_sum(n))
