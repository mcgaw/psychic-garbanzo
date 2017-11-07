#Uses python3

import sys
import threading

sys.setrecursionlimit(1000000000) # max depth of recursion
threading.stack_size(2**29)  # new thread will get stack of such size

def acyclic(adjacents):
    num_vertices = len(adjacents)
    order = []
    def find_sink(node, visited):
        if visited.issuperset(set([node])):
            return -1
        visited.add(node)

        for adj in adjacents[node]:
            if adjacents[adj] is None:
                continue
            next_node = adj
            break
        else:
            next_node = None

        if next_node is None:
            # case where unable to find an adjacent, ie a sink
            return node
        else:
            return find_sink(next_node, visited)

    vertices = set([vert for vert in range(0, len(adjacents))])
    while len(order) < num_vertices:
        sink = find_sink(next(iter(vertices)), set([]))
        adjacents[sink] = None
        if sink == -1:
            break
        else:
            vertices.remove(sink)
        order.append(sink)

    return 1 if len(order) < num_vertices else 0

if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))
    adj = [[] for _ in range(n)]
    for (a, b) in edges:
        adj[a - 1].append(b - 1)
    print(acyclic(adj))
