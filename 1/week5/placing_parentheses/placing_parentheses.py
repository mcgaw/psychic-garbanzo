# Uses python3
import re

M = None
m = None

def evalt(a, b, op):
    if op == '+':
        return a + b
    elif op == '-':
        return a - b
    elif op == '*':
        return a * b
    else:
        assert False

def min_max(i, j, exp):
    max_ = -float('Inf')
    min_ = float('Inf')

    for k in range(i, j):
        op = exp[k]
        a = evalt(M[i][k], M[k+1][j], op)
        b = evalt(M[i][k], m[k+1][j], op)
        c = evalt(m[i][k], M[k+1][j], op)
        d = evalt(m[i][k], m[k+1][j], op)

        max_ = max(a, b, c, d, max_)
        min_ = min(a, b, c, d, min_)
    
    return (max_, min_)

def extract_placement():
    pass


def get_maximum_value(dataset):

    operators = list(filter(lambda t: t != '', re.split(r'[0-9]', dataset)))
    digits = list(map(lambda t: int(t), filter(lambda t: t != '', re.split(r'[^0-9]', dataset))))

    n = len(digits)
    global M, m
    M = [[None for _ in range(n)] for _ in range(n)]
    m = [[None for _ in range(n)] for _ in range(n)]

    for i in range(n):
        M[i][i] = digits[i]
        m[i][i] = digits[i]

    for s in range(1, n):
        for i in range(0, n-s):
            j = i + s
            M[i][j], m[i][j] = min_max(i, j, operators)

    return M[0][n-1]


if __name__ == "__main__":
    print(get_maximum_value(input()))
