#Uses python3

import sys
import collections

def vertices(component):
    s = set()
    for (vert1, vert2, _) in component:
        if vert1 not in s:
            s.add(vert1)
            yield vert1
        if vert2 not in s:
            s.add(vert2)
            yield vert2

def shortest_paths(adjacents, costs, s):
    # edges list [(node, adj_node, weight)]
    edges = []
    for n in range(0, len(adjacents)):
        num_edges = len(adjacents[n])
        edges += zip([n]*num_edges, adjacents[n], costs[n])

    distances = [float('Inf')] * len(adjacents)

    reverse_adjacents = [[] for n in range(0, len(adjacents))]
    for node, immediate_adjs in enumerate(adjacents):
        for adj in immediate_adjs:
            reverse_adjacents[adj].append(node)

    def update_distances(component):
        updates = set([])
        for (node, adj_node, cost) in component:
            if distances[node] + cost < distances[adj_node]:
                distances[adj_node] = distances[node] + cost
                updates.add(adj_node)
        return updates

    def reachable(s):
        q = collections.deque()
        layers = [-1] * len(reverse_adjacents)
        layers[s] = -1

        q.appendleft(s)
        while len(q) > 0:
            current = q.pop()
            for adjacent in reverse_adjacents[current]:
                if layers[adjacent] != -1:
                    continue
                layers[adjacent] = current
                q.appendleft(adjacent)

        return set([node for node, parent in enumerate(layers) if parent != -1])


    # filter out edges definitely not in this component
    component = list(filter(lambda x: distances[x[0]] == float('Inf')\
        and distances[x[1]] == float('Inf'), edges))

    distances[s] = 0

    # bellman-ford on this component
    nodes = set((vertices(component)))
    # edge case where s is isoloated node
    nodes.add(s)

    for n in range(0, 1 + len(nodes)):
        updated_nodes = update_distances(component)
        if len(updated_nodes) == 0:
            return ([node for node in nodes if distances[node] != float('Inf')], set([]), distances)
    else:
        # negative cycle deteced, need to find nodes that can reach it.
        component = [node for node in nodes if distances[node] != float('Inf')]
        # presumption of one negative cycle?
        cycle_node = updated_nodes.pop()
        reach_cycle = set([])
        for node in component:
            if cycle_node in reachable(node):
                reach_cycle.add(node)
        return (component, reach_cycle, distances)


def optimum_exchange(adjacents, costs, source):
    sp = shortest_paths(adjacents, costs, source)
    (component, cycle, distances) = sp

    for node in range(0, len(adjacents)):
        if node in cycle:
            print('-')
        elif not node in component:
            print('*')
        else:
            print(distances[node])


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
    s = data[0]
    s -= 1
    optimum_exchange(adj, cost, s)
