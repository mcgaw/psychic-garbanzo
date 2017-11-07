#uses python3

import functools
import sys
import threading
import collections

# This code is used to avoid stack overflow issues
sys.setrecursionlimit(10**6) # max depth of recursion
threading.stack_size(2**26)  # new thread will get stack of such size


class Vertex:
    def __init__(self, weight):
        self.weight = weight
        self.children = []


def read_tree():
    size = int(input())
    tree = [Vertex(w) for w in map(int, input().split())]
    for i in range(1, size):
        a, b = list(map(int, input().split()))
        tree[a - 1].children.append(b - 1)
        tree[b - 1].children.append(a - 1)
    return tree

def D(memoised, graph, v, p):
    #print(v, graph[v].weight, graph[v].children)

    if memoised[v] != -1:
        return memoised[v]

    vert = graph[v]
    if len(list(filter(lambda c: c != p, vert.children))) == 0:
        memoised[v] = vert.weight
        return vert.weight
    
    m1 = vert.weight
    for child in [c for c in vert.children if c != p]:
        for g_child in  [g_child for g_child in graph[child].children if g_child != v]:
           if memoised[g_child] == -1:
                memoised[g_child] == graph[g_child].weight
           m1 += memoised[g_child]
            
    m0 = 0
    for child in [c for c in vert.children if c != p]:
        if memoised[child] == -1:
            memoised[child] = graph[child].weight
        m0 += memoised[child]

    memoised[v] = max(m0,m1)
    return memoised[v]

def dfs(tree, vertex, parent, d_func):
    for child in tree[vertex].children:
        if child != parent:
            dfs(tree, child, vertex, d_func)
    r = d_func(vertex, parent)

def max_indep_set_weight(tree):
    size = len(tree)
    if size == 0:
        return 0

    weights = collections.defaultdict(lambda: -1)
    d_func = functools.partial(D, weights, tree)

    dfs(tree, 0, -1, d_func)
    return max(weights.values())


def main():
    tree = read_tree();
    weight = max_indep_set_weight(tree);
    print(weight)


# This is to avoid stack overflow issues
threading.Thread(target=main).start()
