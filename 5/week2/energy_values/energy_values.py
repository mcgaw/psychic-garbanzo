# python3

EPS = 1e-6
PRECISION = 20

class Equation:
    def __init__(self, a, b):
        self.a = a
        self.b = b

class Position:
    def __init__(self, column, row):
        self.column = column
        self.row = row

def ReadEquation():
    size = int(input())
    a = []
    b = []
    for row in range(size):
        line = list(map(float, input().split()))
        a.append(line[:size])
        b.append(line[size])
    return Equation(a, b)

def SelectPivotElement(a, b, used_rows, used_columns):
    # This algorithm selects the first free element.
    # You'll need to improve it to pass the problem.

    pivot_element = Position(0, 0)
    while used_rows[pivot_element.row]:
        pivot_element.row += 1
    while used_columns[pivot_element.column]:
        pivot_element.column += 1

    val = a[pivot_element.row][pivot_element.column]
    if val == 0:
        # find next non zero val and swap that row with
        # the pivot row.
        col = pivot_element.column
        pivot_row = pivot_element.row
        for row in range(pivot_element.row+1, len(a)):
            if a[row][col] != 0:
                # swap this row with the pivot row
                temp = a[row]
                a[row] = a[pivot_row]
                a[pivot_row] = temp

                temp = b[row]
                b[row] = b[pivot_row]
                b[pivot_row] = temp

    return pivot_element

def SwapLines(a, b, used_rows, pivot_element):
    a[pivot_element.column], a[pivot_element.row] = a[pivot_element.row], a[pivot_element.column]
    b[pivot_element.column], b[pivot_element.row] = b[pivot_element.row], b[pivot_element.column]
    used_rows[pivot_element.column], used_rows[pivot_element.row] = used_rows[pivot_element.row], used_rows[pivot_element.column]
    pivot_element.row = pivot_element.column;

def ProcessPivotElement(a, b, pivot_element):
    pivot_coeff = a[pivot_element.row][pivot_element.column]
    pivot_col =  pivot_element.column
    pivot_row = pivot_element.row

    assert pivot_coeff != 0

    if pivot_coeff != 1:
        # scale for simplicity
        for col, coeff in enumerate(a[pivot_element.row]):
            a[pivot_row][col] = coeff / pivot_coeff
        b[pivot_row] = b[pivot_row] / pivot_coeff
        assert a[pivot_row][pivot_col] == 1
        pivot_coeff = 1

    # substitue into remaining rows
    for row in range(len(a)):
        if row == pivot_row:
            continue

        factor = (a[row][pivot_col] / pivot_coeff)
        # subtract pivot row from the current row to reduce
        # coeff in pivot column to zero.
        for col, coeff in enumerate(a[row]):
            a[row][col] = a[row][col] - factor * a[pivot_row][col]
        b[row] = b[row] - factor * b[pivot_row]
    
def MarkPivotElementUsed(pivot_element, used_rows, used_columns):
    used_rows[pivot_element.row] = True
    used_columns[pivot_element.column] = True

def SolveEquation(equation):
    a = equation.a
    b = equation.b
    size = len(a)
 
    used_columns = [False] * size
    used_rows = [False] * size
    for step in range(size):
        pivot_element = SelectPivotElement(a, b, used_rows, used_columns)
        SwapLines(a, b, used_rows, pivot_element)
        ProcessPivotElement(a, b, pivot_element)
        MarkPivotElementUsed(pivot_element, used_rows, used_columns)
    return b

def PrintColumn(column):
    size = len(column)
    for row in range(size):
        print("%.20lf" % column[row])

if __name__ == "__main__":
    equation = ReadEquation()
    solution = SolveEquation(equation)
    PrintColumn(solution)
    exit(0)
