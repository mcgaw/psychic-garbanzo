#!/usr/bin/python3

import sys
import heapq
import math
import itertools
import collections

math.inf = float('Inf')

# priority node queue
class NodeQueue:
    """
    NodeQueue uses a heapq but allows nodes to be deleted from
    the queue without any costly reordering.
    This is achieved by maintaining a seperate list of nodes,
    which items in the heapq then refer to. Removing a node
    inserts a magic string into this array, which is checked for
    when popping the heapq.
    """

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

    def size(self):
        return len(self.pq)

    def pop_min(self):
        while self.pq:
            item = heapq.heappop(self.pq)
            self.contents[item[0]] = None
            if item[2] != "REMOVED":
                return item[2]
        return None


class Dijkstra:

    def __init__(self, adjacents, costs):
        self.previous = [-1] * len(adjacents)
        self.adjacents = adjacents
        self.costs = costs
        self.distances = None
        self.q = None

    def _clear(self):
        self.distances = [math.inf] * len(self.adjacents)
        self.q = NodeQueue()

    def query(self, s, t, max_distance=-1, max_hops=-1):
        self._clear()

        self.distances[s] = 0
        self.previous[s] = None

        self.q.add_node(s, 0)

        while True:
            node = self.q.pop_min()
            if node is None:
                break

            yield node

            for idx, neighbour in enumerate(self.adjacents[node]):
                relaxed = self.distances[node] + self.costs[node][idx]
                if self.distances[neighbour] > relaxed:
                    self.distances[neighbour] = relaxed
                    self.previous[neighbour] = node
                    self.q.add_node(neighbour, relaxed)

        return -1 if self.distances[t] == math.inf else self.distances[t]

    def distance(self, t):
        """
        Return the calculated distance from the source
        node to the node t.
        This may be Inf in the case the node is not discovered.
        """
        return self.distances[t]


class BiDijkstra(object):

    def __init__(self, adjacents, costs):
        self.left = Dijkstra(adjacents[0], costs[0])
        self.right = Dijkstra(adjacents[1], costs[1])


    def query(self, s, t):
        if s == t:
            return 0
        traversed = set([])
        min_dist = math.inf
        for nodes in zip(self.left.query(s, t), self.right.query(t, s)):
            if nodes[0] in traversed or\
                nodes[1] in traversed:
                break
            traversed.add(nodes[0])
            traversed.add(nodes[1])

        for node in traversed:
            dist = self.left.distance(node) + self.right.distance(node)
            if dist < min_dist:
                min_dist = dist

        return -1 if min_dist == math.inf else min_dist

def readl():
    return map(int, sys.stdin.readline().split())


if __name__ == '__main__':
    n,m = readl()
    adj = [[[] for _ in range(n)], [[] for _ in range(n)]]
    cost = [[[] for _ in range(n)], [[] for _ in range(n)]]
    for e in range(m):
        u,v,c = readl()
        adj[0][u-1].append(v-1)
        cost[0][u-1].append(c)
        adj[1][v-1].append(u-1)
        cost[1][v-1].append(c)
    t, = readl()
    bi_dijk = BiDijkstra(adj, cost)
    for i in range(t):
        s, t = readl()
        print(bi_dijk.query(s-1, t-1))
