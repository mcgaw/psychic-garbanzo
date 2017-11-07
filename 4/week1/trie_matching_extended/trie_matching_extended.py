# python3
import sys

class Node(dict):

    def __init__(self):
        self.end_node = False

    def __repr__(self):
        if self.end_node:
            return '-'+ super().__repr__() + '-'
        else:
            return super().__repr__()

def build_trie(patterns):
    tree = Node()
    tree[0] = Node()
    count = 1
    for pattern in patterns:
        node = tree[0]
        for letter in pattern:
            if letter in node:
                # traverse to next node in trie
                node = tree[node[letter]]
            else:
                # add new node in trie for this letter
                node[letter] = count
                tree[count] = Node()
                node = tree[count]
                count += 1

        node.end_node = True

    return tree

def solve (text, n, patterns):
  trie = build_trie(patterns)
  matches = []

  for start in range(0, len(text)):
    node = trie[0]
    letter = text[start]

    count = start
    while letter in node:
      node = trie[node[letter]]
      if node.end_node:
          break
      count += 1
      if count >= len(text):
        break
      letter = text[count]

    if node == {} or node.end_node:
      matches.append(start)

  return matches

text = sys.stdin.readline ().strip ()
n = int (sys.stdin.readline ().strip ())
patterns = []
for i in range (n):
  patterns += [sys.stdin.readline ().strip ()]

ans = solve (text, n, patterns)

sys.stdout.write (' '.join (map (str, ans)) + '\n')
