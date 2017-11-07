#Uses python3

import sys
import heapq
import math
import itertools
import collections

math.inf = float('Inf')

# priority node queue

count = itertools.count()
pq = []
contents = collections.defaultdict(lambda : None)

def add_node(node, relaxed_weight):
    if not contents[node] is None:
        remove_node(node)

    item = [relaxed_weight, next(count), node]
    contents[node] = item
    heapq.heappush(pq, item)

def remove_node(node):
    contents[node][2] = "REMOVED"
    contents[node] = None

def queue_size():
    return len(pq)

def pop_min():
    while pq:
        item = heapq.heappop(pq)
        contents[item[0]] = None
        if item[2] != "REMOVED":
            return item[2]
    return None

# dijkstra's algo

def distance(adjacents, costs, s, t):
    distances = [math.inf] * len(adj)
    distances[s] = 0
    previous = [-1] * len(adj)
    previous[s] = None

    add_node(s, 0)

    while True:
        node = pop_min()
        if node is None:
            break

        for idx, neighbour in enumerate(adjacents[node]):
            relaxed = distances[node] + costs[node][idx]
            if distances[neighbour] > relaxed:
                distances[neighbour] = relaxed
                previous[neighbour] = node
                add_node(neighbour, relaxed)

    return -1 if distances[t] == math.inf else distances[t]


if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(zip(data[0:(3 * m):3], data[1:(3 * m):3]), data[2:(3 * m):3]))
    data = data[3 * m:]
    adj = [[] for _ in range(n)]
    cost = [[] for _ in range(n)]
    for ((a, b), w) in edges:
        adj[a - 1].append(b - 1)
        cost[a - 1].append(w)
    s, t = data[0] - 1, data[1] - 1
    print(distance(adj, cost, s, t))
