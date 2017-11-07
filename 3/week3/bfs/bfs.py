#Uses python3

import sys
import collections

def distance_layers(adjacents, s):

    q = collections.deque()
    layers = [-1] * len(adjacents)
    layers[s] = None

    q.appendleft(s)
    while len(q) > 0:
        current = q.pop()
        for adjacent in adjacents[current]:
            if layers[adjacent] != -1:
                continue
            layers[adjacent] = current
            q.appendleft(adjacent)

    return layers

def distance(adjacents, s, t):

    layers = distance_layers(adjacents, s)

    if layers[t] == -1:
        return -1

    dist = 0
    node = t
    while node != s:
        dist += 1
        node = layers[node]

    return dist

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
    s, t = data[2 * m] - 1, data[2 * m + 1] - 1
    print(distance(adj, s, t))
