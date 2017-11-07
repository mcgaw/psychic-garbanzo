# python3

import sys
import threading

sys.setrecursionlimit(10**7)  # max depth of recursion
threading.stack_size(2**27)  # new thread will get stack of such size

n, m = map(int, sys.stdin.readline().split())
lines = list(map(int, sys.stdin.readline().split()))
ranks = [1] * n
parents = list(range(0, n))
ans = max(lines)

def getParent(table):
    # find parent and compress path
    if parents[table] != table:
        parents[table] = getParent(parents[table])

    return parents[table]

def merge(destination, source):
    real_destination, real_source = getParent(destination), getParent(source)

    #print('real_destination {0}, real_source {1}'.format(real_destination, real_source))
    if real_destination == real_source:
        return False

    # merge two components
    # use union by rank heuristic 
    # update ans with the new maximum table size
    merged_lines = lines[real_destination] + lines[real_source]

    if ranks[real_destination] > ranks[real_source]:
        parents[real_source] = real_destination
        lines[real_destination] =  merged_lines
    else:
        parents[real_destination] = real_source
        lines[real_source] =  merged_lines
        if ranks[real_destination] == ranks[real_source]:
            ranks[real_source] = ranks[real_source] + 1

    global ans
    if merged_lines > ans:
        ans = merged_lines

    return True

for i in range(m):
    destination, source = map(int, sys.stdin.readline().split())
    merge(destination - 1, source - 1)
    print(ans)

