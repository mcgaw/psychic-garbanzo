# python3
import collections

class Edge:

    def __init__(self, u, v, capacity):
        self.u = u
        self.v = v
        self.capacity = capacity
        self.flow = 0

    def __repr__(self):
        return '<u: {0} v: {1} cap: {2} flow: {3}>'.format(self.u, self.v, self.capacity, self.flow)
# This class implements a bit unusual scheme for storing edges of the graph,
# in order to retrieve the backward edge for a given edge quickly.
class FlowGraph:

    def __init__(self, n):
        # List of all - forward and backward - edges
        self.edges = []
        # These adjacency lists store only indices of edges in the edges list
        self.graph = [[] for _ in range(n)]

    def add_edge(self, from_, to, capacity):
        # Note that we first append a forward edge and then a backward edge,
        # so all forward edges are stored at even indices (starting from 0),
        # whereas backward edges are stored at odd indices.
        forward_edge = Edge(from_, to, capacity)
        backward_edge = Edge(to, from_, 0)
        self.graph[from_].append(len(self.edges))
        self.edges.append(forward_edge)
        self.graph[to].append(len(self.edges))
        self.edges.append(backward_edge)

    def size(self):
        return len(self.graph)

    def get_ids(self, from_):
        return self.graph[from_]

    def get_edge(self, id):
        return self.edges[id]

    def add_flow(self, id, flow):
        # To get a backward edge for a true forward edge (i.e id is even), we should get id + 1
        # due to the described above scheme. On the other hand, when we have to get a "backward"
        # edge for a backward edge (i.e. get a forward edge for backward - id is odd), id - 1
        # should be taken.
        #
        # It turns out that id ^ 1 works for both cases. Think this through!
        self.edges[id].flow += flow
        self.edges[id ^ 1].flow -= flow

    def find_edge(self, from_, to):
        for e in self.graph[from_]:
            edge = self.edges[e]
            if edge.v == to:
                return edge
        
def find_augement_path(graph, from_, to):
    q = collections.deque()
    visited = [False] * len(graph.graph)

    augmented_path = None
    q.appendleft((from_, []))
    while len(q) > 0:
        (vert, path) = q.pop()
        if vert == to:
            augmented_path = path
            break

        if visited[vert]:
            continue
        visited[vert] = True

        for idx in graph.graph[vert]:
            edge = graph.edges[idx]
            # edge in the flow that is maxed out
            if edge.u == edge.v:
                continue
            if edge.capacity == edge.flow  and edge.capacity != 0: 
                continue
            # check for 'reverse edge' with no flow to reverse
            if edge.capacity == 0 and graph.edges[idx-1].flow == 0:
                continue
            node = (edge.v, list(path))
            node[1].append(idx)
            q.appendleft(node)

    return  augmented_path

def augment_flow(graph, path):
    max_potential = float('Inf')
    for idx in path:
        edge = graph.edges[idx]
        if edge.capacity == 0:
            # 'backward' flow
            potential = graph.edges[idx-1].flow
        else:
            potential = edge.capacity - edge.flow
        if potential < max_potential:
            max_potential = potential

    return max_potential

def update_augmented(graph, path, flow):
    for idx in path:
        edge = graph.edges[idx]
        if edge.capacity == 0:
            # 'reversing' the flow
            forward_edge = graph.edges[idx-1]
            forward_edge.flow = forward_edge.flow - flow
        else:
            edge.flow = edge.flow + flow
            backward_edge = graph.edges[idx+1]
            backward_edge.flow = edge.flow

def max_flow(graph, from_, to):
    while True:
        path = find_augement_path(graph, from_, to)
        #print('path: '+str(path))
        if not path:
            break
        flow = augment_flow(graph, path)
        #print('flow: '+str(flow))
        assert flow != 0
        update_augmented(graph, path, flow)

    flow = 0
    for idx in graph.graph[from_]:
        flow += graph.edges[idx].flow

    return flow

def airline_crews(num_flight, num_crews, adj_matrix):
    # convert to format required for graph
    num_nodes = 2 + n + m
    graph = FlowGraph(num_nodes)
    crew_offset = 1 + n
    sink_node = num_nodes - 1

    for idx, row in enumerate(adj_matrix):
        flight_node = 1 + idx
        graph.add_edge(0, flight_node, 1)
        for idx, edge in enumerate(row):
            crew_node = idx + crew_offset
            if edge == 0:
                continue
            # don't add duplicate edges
            if graph.find_edge(crew_node, sink_node) is None:
                graph.add_edge(crew_node, sink_node, 1)
            if graph.find_edge(flight_node, crew_node) is None:
                graph.add_edge(flight_node, crew_node, 1)

    # calculate max flow in graph
    flow = max_flow(graph, 0, sink_node)   

    # pull out the 'pairings' of flight to crew, indicated by a
    # flow on an edge between flight and crew.
    pairings = []
    for node in range(1, 1 + n):
        for edge_idx in graph.graph[node]:
            edge = graph.edges[edge_idx]
            if edge.flow == 1:
                pairings.append(edge.v - crew_offset + 1)
                break
        else:
            pairings.append(-1)

    return pairings


if __name__ == '__main__':
    n, m = map(int, input().split())
    adj_matrix = [list(map(int, input().split())) for i in range(n)]
    pairings = airline_crews(n, m, adj_matrix)
    print(' '.join([str(pairing) for pairing in pairings]))
