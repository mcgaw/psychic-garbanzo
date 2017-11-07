import numpy as np
from scipy.optimize import linprog
from sys import stdin

m, n = list(map(int, stdin.readline().split()))
a = []
for i in range(m):
    a += [list(map(int, stdin.readline().split()))]
b = list(map(int, stdin.readline().split()))
c = list(map(int, stdin.readline().split()))


# Try to reduce "false positive" results, where linprog() returns an answer that is
# not correct. Use the idea for "a slightly modified procedure" described at:
# https://www.coursera.org/learn/advanced-algorithms-and-complexity/discussions/all/threads/XBz2qmB5EeaqYRKO7-Ax0Q/replies/GdzNnHYvEealrxI7520HyQ/comments/AAAGGXbSEeaF8w5uWHT1BQ
def print_intermediate(xk, **kwargs):
    print(kwargs['phase'])
    print(kwargs['tableau'])

linprog_res = linprog(np.negative(c), callback=print_intermediate, A_ub=a, b_ub=b, options={'tol': 1e-4})
if linprog_res.status != 2:
    prev_linprog_res = linprog_res
    tolerances = [1e-5, 1e-6, 1e-7, 1e-8, 1e-9, 1e-10, 1e-11, 1e-12, 1e-13]
    for tol in tolerances:
      linprog_res = linprog(np.negative(c), A_ub=a, b_ub=b, options={'tol': tol})
      if linprog_res.status == 2:
        linprog_res = prev_linprog_res
        break
      prev_linprog_res = linprog_res

if linprog_res.status == 3:
    print('Infinity')
elif linprog_res.status == 2:
    print('No solution')
elif linprog_res.status == 0:
    x_ref = linprog_res.x
    print('Bounded solution')
    print('x_ref =', ' '.join(list(map(lambda x: '%.18f' % float(x), x_ref))))