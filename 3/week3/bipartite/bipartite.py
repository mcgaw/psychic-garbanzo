#Uses python3

import sys
import collections


def bipartite(adjacents):
    RED = 'red'
    BLACK = 'black'

    q = collections.deque()
    layers = [-1] * len(adjacents)
    layers[0] = (None, BLACK)
    q.appendleft((0, BLACK))

    clash = False
    while len(q) > 0:
        current = q.pop()

        #print('current {0}'.format(current))

        for adjacent in adjacents[current[0]]:
            if layers[adjacent] != -1:
                # check for matching adjacent colours
                # which would break bipartite condition.
                if layers[adjacent][1] == current[1]:
                    #print('clash {0} vs {1}'.\
                    #    format(layers[adjacent], current))
                    clash = True
                    break
                else:
                    continue
            colour = RED if current[1] == BLACK else BLACK
            layers[adjacent] = (current, colour)
            q.appendleft((adjacent, colour))

        else:
            continue

        break

    return 0 if clash else 1


if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))
    adj = [[] for _ in range(n)]
    for (a, b) in edges:
        adj[a - 1].append(b - 1)
        adj[b - 1].append(a - 1)
    print(bipartite(adj))
