#!/usr/bin/python3

import sys
import math
import heapq
import itertools
import collections

class NodeQueue:

    def __init__(self):
        self.count = itertools.count()
        self.pq = []
        self.contents = collections.defaultdict(lambda : None)

    def add_node(self, node, relaxed_weight):
        if not self.contents[node] is None:
            self.remove_node(node)

        item = [relaxed_weight, next(self.count), node]
        self.contents[node] = item
        heapq.heappush(self.pq, item)

    def remove_node(self, node):
        self.contents[node][2] = "REMOVED"
        self.contents[node] = None

    def __len__(self):
        return len(self.pq)

    def pop_min(self):
        while self.pq:
            item = heapq.heappop(self.pq)
            self.contents[item[0]] = None
            if item[2] != "REMOVED":
                return item[2]
        return None

class AStar:
    def __init__(self, n, adj, cost, x, y):
        self.n = n;
        self.adjacents = adj
        self.costs = cost
        self.inf = float('Inf')

        self.d = [self.inf]*n
        self.visited = [False]*n
        self.workset = []
        self.previous = [None]*n
        # Coordinates of the nodes
        self.x = x
        self.y = y

    def clear(self):
        for v in self.workset:
            self.previous[v] = None
            self.d[v] = self.inf
            self.visited[v] = False;
        del self.workset[0:len(self.workset)]

    def potential(self, node, target):
        # coordinate distance from node to target.
        return math.sqrt(math.pow(self.y[target] - self.y[node], 2) +
            math.pow(self.x[node] - self.x[target], 2))

    def visit(self, q, node, target):
        #print('visiting {0} on side {1}'.format(node+1, side))
        self.workset.append(node)
        self.visited[node] = True

        for idx, neighbour in enumerate(self.adjacents[node]):
            if self.visited[neighbour]:
                continue

            # relaxed distance includes a 'potential' which is a heuristic determining how
            # well the node is moving in the direction of the target.
            relaxed = self.d[node] + (self.costs[node][idx] +\
                self.potential(neighbour, target) - self.potential(node, target))
            if self.d[neighbour] > relaxed:
                self.workset.append(neighbour)
                self.d[neighbour] = relaxed
                self.previous[neighbour] = node
                q.add_node(neighbour, relaxed)

    def path(self, target):
        node = target
        path = []
        while node != None:
            path.append(node)
            node = self.previous[node]
        path = list(reversed(path))
        return path

    def visited_nodes(self):
        return [idx + 1 for idx, val in enumerate(self.visited) if val == True]

    def query(self, start, target):
        #print('adjacents {0}'.format(adj))
        #print('costs {0}'.format(cost))
        #print('calculating path from node {0} to node {1}'.format(start+1, target+1))
        self.clear()

        q = NodeQueue()
        self.previous[start] = None
        self.d[start] = 0
        q.add_node(start, 0)
        self.workset.append(start)

        while True:
            node = q.pop_min()
            if node is None:
                break
            if self.visited[node]:
                continue
            if node == target:
                path = self.path(target)
                #print('found target node {0}'.format(node+1))
                #print('visited {0}'.format([idx + 1 for idx, val in enumerate(self.visited) if val == True]))
                #print('path {0}'.format([p + 1 for p in path]))
                distance = 0
                current = path[0]
                for next_node in path[1:]:
                    distance += self.costs[current][self.adjacents[current].index(next_node)]
                    current = next_node
                return distance

            self.visit(q, node, target)

        return -1 

def readl():
    return map(int, sys.stdin.readline().split())

if __name__ == '__main__':
    n,m = readl()
    x = [0 for _ in range(n)]
    y = [0 for _ in range(n)]
    adj = [[] for _ in range(n)]
    cost = [[] for _ in range(n)]
    for i in range(n):
        a, b = readl()
        x[i] = a
        y[i] = b
    for e in range(m):
        u,v,c = readl()
        adj[u-1].append(v-1)
        cost[u-1].append(c)
    t, = readl()
    astar = AStar(n, adj, cost, x, y)
    for i in range(t):
        s, t = readl()
        print(astar.query(s-1, t-1))
