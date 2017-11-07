# python3
import sys
import threading
import collections

sys.setrecursionlimit(10**6) # max depth of recursion
threading.stack_size(2**26)  # new thread will get stack of such size

import itertools

def conn_comp(edges):
    """
    Tarjan's algorithm for connected
    components.
    """

    vertices = set(v for v in itertools.chain(*edges))
    indices = dict((v, -1) for v in vertices)
    lowlinks = indices.copy()
    ccs = []

    index = 0
    stack = []
    for v in vertices:
        if indices[v] < 0:
            strong_connect(v, edges, indices, lowlinks, ccs, index, stack)

    return ccs

def strong_connect(vertex, edges, indices, lowlinks, ccs, index, stack):

    indices[vertex] = index
    lowlinks[vertex] = index
    index += 1
    stack.append(vertex)

    for v, w in [e for e in edges if e[0] == vertex]:
        if indices[w] < 0:
            strong_connect(w, edges, indices, lowlinks, ccs, index, stack)
            lowlinks[v] = min(lowlinks[v], lowlinks[w])
        elif w in stack:
            lowlinks[v] = min(lowlinks[v], indices[w])

    if indices[vertex] == lowlinks[vertex]:
        ccs.append([])
        while stack[-1] != vertex:
            ccs[-1].append(stack.pop())
        ccs[-1].append(stack.pop())


class OrderedSet(collections.MutableSet):

    def __init__(self, iterable=None):
        self.end = end = [] 
        end += [None, end, end]         # sentinel node for doubly linked list
        self.map = {}                   # key --> [key, prev, next]
        if iterable is not None:
            self |= iterable

    def __len__(self):
        return len(self.map)

    def __contains__(self, key):
        return key in self.map

    def add(self, key):
        if key not in self.map:
            end = self.end
            curr = end[1]
            curr[2] = end[1] = self.map[key] = [key, curr, end]

    def discard(self, key):
        if key in self.map:        
            key, prev, next = self.map.pop(key)
            prev[2] = next
            next[1] = prev

    def __iter__(self):
        end = self.end
        curr = end[2]
        while curr is not end:
            yield curr[0]
            curr = curr[2]

    def __reversed__(self):
        end = self.end
        curr = end[1]
        while curr is not end:
            yield curr[0]
            curr = curr[1]

    def pop(self, last=True):
        if not self:
            raise KeyError('set is empty')
        key = self.end[1][0] if last else self.end[2][0]
        self.discard(key)
        return key

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self))

    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and list(self) == list(other)
        return set(self) == set(other)


def post_orders(adjacents):
    """
    Order the nodes of the graph according to their
    post order. Uses (possibly repeated) Depth First Search on
    the graph.
    """

    vertices = set([node for node in range(len(adjacents))])

    def dfs(node, order, traversed):
        q = collections.deque([node])
        while len(q) > 0:
            node = q.pop()
            traversed.add(node)
            moving_up = True
            to_add = []
            for adj in adjacents[node]:
                if adj in traversed:
                    continue
                moving_up = False
                to_add.append(adj)
            if moving_up:
                order.add(node)
                if node in vertices:
                    vertices.remove(node)
            else:
                q.append(node)
                for n in to_add:
                    q.append(n)

    post_order = OrderedSet([])
    traversed = set([])
    vertices = set([node for node in range(len(adjacents))])
    while True:
        dfs(vertices.pop(), post_order, traversed)
        if len(post_order) == len(adjacents):
            break

    assert len(post_order) == len(adjacents)
    return list(post_order)


def post_orders_(adjacents):
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
        if node in vertices:
            vertices.remove(node)
        order.add(node)

    post_order = OrderedSet([])
    traversed = set([])
    vertices = set([node for node in range(len(adjacents))])

    while True:
        dfs(vertices.pop(), post_order, traversed)
        if len(post_order) == len(adjacents):
            break

    assert len(post_order) == len(adjacents)

    return list(post_order)

def connected_component_(adjacents, node, found):
    """ 
    Explore the graph starting at node stopping
    at dead ends and avoiding both cycles and nodes
    in the ignore list.
    """

    connected = set([])
    def dfs(node, connected):
        connected.add(node)
        found.add(node)
        for adj in adjacents[node]:
            if adj in found or adj in connected:
                continue
            dfs(adj, connected)

    dfs(node, connected)
    return connected

def connected_component(adjacents, node, found):
    """ 
    Explore the graph starting at node stopping
    at dead ends and avoiding both cycles and nodes
    in the ignore list.
    While exploring build up the part of the solution belonging to
    this connected component while also checking that there is no
    duplicates of any litteral, indicating no solution.
    """

    connected = set([])
    q = collections.deque([node])
    found_litterals = set([])

    while len(q) > 0:
        node = q.pop()

        # Possible a node is added twice before
        # having a chance to be processed.
        if node in connected:
            continue
        connected.add(node)
        found.add(node)

        for adj in adjacents[node]:
            if adj in found or adj in connected:
                continue
            q.append(adj)

    return connected

def analyse_connected_components_(n, adjacents, reverse, var_map):

    # Ensure topological ordering.
    order = post_orders_(reverse)
    #print('orders: {0}'.format(orders))

    order_pointer = len(order) - 1
    found = set([])
    ccs = []
    while order_pointer >= 0:
        if order[order_pointer] in found:
            order_pointer -= 1
            continue

        ccs.append(connected_component_(adjacents, order[order_pointer], found))

    assert len(found) == len(adjacents), 'found {0} nodes, but {1} were specified'.format(len(found), n)
    return ccs

def analyse_connected_components(n, adjacents, reverse, var_map):

    # Ensure topological ordering.
    order = post_orders_(reverse)
    #print('orders: {0}'.format(orders))

    order_pointer = len(order) - 1
    found = set([])
    ccs = []
    while order_pointer >= 0:
        if order[order_pointer] in found:
            order_pointer -= 1
            continue

        ccs.append(connected_component(adjacents, order[order_pointer], found))

    assert len(found) == len(adjacents), 'found {0} nodes, but {1} were specified'.format(len(found), n)
    return ccs

def build_implication_graph(n, clauses):

    edges = []
    var_dict =  {}
    node_dict = {}
    node_num = 0
    adjacents = [[] for _ in range(2*n)]
    reversed_adjs = [[] for _ in range(2*n)]

    for clause in clauses:
        #if len(clause) == 1:
        #    assert False, 'should be two terms in the clause'

        left = clause[0]
        right = clause[1]
        for term in [left, right]:
            if not term in node_dict:
                var_dict[node_num] = term
                node_dict[term] = node_num
                node_num += 1
            if not -term in node_dict:
                var_dict[node_num] = -term
                node_dict[-term] = node_num
                node_num += 1

        adjacents[node_dict[-left]].append(node_dict[right])
        reversed_adjs[node_dict[right]].append(node_dict[-left])
        #edges.append((node_dict[-left], node_dict[right]))

        adjacents[node_dict[-right]].append(node_dict[left])
        reversed_adjs[node_dict[left]].append(node_dict[-right])
        #edges.append((node_dict[-right], node_dict[left]))

    return edges, adjacents[:node_num], reversed_adjs[:node_num], node_dict, var_dict

def is_satisfiable(n, m, clauses):
    edges, implication_g, reversed_imp_g, node_map, var_map = build_implication_graph(n, clauses)

    ccs = analyse_connected_components_(n, implication_g, reversed_imp_g, var_map)
    #ccs = analyse_connected_components(n, implication_g, reversed_imp_g, var_map)

    print(ccs)

    result = collections.defaultdict(lambda: None)
    for cc in ccs:
        cc_vars = set([])
        for node in cc:

            # Check valid solution.
            litteral = var_map[node]
            if abs(litteral) in cc_vars:
                return None
            else:
                cc_vars.add(abs(litteral))

            if result[abs(litteral)] is None:
                if litteral < 0:
                    result[abs(litteral)] = 0 
                else:
                    result[abs(litteral)] = 1

    return result

def circuit_design():
    n, m = map(int, input().split())
    clauses = [ list(map(int, input().split())) for i in range(m) ]

    result = is_satisfiable(n, m, clauses)

    if result is None:
        print("UNSATISFIABLE")
    else:
        print("SATISFIABLE");
        print(" ".join(str(i if result[i] else -i) for i in range(1, n+1)))


if __name__ == '__main__':
    threading.Thread(target=circuit_design).start()