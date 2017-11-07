# python3

import sys, threading

sys.setrecursionlimit(1000000000) # max depth of recursion
threading.stack_size(2**29)  # new thread will get stack of such size

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
    if not debug:
      return ''

    if self is None:
      return 'Empty'

    repr = ['Tree structure:']
    def traverse_node(node, is_root):
      if node is None:
        return

      assert is_root or node.parent is not None, "invalid tree"

      nonlocal repr
      traverse_node(node.left, False)
      parent = 'None' if node.parent is None else node.parent.key
      left_child = 'None' if node.left is None else node.left.key 
      right_child = 'None' if node.right is None else node.right.key 
      repr.append(str('  ') + str(node.key) + ' : ' + str(node.sum) +
        ' ->'+left_child+', ->'+right_child + ':: '+parent)
      traverse_node(node.right, False)

    traverse_node(self, True)
    return '\n'.join(repr)

# update the sum values of the node and
# parent child references
def update(v):
  if v == None:
    return
  v.sum = 1 + (v.left.sum if v.left != None else 0) + (v.right.sum if v.right != None else 0)
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

def order_statistic_find(root, pos):

  if root is None:
    return (None, None)

  log('performing find of order statistic {0} on:'.format(pos))
  log(str(root))

  node = root
  if node.left is None:
    l_size = 0
  else:
    l_size = node.left.sum

  while (pos != l_size + 1):
    assert node is not None, "invalid order statistics"

    if pos < l_size + 1:
      node = node.left
    else:
      node = node.right
      pos = pos - l_size -1

    if node.left is None:
      l_size = 0
    else:
      l_size = node.left.sum

  return(node, splay(node))

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

def split(root_, order_stat):

  log('::SPLIT::')
  log('order stat {0}'.format(order_stat))

  (result, root) = order_statistic_find(root_, order_stat)  
  #(result, root) = find(root_, key)  

  log('found node:')
  log('None' if result is None else str(result.key))
  if result == None:    
    return (root, None)

  right = splay(result)
  left = right.left

  right.left = None
  if left != None:
    left.parent = None
  update(left)
  update(right)

  log('result of split:')
  log(str(left))
  log(str(right))
  return (left, right)


# there is an assumption that all the key values in the
# left tree are less than those in the right tree.
def merge(left, right):
  log('::MERGE::')
  log(left)
  log(right)
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

def in_order_chars(node):
  chars = []
  if root is None:
    return chars

  def traverse_node(node):
    nonlocal chars 
    if node is None:
      return
    left = node.left
    traverse_node(left)
    right = node.right
    chars.append(node.key)
    traverse_node(right)

  current = node.left
  parent = node
  while current != None or parent != None:
      if parent != None:
        parent.left = current.right
        current.right = parent
      
      if current.left != None:
        parent = current
        current = current.left
      else:
        chars.append(current.key)
        current = current.right
        parent = None
  
  #traverse_node(root)
  return chars

class Rope:
  def __init__(self, s):
    global root
    self.s = s
    for pos, char in enumerate(s):
      log('inserting key {0} with order statistic {1}'.format(char, pos))
      if root is None:
        root = Vertex(char, 1, None, None, None)
      else:
        child = root
        root = Vertex(char, child.sum + 1, child, None, None)
        child.parent = root
      log(root)
    log('finished building initial tree')

  def result(self):
    return ''.join(in_order_chars(root))

  def process(self, left_pos, right_pos, insertion_pos):
    global root
    # first remove the substring
    (left, start) = split(root, left_pos+1)

    # splitting depends on whether the substring is at the end
    if right_pos == len(self.s) - 1:
      log('substring is at the end, no need to split')
      substring = start
      right = None
    else:
      (substring, right) = split(start, right_pos - left_pos + 2)

    spliced = merge(left, right)

    # then split at the insertion pointer
    # if position at end no need to split
    if insertion_pos == len(self.s) - (right_pos - left_pos + 1):
      log('insertion point is at end of spliced string, no need to split')
      left = spliced
      right = None
    else:
      (left, right) = split(spliced, insertion_pos + 1)

    # and insert the substring at new position
    new_left = merge(left, substring)
    root = merge(new_left, right)

rope = Rope(sys.stdin.readline().strip())
q = int(sys.stdin.readline())
for _ in range(q):
  i, j, k = map(int, sys.stdin.readline().strip().split())
  rope.process(i, j, k)

print(rope.result())
