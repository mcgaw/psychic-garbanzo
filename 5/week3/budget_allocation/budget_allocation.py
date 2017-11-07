# python3
import itertools
from sys import stdin

#import cnf

# Quine-McKluskey algorithm
def combine(m, n):
    a = len(m)
    c = []
    count = 0
    for i in range(a): 
        if(m[i] == n[i]):
            c.append(m[i])
        elif(m[i] != n[i]):
            c.append('-')
            count += 1

    if(count > 1): 
        return None
    else:            
        return c

def find_prime_implicants(data):
    newList = list(data)
    size = len(newList)
    IM = []
    im = []
    im2 = []
    mark = [0]*size
    m = 0
    for i in range(size):
        for j in range(i+1, size):
            c = combine( newList[i], newList[j] )
            if c != None:
                im.append(c)
                mark[i] = 1
                mark[j] = 1
            else:
                continue

    mark2 = [0]*len(im)
    for p in range(len(im)):
        for n in range(p+1, len(im)):
            if( p != n and mark2[n] == 0):
                if( im[p] == im[n]):
                    mark2[n] = 1

    for r in range(len(im)):
        if(mark2[r] == 0):
            im2.append(im[r])

    for q in range(size):
        if( mark[q] == 0 ):
            IM.append(newList[q])
            m = m+1

    if(m == size or size == 1):
        return IM
    else:
        return IM + find_prime_implicants(im2)

def next_var(var):
    while True:
        var += 1
        yield var

var_seq = next_var(0)

def add_cnf_terms(eqs, terms, violations):

    if len(terms) == 1:
        clause = -terms[0][0] if violations[0][0] == 1 else terms[0][0]
        eqs.append([clause])
        return

    minterms = set(list(itertools.product(*[list(range(2))]*len(terms))))
    for v in violations:
        minterms.remove(v)

    def convert(implicant):
        if implicant[1] == 0:
            return terms[implicant[0]][0]
        elif implicant[1] == 1:
            return -terms[implicant[0]][0]
        return implicant[1]

    #print(cnf.cnf_terms_sympy(terms, minterms))

    pi = find_prime_implicants(violations)
    for implicant in pi:
        cnf_form = list(map(lambda t: convert(t), enumerate(implicant)))
        eqs.append(list(filter(lambda x: x != '-', cnf_form)))


def calculate_sat_problem(m, n, a, b):

    def print_equations(eqs):
        for eq in eqs:
            print('{0} 0'.format(' '.join([str(var) for var in eq])))

    # Basic binary condition to introduce all the
    # initial variables. (Some may not be presnet
    # and minisat needs to see them all at least
    # once)
    departments = [next(var_seq) for _ in range(n)]
    initial = []
    # Always satisfied.
    for dept in departments:
        initial += [dept, -dept]
    eqs = [initial]

    # Each equation has a set of constraints that if violated will
    # invalidate the inequality.
    for idx, ineq in enumerate(a):
        # Terms (max 3) with coeffs not 0.
        terms = list(filter(lambda x: x[1] != 0, enumerate(ineq, start=1)))

        violations = []
        # For all possible binary values of the variables in
        # this inequality.
        for comb in list(itertools.product(*[list(range(2))]*len(terms))):
            if sum([terms[i][1] * c for i, c in enumerate(comb)]) > b[idx]:
                violations.append(comb)

        # Case where constraint is impossible to satisfy.
        if len(violations) == pow(2, len(terms)):
            eqs += [[1], [-1]]
            break

        if len(violations) > 0:
            add_cnf_terms(eqs, terms, violations)

    #print('p cnf {1} {0}'.format(len(eqs), next(var_seq) - 1))
    print('{0} {1}'.format(len(eqs), next(var_seq) - 1))
    print_equations(eqs)

n, m = list(map(int, stdin.readline().split()))
a = []
for i in range(n):
  a += [list(map(int, stdin.readline().split()))]
b = list(map(int, stdin.readline().split()))


calculate_sat_problem(n, m, a, b)
