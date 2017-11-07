# python3
import sys
from datetime import datetime
import threading

sys.setrecursionlimit(1000000000) # max depth of recursion
threading.stack_size(2**29)  # new thread will get stack of such size

class Node(dict):

    def __init__(self):
        self.suffix = ''
        self.position = 0

    def __repr__(self):
      return '<<' + super().__repr__() + ' : ' + self.suffix + '>>'

count = 1

def update_trie(trie, text, text_pointer):
    global count

    node_id = 0
    node = trie[node_id]
    # loop around each traversal of trie
    finished = False
    while True:
        # how much of the remaining text is stored at this node
        split = False
        pos = 0

        if len(node.suffix) == 1:
            pos = 1
        else:
            for letter in node.suffix:
                if pos > len(text) - text_pointer or text[text_pointer + pos] != letter:
                    # need to break here, the text and the stored suffix have
                    # diverged
                    split = True
                    break
                pos += 1

        text_pointer = text_pointer + pos
        if not split:
            # all the suffix text in this node matches

            if text_pointer == len(text):
                # done, pattern already exists
                break

            next_letter = text[text_pointer]
            if next_letter in node:
                # continue traversing
                node_id = node[next_letter]
                node = trie[node_id]
                continue
            else:
                remaining_text = text[text_pointer:]
                #log('Adding new node for {0}'.format(remaining_text))
                new = Node()
                node[next_letter] = count
                trie[count] = new
                new.suffix = remaining_text
                count += 1
                break

        # the node needs forked. need to consider the letters remaining
        # of the suffix stored on the node, and the remaining letters of the
        # text.
        current_letter = text[text_pointer]
        remaining_text = text[text_pointer:]
        remaining_suffix = node.suffix[pos:]
        consumed_suffix = node.suffix[0:pos]

        #log('Breaking current letter: {0} remaining text: {1} remaining suffix: {2} consumed: {3}'.format(current_letter,
        #    remaining_text, remaining_suffix, consumed_suffix))

        # make any adjustments to the stored suffix on the node
        # and give it a new id (old id used for branch node)
        node.suffix = remaining_suffix
        new_id = count
        count += 1
        trie[new_id] = node

        # replace this node with a branch
        branch = Node()
        trie[node_id] = branch
        branch.suffix = consumed_suffix
        branch[remaining_suffix[0]] = new_id

        # add new node for the remainder of the text
        new = Node()
        new_id = count
        count += 1
        trie[new_id] = new
        branch[current_letter] = new_id
        new.suffix = remaining_text
        break

def build_suffix_tree(text):
    trie = {}
    trie[0] = Node()
    length = len(text)
    start = datetime.now()
    for pos, suffix_len in zip(range(length-1, -1, -1), range(1, length+1)):
        update_trie(trie, text, pos)
    return trie

def build_suffix_array2(text):
  suffix_tree = build_suffix_tree(text)
  result = []

  def dft(text_length, node, suffix):
    if len(node) == 0:
      result.append(str(text_length - len(suffix)))
      return
    letters = sorted([(key, val) for key, val in node.items()], key=lambda x: x[0])
    for letter, val in letters:
      child = suffix_tree[val]
      dft(text_length, child, suffix + child.suffix)

  dft(len(text), suffix_tree[0], '')
  return result

def build_suffix_array(text):
  suffixes = [None]*len(text)
  for x in range(0, len(text)):
    suffixes[x] = (text[x:], x)

  sorted_suffixes = sorted(suffixes, key=lambda x: x[0])
  result = []
  for suff in sorted_suffixes:
    result.append(suff[1])
  return result


if __name__ == '__main__':
  text = sys.stdin.readline().strip()
  print(" ".join(map(str, build_suffix_array(text))))
