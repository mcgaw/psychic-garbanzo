#Uses python3

import sys

def vertices(component):
    s = set()
    for (vert, _, _) in component:
        if vert not in s:
            s.add(vert)
            yield vert


def negative_cycle(adjacents, costs):
    # edges list [(node, adj_node, weight)]
    edges = []
    for n in range(0, len(adjacents)):
        num_edges = len(adjacents[n])
        edges += zip([n]*num_edges, adjacents[n], costs[n])

    distances = [float('Inf')] * len(adjacents)

    def update_distances(component):
        update = False
        for (node, adj_node, cost) in component:
            if distances[node] + cost < distances[adj_node]:
                distances[adj_node] = distances[node] + cost
                update = True
        return update


    cycle = False
    component = edges
    while float('Inf') in distances and not cycle:
        # filter out edges definitely not in this component
        component = list(filter(lambda x: distances[x[0]] == float('Inf')\
            and distances[x[1]] == float('Inf'), edges))

        # min of 1 edges to be a negative cycle
        if len(component) == 0:
            break

        # arbitrary starting node within the component.
        distances[component[0][0]] = 0

        # bellman-ford on this component
        cycle = False
        for n in range(0, 1 + len(list(vertices(component)))):
            if not update_distances(component):
                break
        else:
            cycle = True

    return 1 if cycle else 0


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
    print(negative_cycle(adj, cost))
