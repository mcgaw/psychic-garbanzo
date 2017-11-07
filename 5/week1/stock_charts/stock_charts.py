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

def create_graph(chart_matrix):
    n = len(chart_matrix)
    num_nodes = 2 + 2*n
    graph = FlowGraph(num_nodes)
    y_offset = 1 + n

    sink_node = num_nodes - 1
    # add edges from source to X set.
    for i in range(1, 1 + n):
        graph.add_edge(0, i, 1)

    for i, x_chart in enumerate(chart_matrix):
        # look for charts that can fit under this chart
        for j, y_chart in enumerate(chart_matrix):
            if j == i:
                continue
            lower = True
            for k, point in enumerate(y_chart):
                if point >= x_chart[k]:
                    lower = False
                    break
            if lower:
                graph.add_edge(1 + i, y_offset + j, 1)

    # add edges from the Y set to the sink
    for i in range(y_offset, y_offset + n):
        graph.add_edge(i, sink_node, 1)
    return graph

def min_charts(chart_matrix):
    #print(chart_matrix)
    graph = create_graph(chart_matrix) 
    n = len(chart_matrix)

    sink_node = len(graph.graph) - 1
    # calculate max flow in graph
    max_flow(graph, 0, sink_node)   

    def flow_edge(graph, node, exclude):
        for i in graph.graph[node]:
            edge = graph.edges[i]
            if edge.flow == 1 and edge.capacity != 0 and edge.v not in exclude:
                return edge.v
   
    def x_y_flow_edge(graph, node):
        return flow_edge(graph, node, [0])
   
    def y_x_flow_edge(graph, node):
        return flow_edge(graph, node, [sink_node])

    # Pull out the chains of charts.
    # Probably better to add reverse edges and
    # process chains in one go instead of having
    # to patch up because of only traversing one
    # way.
    overlay_charts = []
    overlayed = set([])
    for node in range(1, 1 + n):
        if node in overlayed:
            # already part of an overlay
            continue
        start_node = node
        next_node = x_y_flow_edge(graph, node)
        chart = [start_node]
        if next_node:
            overlayed.add(start_node)
            # start of a series of overlays
            while next_node:
                chart.append(next_node)
                opposite_node = next_node - n
                if opposite_node in overlayed:
                    # come up against an existing overlay
                    break
                overlayed.add(opposite_node)
                next_node = x_y_flow_edge(graph, opposite_node)

            # Check if this overlay is independent or can be added
            # to existing.
            last_node = chart[-1:][0] - n
            for i, chain in enumerate(overlay_charts):
                if chain[0] == last_node:
                    overlay_charts[i] = chart + chain[1:]
                    break 
            else: 
                overlay_charts.append(chart)

    #print([edge for edge in graph.edges if edge.flow == 1 and edge.capacity > 0])

    for node in set(list(range(1,1+n))).difference(overlayed):
        overlay_charts.append([node])

    def nodes_to_chart(nodes):
        chart = [nodes[0]]
        for node in nodes[1:]:
            chart.append(node - n)
        return chart

    #overlay_charts_ = [nodes_to_chart(nodes) for nodes in overlay_charts] 
    #print(overlay_charts_)
    return len(overlay_charts)

def read_data():
    n, k = map(int, input().split())
    stock_data = [list(map(int, input().split())) for i in range(n)]
    return stock_data

def solve():
    stock_data = read_data()
    result = min_charts(stock_data)
    print(result)

if __name__ == '__main__':
    solve()
