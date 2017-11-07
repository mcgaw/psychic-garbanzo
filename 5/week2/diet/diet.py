# python3
from sys import stdin

EPS = 1e-3
PRECISION = 20

class Equation:
    def __init__(self, a, b):
        self.a = a
        self.b = b

class Position:
    def __init__(self, column, row):
        self.column = column
        self.row = row

def select_pivot(a, b, used_rows, used_columns):

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
                break
        else:
          return None

    return pivot_element

def swap_lines(a, b, used_rows, pivot_element):
    a[pivot_element.column], a[pivot_element.row] = a[pivot_element.row], a[pivot_element.column]
    b[pivot_element.column], b[pivot_element.row] = b[pivot_element.row], b[pivot_element.column]
    used_rows[pivot_element.column], used_rows[pivot_element.row] = used_rows[pivot_element.row], used_rows[pivot_element.column]
    pivot_element.row = pivot_element.column;

def process_pivot(a, b, pivot_element):
    pivot_coeff = a[pivot_element.row][pivot_element.column]
    pivot_col =  pivot_element.column
    pivot_row = pivot_element.row

    #assert pivot_coeff != 0

    if pivot_coeff != 1:
        # scale for simplicity
        for col, coeff in enumerate(a[pivot_element.row]):
            a[pivot_row][col] = coeff / pivot_coeff
        b[pivot_row] = b[pivot_row] / pivot_coeff
        #assert a[pivot_row][pivot_col] == 1
        pivot_coeff = 1

    # substitue into remaining rows
    for row in range(len(a)):
        if row == pivot_row:
            continue

        factor = (a[row][pivot_col] / pivot_coeff)
        # subtract pivot row from the current row to reduce
        # coeff in pivot column to zero.
        for col, coeff in enumerate(a[row]):
            if col == pivot_col:
              a[row][col] = 0
              continue
            a[row][col] = a[row][col] - factor * a[pivot_row][col]
        b[row] = b[row] - factor * b[pivot_row]
    
def mark_pivot(pivot_element, used_rows, used_columns):
    used_rows[pivot_element.row] = True
    used_columns[pivot_element.column] = True

def gaussian(a, b):
    size = len(a)

    used_columns = [False] * size
    used_rows = [False] * size
    for step in range(size):
        pivot_element = select_pivot(a, b, used_rows, used_columns)
        if pivot_element is None:
          return None
        swap_lines(a, b, used_rows, pivot_element)
        process_pivot(a, b, pivot_element)
        mark_pivot(pivot_element, used_rows, used_columns)
    return b

def find_subsets(size, the_set):
  """
  Subsets of size size in set the_set.
  """
  if size == 0:
    return set()

  subsets =  set([ frozenset([i]) for i in range(1, the_set+1)])

  for size in range(2, size+1):
    new_sets = set([])
    for subset in subsets:
      for num in range(1, the_set+1):
        temp = frozenset(list(subset)+[num])
        if len(temp) == size:
          new_sets.add(temp)
    subsets = new_sets
  return subsets

def are_equal(a, b):
  if abs(a - b) <= EPS:
    return True
  else:
    return False

def solve_diet_problem(n, m, a, b, c):  
  """
  Try solving systems of n equalities with m
  unknowns to find possible solutions.
  Solutions are then checked against the remaining inequalities.
  Repeat until a starting solution is found.
  """
  best_result = -float('Inf')
  solution = None
  infinity = False
 
  # add greater than zero inequalities
  for idx in range(n, n+m):
    row = [0] * (m)
    a.append(row)
    row[idx-n] = -1
    b.append(0)

  # add restriction to catch 'infinity'
  a.append([1] * m)
  b.append(10e9)
  for equations in find_subsets(m, len(a)):
      a_ = []
      b_ = []
      for eq in equations:
        a_.append(a[eq-1].copy())
        b_.append(b[eq-1])

      result = gaussian(a_, b_)
      if not result is None:
        #print('found possible solution {0} using {1}'.format(result, equations))
        # see if the other inequalities are satisfied.
        satisfied = True
        other_inequals = set(list(range(1, len(a)+1))).difference(equations)
        for eq in other_inequals :
          sum = 0
          for col, coeff in enumerate(a[eq-1]):
            sum += coeff * result[col]

          if sum - b[eq-1] >= EPS:
          #if are_equal(sum, b[eq-1]) or sum > b[eq-1]:
            satisfied = False
            #print('equation {0} not satisfied'.format(eq))
            break

        if satisfied:
          # see if this solution is better than
          # the current one.
          maximization = 0
          for idx, x in enumerate(result):    
            maximization += x * c[idx]
          # check for 'infinity' result
          if len(a) in equations:
            infinity_based = True
          else:
            infinity_based = False

          if (not infinity_based and are_equal(maximization, best_result)) or\
            (maximization > best_result):
            infinity = infinity_based
            #print('new max of {0}'.format(maximization))
            best_result = maximization
            solution = result
          else:
            #print('{0} is lower than or equal to {1}'.format(maximization, best_result))
            pass

  if infinity:
    return [1, solution]

  if not solution:
    return [-1, solution]

  return [0, solution]



n, m = list(map(int, stdin.readline().split()))
A = []
for i in range(n):
  A += [list(map(int, stdin.readline().split()))]
b = list(map(int, stdin.readline().split()))
c = list(map(int, stdin.readline().split()))

anst, ansx = solve_diet_problem(n, m, A, b, c)

if anst == -1:
  print("No solution")
if anst == 0:  
  print("Bounded solution")
  print(' '.join(list(map(lambda x : '%.18f' % x, ansx))))
if anst == 1:
  print("Infinity")
    
