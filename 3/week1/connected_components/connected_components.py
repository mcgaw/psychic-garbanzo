#Uses python3

import sys, threading
import collections
sys.setrecursionlimit(1000000000) # max depth of recursion
threading.stack_size(2**29)  # new thread will get stack of such size

def number_of_components(adjacents):

    # allow exhaustive search of components by keeping
    # track of remaining vertices.
    vertices = set()
    for vert in range(0, len(adjacents)):
        vertices.add(vert)

    def explore(vert, adjacents, explored):
        nonlocal vertices
        # if already discarded does nothing.
        vertices.discard(vert)

        if explored[vert]:
            return
        explored[vert] = True
        for adjacent in adjacents[vert]:
            explore(adjacent, adjacents, explored)

    num_components = 0
    while len(vertices) != 0:
        explore(vertices.pop(), adjacents,
                collections.defaultdict(lambda: False))
        num_components += 1

    return num_components

if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))
    adj = [[] for _ in range(n)]
    for (a, b) in edges:
        adj[a - 1].append(b - 1)
        adj[b - 1].append(a - 1)
    print(number_of_components(adj))
