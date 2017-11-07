#Uses python3
import sys
import math

def distance(a, b):
    x = b[0]-a[0]
    y = b[1]-a[1]
    return math.sqrt(x*x + y*y)

def minimum_distance(x, y):
    points = list(zip(x, y))
    edges = []
    for a in points:
        for b in points:
            if b == a:
                continue
            edges.append((a, b, distance(a, b)))
    edges = sorted(edges, key=lambda x: x[2])

    # Kruksal algo
    disjoint_sets = [set([point]) for point in points]

    minimum_edges = set([])
    for edge in edges:
        point_a = edge[0]
        point_b = edge[1]
        set1 = None
        set2 = None
        for idx, vertices in enumerate(disjoint_sets):
            if point_a in vertices:
                set1 = idx
            if point_b in vertices:
                set2 = idx
            if not set1 is None and\
                not set2 is None:
                break
        else:
            assert "Edge nodes not in the dijoint sets", False

        # check will not form a cycle
        if set1 == set2:
            continue
        minimum_edges.add(edge)
        disjoint_sets[set1] = disjoint_sets[set1].union(disjoint_sets[set2])
        disjoint_sets[set2] = set([])


    return sum([edge[2] for edge in minimum_edges])


if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n = data[0]
    x = data[1::2]
    y = data[2::2]
    print("{0:.9f}".format(minimum_distance(x, y)))
