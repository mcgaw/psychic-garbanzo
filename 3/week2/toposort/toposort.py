#Uses python3

import sys
import threading

sys.setrecursionlimit(1000000000) # max depth of recursion
threading.stack_size(2**29)  # new thread will get stack of such size

def dfs(adj, used, order, x):

    for node in adj[x]:
        if node not in used:
            continue
        dfs(adj, used, order, node)

    used.remove(x)
    order.append(x)

def toposort(adj):
    order = []
    used = set([x for x in range(len(adj))])
    while len(used) > 0:
        dfs(adj, used, order, next(iter(used)))
    return reversed(order)

if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))
    adj = [[] for _ in range(n)]
    for (a, b) in edges:
        adj[a - 1].append(b - 1)
    order = toposort(adj)
    for x in order:
        print(x + 1, end=' ')

