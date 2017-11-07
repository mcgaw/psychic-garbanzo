# python3
import itertools

INF = float('Inf')

def read_data():
    n, m = map(int, input().split())
    graph = [[INF] * n for _ in range(n)]
    for _ in range(m):
        u, v, weight = map(int, input().split())
        u -= 1
        v -= 1
        graph[u][v] = graph[v][u] = weight
    return graph

def print_answer(path_weight, path):
    if path_weight == INF:
        print('-1')
    else:
        print(path_weight)
        print(' '.join(map(str, path)))

def optimal_path(graph):
    n = len(graph)
    C = {}

    def get_distance(vertices, last_vertex):
        key = tuple(sorted(vertices))
        if key not in C:
            return INF
        return C[key][last_vertex]

    def set_distance(vertices, last_vertex, distance):
        key = tuple(sorted(vertices))
        if key not in C:
            C[key] = [INF] * n
        C[key][last_vertex] = distance


    set_distance((0,), 0, 0)
    for s in range(1, n):
        for S_ in itertools.combinations(range(1,n), s):
            S = (0,) + S_

            # Each new combination can be investigated by looking at
            # all the len(S_) - 1 combinations and looking at their
            # possible extensions to cover the extra vertice.
            for i in S:
                if i == 0:
                    continue
                for j in S:
                    if j == i:
                        continue
                    for z in range(len(S)-1, 0, -1):
                        if S[z] == i:
                            without_i = S[:z] + S[z+1:]
                    current = get_distance(S, i)
                    new = get_distance(without_i, j) + graph[j][i]
                    #print(S, without_i, j, i, current, new)
                    if new < current:
                        set_distance(S, i, new)

    best_path = [] 
    best_ans = INF
    
    # for key in sorted(C.keys(), key=lambda x: len(x)):
    #     print(key, C[key])

    # If a full set of vertices has been found need to manually
    # check which path back to vertice 1 will give the shortest
    # distance. This defines the final vertice in the path.
    for key in C:
        if len(key) == n:
            last_vert = None
            for vert in key:
                distance = get_distance(key, vert) + graph[vert][0]
                if distance < best_ans:
                    last_vert = vert
                    best_ans = distance
                    best_vertices = key


    # To get the actual path from the set of vertices, basically reverse
    # the steps of the dynamic programming algorithm.
    # No information has been lost.
    best_path = [] 
    path_distance = None

    def walk_path(remaining, path, distance):
        nonlocal best_path, path_distance
        if len(remaining) == 2:
            best_path = path
            remaining_ = set(remaining)
            remaining_.remove(0)
            path_distance = distance + get_distance(remaining, remaining_.pop())
            return

        # Find the vertice in the smaller set that was used
        # to construct a path to path[0].
        remaining_ = set(remaining)
        remaining_.remove(path[0])
        smallest = INF
        path_vertice = None
        for i  in remaining_:
            dist = get_distance(remaining_, i)
            if i == 0 or dist == INF:
                continue
            dist_back = graph[i][path[0]] + dist
            if dist_back < smallest:
                smallest = dist_back
                path_vertice = i

        assert smallest != INF
        new_path = [path_vertice] + path.copy()
        walk_path(remaining_, new_path, distance + smallest)

    if best_ans < INF:
        walk_path(best_vertices, [last_vert, 0], graph[last_vert][0])

    # Check path gives the correct distance.
    distance = 0
    if best_ans < INF:
        for i, vert in enumerate(best_path[:-1]):
            distance += graph[vert][best_path[i+1]]
        distance += graph[best_path[-1]][best_path[0]]
        assert distance == best_ans, 'path shows a distance of {0}, but answer was {1}'.format(
            distance, best_ans)

    return (best_ans, [x + 1 for x in best_path])

if __name__ == '__main__':
    data = read_data()
    print_answer(*optimal_path(data))
