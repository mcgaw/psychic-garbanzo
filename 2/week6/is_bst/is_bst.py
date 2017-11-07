#!/usr/bin/python3

import sys, threading

sys.setrecursionlimit(10**7) # max depth of recursion
threading.stack_size(2**27)  # new thread will get stack of such size

def IsBinarySearchTree(tree):

  invalid = [False]

  def traverse(node, upper, lower, invalid):
    if invalid[0]:
      return

    node_val = node[0]
    left = node[1]
    right = node[2]

    if left != -1:
      left_val = tree[left][0]
      if left_val > node_val or \
        (upper and left_val > upper) or \
        (lower and left_val < lower):
        #print('failed upper: {0} left_val: {1}'.format(upper, left_val))
        invalid[0] = True   
        return
      else:
        if not upper or node_val < upper:
          upper_ = node_val
        traverse(tree[left], upper_, lower, invalid)

    if right != -1:
      right_val = tree[right][0]
      if right_val < node_val or \
        (lower and right_val < lower) or \
        (upper and right_val > upper):
        #print('failed lower: {0} right_val: {1}'.format(lower, right_val))
        invalid[0] = True
        return
      else:
        if not lower or node_val > lower:
          lower_ = node_val
        traverse(tree[right], upper, lower_, invalid)

  if tree != []:
    traverse(tree[0], None, None, invalid)
    return not invalid[0]
  else:
    return True

def main():
  nodes = int(sys.stdin.readline().strip())
  tree = []
  for i in range(nodes):
    tree.append(list(map(int, sys.stdin.readline().strip().split())))
  if IsBinarySearchTree(tree):
    print("CORRECT")
  else:
    print("INCORRECT")

threading.Thread(target=main).start()
