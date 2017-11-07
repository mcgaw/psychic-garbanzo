# python3
import itertools

def calculate_sat_problem(n, m, edges):

    # Num of variables is num of nodes times num
    # of freq. Each of the variables for a given
    # node will be limited to allow only one to
    # be true.
    num_vars = n * 3

    # 2 equations for each node to restrict each node
    # to one frequency.
    # And 3 equations for each edge constraint.
    num_equations = (n * 4) + (m * 3)

    print('{1} {0}'.format(num_vars, num_equations))

    node_vars = {} 
    var_count = 1

    def add_node(node):
        nonlocal var_count
        node_vars[node] = [var for var in range(var_count, var_count + 3)]
        var_count += 3
        # Node can be one of the 3 frequencies.
        print('{0} 0'.format(' '.join([str(var) for var in node_vars[node]])))
        for comb in itertools.combinations(node_vars[node], 2):
            print('{0} {1} 0'.format(-comb[0], -comb[1]))

    for node in range(1, n+1):
        add_node(node)

    for edge in edges:
        #if not edge[0] in node_vars:
        #    add_node(edge[0])
        #if not edge[1] in node_vars:
        #    add_node(edge[1])
        # Add edge restriction.
        for idx, node_var in enumerate(node_vars[edge[0]]):
            opposite = node_vars[edge[1]]
            opposite_vars = opposite[idx+1:] + opposite[0:idx]
            print('{0} {1} 0'\
                .format(str(-node_var), str(-opposite[idx])))
            continue
            print('{0} {1} 0'\
                .format(str(-node_var), ' '.join([str(var) for var in opposite_vars])))

n, m = map(int, input().split())
edges = [ list(map(int, input().split())) for i in range(m) ]
calculate_sat_problem(n, m, edges)
