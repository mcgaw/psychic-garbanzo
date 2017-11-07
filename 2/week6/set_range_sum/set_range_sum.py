# python3

import sys, threading
from sys import stdin

sys.setrecursionlimit(10**7) # max depth of recursion
threading.stack_size(2**27)  # new thread will get stack of such size

debug = False

def log(text):
  if debug:
    print(text)

# Splay tree implementation

# Vertex of a splay tree
class Vertex:
  def __init__(self, key, sum, left, right, parent):
    (self.key, self.sum, self.left, self.right, self.parent) = (key, sum, left, right, parent)

  def __repr__(self):
    return str(self.key)

# update the sum values of the node and
# parent child references
def update(v):
  if v == None:
    return
  v.sum = v.key + (v.left.sum if v.left != None else 0) + (v.right.sum if v.right != None else 0)
  if v.left != None:
    v.left.parent = v
  if v.right != None:
    v.right.parent = v

def smallRotation(v):
  parent = v.parent
  if parent == None:
    return
  grandparent = v.parent.parent
  if parent.left == v:
    m = v.right
    v.right = parent
    parent.left = m
  else:
    m = v.left
    v.left = parent
    parent.right = m
  update(parent)
  update(v)
  v.parent = grandparent
  if grandparent != None:
    if grandparent.left == parent:
      grandparent.left = v
    else: 
      grandparent.right = v

def bigRotation(v):
  if v.parent.left == v and v.parent.parent.left == v.parent:
    # Zig-zig
    smallRotation(v.parent)
    smallRotation(v)
  elif v.parent.right == v and v.parent.parent.right == v.parent:
    # Zig-zig
    smallRotation(v.parent)
    smallRotation(v)    
  else: 
    # Zig-zag
    smallRotation(v)
    smallRotation(v)

# Makes splay of the given vertex and makes
# it the new root.
def splay(v):
  if v == None:
    return None
  while v.parent != None:
    if v.parent.parent == None:
      smallRotation(v)
      break
    bigRotation(v)
  return v

# Searches for the given key in the tree with the given root
# and calls splay for the deepest visited node after that.
# Returns pair of the result and the new root.
# If found, result is a pointer to the node with the given key.
# Otherwise, result is a pointer to the node with the smallest
# bigger key (next value in the order).
# If the key is bigger than all keys in the tree,
# then result is None.
def find(root, key): 
  (last, next) = _find_node(root, key)
  root = splay(last)
  return (next, root)

# non-destructive node find
def _find_node(root, key):
  v = root
  next_biggest = None
  last = root
  while v != None:
    # update the next biggest key if neccessary, in case
    # the key is never found
    if v.key >= key and (next_biggest == None or v.key < next_biggest.key):
      next_biggest = v

    last = v
    if v.key == key:
      break    
    if v.key < key:
      v = v.right
    else: 
      v = v.left

  # last and next_biggest _may_ equal the key
  return (last, next_biggest)

def split(root_, key):  
  (result, root) = find(root_, key)  
  if result == None:    
    return (root, None)  
  right = splay(result)
  left = right.left
  right.left = None
  if left != None:
    left.parent = None
  update(left)
  update(right)
  return (left, right)


def merge(left, right):
  if left == None:
    return right
  if right == None:
    return left
  while right.left != None:
    right = right.left
  right = splay(right)
  right.left = left
  update(right)
  return right


# Code that uses splay tree to solve the problem

root = None

def print_tree(root):
  if not debug:
    return

  if root is None:
    log('None')

  def traverse_node(node):
    if node is None:
      return

    log(str(node) + ' <- ' + str(node.parent))

    left = node.left
    if left is not None:
      traverse_node(left)
    right = node.right

    if right is not None:
      traverse_node(right)

  traverse_node(root)

def insert(x):
  global root
 
  log('inserting node with key {0}'.format(x))
  
  (left, right) = split(root, x)
  new_vertex = None
  if right == None or right.key != x:
    new_vertex = Vertex(x, x, None, None, None)  
  root = merge(merge(left, new_vertex), right)

def erase(x):
  global root
  (node, next_biggest) = _find_node(root, x)
  
  log('erasing {0}, node {1} next_biggest {2}'.format(x, node, next_biggest)) 
  
  if not node or node.key != x:
    return

  new_root = splay(node.parent)
  splay(node)

  left = node.left
  right = node.right

  # if was only one node in tree
  if left is None and right is None:
    root = None
    return

  if left is None:
    root = right
    right.parent = None
    update(right)
    return

  if right is None:
    root = left 
    left.parent = None
    update(left)
    return

  left.parent = None
  right.parent = None
  root = merge(left, right)
  return


  vacant_child = (right.left is None) or (left.right is None)
  assert vacant_child, "can't merge trees"

  if right.left is not None: 
    left.parent = right
    right.left = left
    root = right
    right.parent = None
  else:
    right.parent = left 
    left.right = right
    root = left
    left.parent = None

def search(x): 
  global root
  (next_biggest, new_root) = find(root, x)
  root = new_root
  return (next_biggest is not None and next_biggest.key == x)

def sum(fr, to): 
  global root
  (left, middle) = split(root, fr)
  (middle, right) = split(middle, to + 1)

  if middle is not None:
    result = middle.sum
  else:
    result = 0

  root = merge(left, merge(middle, right))
  return result

MODULO = 1000000001
n = int(stdin.readline())
last_sum_result = 0
for i in range(n):
  line = stdin.readline().split()
  log('Operation: {0}'.format(line))
  if line[0] == '+':
    x = int(line[1])
    if debug:
      insert((x + last_sum_result) % MODULO)
    else:
      insert(x)
  elif line[0] == '-':
    x = int(line[1])
    if debug:
      erase((x + last_sum_result) % MODULO)
    else:
      erase(x)
  elif line[0] == '?':
    x = int(line[1])
    if debug:
      print('Found' if search((x + last_sum_result) % MODULO) else 'Not found')
    else:
      print('Found' if search(x) else 'Not found')
  elif line[0] == 's':
    l = int(line[1])
    r = int(line[2])
    if debug:
      res = sum((l + last_sum_result) % MODULO, (r + last_sum_result) % MODULO)
    else:
      res = sum(l, r)
    print(res)
    last_sum_result = res % MODULO
  log('----Tree Nodes-----')
  print_tree(root)
  log('-------------------')
