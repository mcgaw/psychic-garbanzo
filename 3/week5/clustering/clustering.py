#Uses python3
import sys
import math

def distance(a, b):
    x = b[0]-a[0]
    y = b[1]-a[1]
    return math.sqrt(x*x + y*y)

def clustering(x, y, k):
    points = list(zip(x, y))
    edges = []
    for a in points:
        for b in points:
            if b == a:
                continue
            edges.append((a, b, distance(a, b)))
    edges = sorted(edges, key=lambda x: x[2])

    def cluster(k_sets):
        # Kruksal algo
        disjoint_sets = [set([point]) for point in points]

        minimum_edges = set([])
        max_distance = 0
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

            # if have the correct number of clusters, next edge represents the
            # minimum distance between clusters
            if len(list(filter(lambda x: x != set(), disjoint_sets))) == k:
                return edge[2]

            minimum_edges.add(edge)
            disjoint_sets[set1] = disjoint_sets[set1].union(disjoint_sets[set2])
            disjoint_sets[set2] = set([])

        assert 'invalid number of clusters specified', False

    return cluster(k)


if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n = data[0]
    data = data[1:]
    x = data[0:2 * n:2]
    y = data[1:2 * n:2]
    data = data[2 * n:]
    k = data[0]
    print("{0:.9f}".format(clustering(x, y, k)))
