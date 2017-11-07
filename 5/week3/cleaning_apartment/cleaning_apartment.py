# python3

import itertools

def calculate_sat_problem(n, m, edges):

    def print_equations(eqs):
        for eq in eqs:
            print('{0} 0'.format(' '.join([str(var) for var in eq])))

    def one_of(vars):
        eqs = []
        eqs.append(vars)
        for comb in itertools.combinations(vars, 2):
            eqs.append([-comb[0], -comb[1]])
        return eqs

    def next_var(var):
        while True:
            var += 1
            yield var

    var_seq = next_var(0)
    eqs = []

    # Each node must have a position in the path.
    node_positions = {}
    for node in range(1, n+1):
        position_vars = [next(var_seq) for _ in range(1, n+1)]
        node_positions[node] = position_vars
        eqs += one_of(position_vars)

    # Each position is used by only one node.
    for idx, position in enumerate(range(1, n+1)):
        start = idx + 1
        eqs += one_of([position] +\
            [other for other in range(start, start + (n*n), n) if other != position])

    # Each node must have one predecessor and successor node.
    # Nodes with one edge are special cases. They can be end
    # nodes.
    node_edges = {}
    for edge in edges:
        node_edges.setdefault(edge[0], []).append(edge)
        node_edges.setdefault(edge[1], []).append(edge)

    for node in range(1, n+1):
        if n == 1:
            break
        for idx, position in enumerate(node_positions[node]):
            if not node in node_edges:
                eqs.append([-position])
                continue

            #print('node {0} connected nodes {1}'.format(node, connected_nodes))
            if idx != len(node_positions[node])-1:
                # If the node has position, then there should be
                # a neighbour node with position + 1
                connected_nodes = [edge[1] for edge in node_edges[node] if edge[0] == node]
                connected_nodes += [edge[0] for edge in node_edges[node] if edge[1] == node]
                successor = (idx + 1) % n
                eqs.append([-position] + [node_positions[node][successor] for node in connected_nodes])
            

    #print('p cnf {1} {0}'.format(len(eqs), next(var_seq) - 1,))
    print('{0} {1}'.format(len(eqs), next(var_seq) - 1,))
    print_equations(eqs)

n, m = map(int, input().split())
edges = [ list(map(int, input().split())) for i in range(m) ]
calculate_sat_problem(n, m, edges)
