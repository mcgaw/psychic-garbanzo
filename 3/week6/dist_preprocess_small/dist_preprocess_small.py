#!/usr/bin/python3
import collections
import itertools
import sys
import math
import heapq
import datetime

INF = float('Inf')

def roundrobin(*iterables):
    "roundrobin('ABC', 'D', 'EF') --> A D E B F C"
    # Recipe credited to George Sakkis
    pending = len(iterables)
    nexts = itertools.cycle(iter(it).__next__ for it in iterables)
    while pending:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            pending -= 1
            nexts = itertools.cycle(itertools.islice(nexts, pending))

class PriorityQueue:
    """
    PriorityQueue uses a heapq (min heap) but allows nodes to be deleted from
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

    def add_node(self, node, weight):
        if not self.contents[node] is None:
            self.remove_node(node)

        item = [weight, next(self.count), node]
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
        self.q = PriorityQueue()

    def query(self, s, t, ignore=lambda n: False, max_distance=INF, max_hops=INF):
        self._clear()
        self.distances[s] = 0
        self.previous[s] = None

        self.q.add_node(s, 0)

        hops = 0
        while True:
            node = self.q.pop_min()

            if node is not None and ignore(node):
                continue

            if node is None or\
                self.distances[node] > max_distance or\
                hops > max_hops:
                break

            hops += 1
            yield node

            for idx, neighbour in enumerate(self.adjacents[node]):
                relaxed = self.distances[node] + self.costs[node][idx]
                if self.distances[neighbour] > relaxed:
                    self.distances[neighbour] = relaxed
                    self.previous[neighbour] = node
                    self.q.add_node(neighbour, relaxed)

        return -1 if self.distances[t] == math.inf else self.distances[t]

    def distance(self, n):
        """
        Return the calculated distance from the source
        node to the node t.
        This may be Inf in the case the node is not discovered.
        """
        return self.distances[n]


class BiDijkstra(object):

    def __init__(self, adjacents, costs):
        self.left = Dijkstra(adjacents[0], costs[0])
        self.right = Dijkstra(adjacents[1], costs[1])


    def query(self, s, t):
        traversed = set([])
        dist_estimate = INF

        left = self.left.query(s, t, ignore=lambda n: self.left.distance(n) > dist_estimate)
        right = self.right.query(t, s, ignore=lambda n: self.right.distance(n) > dist_estimate)

        for node in roundrobin(left, right):
            if node in traversed:
                dist_estimate = min(dist_estimate, self.left.distance(node) + self.right.distance(node))
            else:
                traversed.add(node)

        return -1 if dist_estimate == INF else dist_estimate


class DistanceCalculator:

    def __init__(self, n, adjacents, costs):

        self.n = n
        self.adjacents = adjacents
        self.cost = costs

        self.bi_dijk = BiDijkstra(adjacents, costs)
        self.dijk = Dijkstra(adjacents[0], costs[0])

    def preprocess(self):
        # Levels of nodes. Upper bound of shortest path to
        # this node.
        self.level = [0] * self.n

        # Order the nodes were processed. Not all nodes
        # are contracted.
        self.order = [-INF] * self.n

        self.contracted = [False] * self.n

        # Overall importance of nodes. Minus infinity
        # ensures that importances of all nodes are
        # caluculated initially.
        self.rank = [-INF] * self.n
 
        nodes = PriorityQueue()
        for node in range(self.n):
            nodes.add_node(node, self.rank[node])

        order = 0
        shorted_paths = 0
        node = nodes.pop_min()
        while node is not None:

            importance, shortcuts = self.shortcut(node)
            self.rank[node] = importance

            # Check if the importance is low enough to contract it
            # now by comparing with next node in q (ostensibly the
            # least important other node)
            next_node = nodes.pop_min()

            if next_node is None or importance <= self.rank[next_node]:
                order += 1
                self.order[node] = order
                self.contracted[node] = True
                if len(shortcuts) > 0:
                    for sc in shortcuts:
                        shorted_paths += 1
                        #print('shorting {0} to {1} for node {2}'.format(sc[0]+1, sc[1]+1, node+1))
                        # update levels for neighbours of node.
                        self.level[sc[0]] = max(self.level[sc[0]], self.level[node]+1)
                        self.level[sc[1]] = max(self.level[sc[1]], self.level[node]+1)
                        self.add_arc(*sc)
            else:
                # There are nodes of lesser importance waiting to
                # be contracted.
                nodes.add_node(node, importance)

            if next_node is None:
                break

            nodes.add_node(next_node, self.rank[next_node])
            node = nodes.pop_min()

        #print('shorted paths: ', shorted_paths)
        self.remove_edges(0)
        self.remove_edges(1)


    def remove_edges(self, left_right):
        for node, neighbours in enumerate(self.adjacents[left_right]):
            neighbours_ = neighbours.copy()
            costs_ = self.cost[left_right][node].copy()

            for i, neighbour in enumerate(neighbours):
                if self.order[neighbour] < self.order[node]:
                    #print('removing edge {0} -> {1}'.format(node, neighbour))
                    neighbours_[i] = None
                    costs_[i] = None
            self.adjacents[left_right][node] = list(filter(lambda n: n is not None, neighbours_))
            self.cost[left_right][node] = list(filter(lambda n: n is not None, costs_))


    def add_arc(self, u, v, c):

        def update(adj, cost, u, v, c):
            for i in range(len(adj[u])):
                if adj[u][i] == v:
                    cost[u][i] = min(cost[u][i], c)
                    return
            adj[u].append(v)
            cost[u].append(c)

        update(self.adjacents[0], self.cost[0], u, v, c)
        update(self.adjacents[1], self.cost[1], v, u, c)


    def shortcut(self, v):
        """
        Look at each path through node v and add a shortcut
        (contract) if appropriate. eg If path u -> v -> w
        with distance d has no witness path with a
        smaller distance then add edge u -> w with distance d.
        Finally, calculate an importance heuristic for this node.
        """

        MAX_HOPS = 2
        shortcuts = []
        source_neighbours = list(filter(lambda n: not self.contracted[n], self.adjacents[1][v]))
        dest_neighbours = list(filter(lambda n: not self.contracted[n], self.adjacents[0][v]))

        for s in source_neighbours:
            if len(dest_neighbours) == 0:
                break

            def dist(s, v, t):
                s_v = self.cost[0][s][self.adjacents[0][s].index(v)]
                v_t = self.cost[1][t][self.adjacents[1][t].index(v)]
                return s_v + v_t

            max_dist = -INF
            for pair in itertools.product([s], dest_neighbours):
                s = pair[0]
                t = pair[1]
                max_dist = max(dist(s, v, t), max_dist)

            # Use v as target, will never be reached due to presence
            # in ignore function. Also need to ignore any nodes that
            # have already been contracted.
            traverse = self.dijk.query(s, v, ignore=lambda n: n == v or self.contracted[n],
                                       max_distance=max_dist, max_hops=MAX_HOPS)

            # Destination neighbours that have witness paths.
            witnesses = []
            while True:
                try:
                    node = next(traverse)
                except StopIteration:
                    for n in filter(lambda n: n not in witnesses, dest_neighbours):
                        #print('contracting node {0} found a required shortcut {1}->{2}'.format(v+1, s+1, n+1))
                        shortcuts.append((s, n, dist(s, v, n)))
                    break
                if node in dest_neighbours:
                    # Only add short cut if the path found using Dijkstra
                    # is not a witness path.
                    if self.dijk.distance(node) <= dist(s, v, node):
                        witnesses.append(node)

        # Compute the node importance.
        shortcut_count = len(shortcuts)
        contracted_neighbors = 0
        for neighbour in dest_neighbours + source_neighbours:
            if self.contracted[neighbour]:
                contracted_neighbors += 1
        shortcut_cover = 0
        level = self.level[v]
        importance = (shortcut_count - len(self.adjacents[1][v]))\
                      + contracted_neighbors + shortcut_cover + level
        return importance, shortcuts

    def query(self, s, t):
        return self.bi_dijk.query(s, t)


def readl():
    return map(int, sys.stdin.readline().split())

def process():
    n,m = readl()
    adj = [[[] for _ in range(n)], [[] for _ in range(n)]]
    cost = [[[] for _ in range(n)], [[] for _ in range(n)]]

    for e in range(m):
        u,v,c = readl()
        adj[0][u-1].append(v-1)
        cost[0][u-1].append(c)
        adj[1][v-1].append(u-1)
        cost[1][v-1].append(c)


    ch = DistanceCalculator(n, adj, cost)
    for arg in sys.argv:
        if 'no-preprocess' in arg:
            break
    else:
        ch.preprocess()

    print("Ready")
    sys.stdout.flush()
    t, = readl()
    for i in range(t):
        s, t = readl()
        start = datetime.datetime.now()
        print(ch.query(s-1, t-1))
        end = datetime.datetime.now()
        #print(end-start)

if __name__ == '__main__':
    process()

