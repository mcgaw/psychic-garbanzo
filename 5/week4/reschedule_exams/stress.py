import numpy as np
from scipy.optimize import linprog
import subprocess
from itertools import permutations

INF = float('Inf')

def optimal_path(graph):
    n = len(graph)
    best_ans = INF
    best_path = []

    for p in permutations(range(n)):
        cur_sum = 0
        for i in range(1, n):
            if graph[p[i - 1]][p[i]] == INF:
                break
            cur_sum += graph[p[i - 1]][p[i]]
        else:
            if graph[p[-1]][p[0]] == INF:
                continue
            cur_sum += graph[p[-1]][p[0]]
            if cur_sum < best_ans:
                best_ans = cur_sum
                best_path = list(p)

    if best_ans == INF:
        return (-1, [])
    return (best_ans, [x + 1 for x in best_path])

for _ in range(100000):
    n = np.random.randint(3, 10)
    m = np.random.randint(1, (n * (n-1))//2)

    edges = np.random.randint(1, n+1, size = (m, 2,))
    weights = np.random.randint(1, 100, size = (m,))

    lines = []
    for i in range(m):
        edge = list(edges[i])
        edge.append(weights[i])
        lines.append(edge)
    
    graph = [[INF] * n for _ in range(n)]
    print(n, m)
    for line in lines:
        print(*line)
        u, v, weight = line
        u -= 1
        v -= 1
        graph[u][v] = graph[v][u] = weight

    proc = subprocess.Popen(['./school_bus.sh'], stdin = subprocess.PIPE, stdout = subprocess.PIPE, universal_newlines = True)
    print(n, m, file=proc.stdin)
    for i in range(m):
        print(*(lines[i]), file=proc.stdin)
    print()

    stdoutdata, _ = proc.communicate()
    assert proc.returncode == 0

    stdout_lines = stdoutdata.splitlines()
    res = optimal_path(graph)

    if stdout_lines[0] == '-1':
        assert res[0] == -1
    else:
        assert int(stdout_lines[0]) == res[0]
        dynamic_sol = [int(x) for x in stdout_lines[1].split()]
        distance = 0
        for i, vert in enumerate(dynamic_sol[:-1]):
            distance += graph[vert-1][dynamic_sol[i+1]-1]
        distance += graph[dynamic_sol[-1]-1][dynamic_sol[0]-1]

        assert distance == int(stdout_lines[0]), 'path added up to {0}, but answer was {1}'.format(
            distance, stdout_lines[0])

    print(stdoutdata, end='')
    print(res)
