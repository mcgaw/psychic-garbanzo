import random
import datetime
import cProfile
import pstats
import io
import circuit_design
import threading

def main():
    pr = cProfile.Profile()
    n = random.randint(1, 10**6)
    m = random.randint(1, 10**6)

    clauses = []
    choices = list(range(-n, 0)) + list(range(1, n + 1))
    l = len(choices)

    for __ in range(m):
        clauses.append([choices[random.randint(0, l - 1)] for _ in range(2)])

    pr.enable()
    print('n: {0} m: {1}'.format(n, m))
    start = datetime.datetime.now()
    result = threading.Thread(target=circuit_design.is_satisfiable, args=(n, m, clauses)).start()
    #result = circuit_design.is_satisfiable(n, m, clauses)
    duration = datetime.datetime.now() - start

    pr.disable()
    s = io.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())
    print('processing took {0}'.format(duration))
    if result is not None:
        for i, clause in enumerate(clauses):
            if result[abs(clause[0])] * clause[0] < 0 and\
                result[abs(clause[1])] * clause[1] < 0:
                assert False, 'result does not satsify solution'
        print('verified satisfied solution')
    else:
        print('no solution')

while True:
    main()