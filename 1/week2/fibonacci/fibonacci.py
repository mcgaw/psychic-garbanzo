# Uses python3
from datetime import datetime

def calc_fib(n):
    if n <= 1:
        return n
    return calc_fib(n - 1) + calc_fib(n - 2)

def calc_fib_fast(n):
    first = 1 
    second =0 

    if n == 0:
        return 0
    if n == 1:
        return 1

    for _ in range(1, n):
        temp = first
        first = first + second
        second = temp

    return first


n = int(input())
start = datetime.now()
print(calc_fib_fast(n))
#print('{0} seconds'.format(datetime.now() - start))
