#Uses python3

import sys
import threading

sys.setrecursionlimit(1000000000) # max depth of recursion
threading.stack_size(2**29)  # new thread will get stack of such size

def reverse_graph(adjacents):
    """ Reverse the direction of the vertices
    in the directed graph.
    """
    reverse = [[] for _ in range(len(adjacents))]

    for idx, nodes in enumerate(adjacents):
        for node in nodes:
            reverse[node].append(idx)
    return reverse

def post_orders(adjacents):
    """
    Order the nodes of the graph according to their
    post order. Uses (possibly repeated) Depth First Search on
    the graph.
    """

    def dfs(node, order, traversed):
        traversed.add(node)
        for adj in adjacents[node]:
            if adj in traversed:
                continue
            dfs(adj, order, traversed)
        order.append(node)

    post_order = []
    vertices = set([node for node in range(len(adjacents))])
    while True:
        order = []

        dfs(vertices.pop(), order, set(post_order))

        vertices = vertices.difference(order)
        post_order = post_order + order

        if len(post_order) == len(adjacents):
            break

    assert len(post_order) == len(adjacents)

    return post_order


def connected_component(adjacents, node, ignore):
    """ Explore the graph starting at node stopping
    at dead ends and avoiding both cycles and nodes
    in the ignore list.
    """

    connected = []
    def explore(node, connected):
        connected.append(node)
        for adj in adjacents[node]:
            if adj in ignore or adj in connected:
                continue
            explore(adj, connected)

    explore(node, connected)
    return connected

def number_cc(adj):
    reverse = reverse_graph(adj)
    orders = post_orders(reverse)

    order_pointer = len(orders) - 1
    num_cc = 0
    found = set([])
    while order_pointer >= 0:
        if orders[order_pointer] in found:
            order_pointer -= 1
            continue

        found = found.union(connected_component(adj, orders[order_pointer], found))
        num_cc += 1

    assert len(found) == len(adj)
    return num_cc

if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))
    adj = [[] for _ in range(n)]
    for (a, b) in edges:
        adj[a - 1].append(b - 1)
    print(number_cc(adj))
