#Uses python3

import sys, threading
import collections
sys.setrecursionlimit(1000000000) # max depth of recursion
threading.stack_size(2**29)  # new thread will get stack of such size

def reach(adjacents, start, finish):

    reached = False
    explored = collections.defaultdict( lambda  : 0)

    def explore(vert, adjacents, explored, target):
        nonlocal reached
        if reached or explored[vert]:
            return
        if vert == target:
            reached = True
            return

        explored[vert] = True
        for adjacent in adjacents[vert]:
            explore(adjacent, adjacents, explored, target)

    explore(start, adjacents, explored, finish)

    return 1 if reached else 0

if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))
    x, y = data[2 * m:]
    adj = [[] for _ in range(n)]
    x, y = x - 1, y - 1
    for (a, b) in edges:
        adj[a - 1].append(b - 1)
        adj[b - 1].append(a - 1)
    print(reach(adj, x, y))
