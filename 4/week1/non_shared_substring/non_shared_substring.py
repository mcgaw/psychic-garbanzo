# python3
import sys
import threading

sys.setrecursionlimit(1000000000) # max depth of recursion
threading.stack_size(2**29)  # new thread will get stack of such size

class Node(dict):

    def __init__(self):
        self.suffix = ''
        self.depth = 0
        self.distance = 0
        self.parent = None

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
    global count
    count = 1
    trie = {}
    trie[0] = Node()
    length = len(text)
    for pos, suffix_len in zip(range(length-1, -1, -1), range(1, length+1)):
        update_trie(trie, text, pos)
    result = []
    def trav_tree(node):
        if node == {}:
            result.append(node.suffix)
            return
        if node.suffix != '':
            result.append(node.suffix)
        for letter in node:
            trav_tree(trie[node[letter]])

    trav_tree(trie[0])
    trie[0].suffix = ''
    return trie

def solve (p, q):
    tree1 = build_suffix_tree(p+'$')
    tree2 = build_suffix_tree(q+'$')
    tree1[0].distance = 0
    tree1[0].depth = 0
    tree2[0].distance = 0
    tree2[0].depth = 0

    # {node, suffix_idx}
    ptr = (tree2[0], -1)
    min_found = None

    # depth first recurse on tree1 while holding a pointer
    # to tree2
    def dfr(node, tree_ptr):
        nonlocal min_found
        if min_found is not None and node.depth >= len(min_found):
            return

        suffix = node.suffix
        node2 = tree_ptr[0]
        suffix2 = node2.suffix
        ptr_idx = tree_ptr[1]

        # try move the pointer on tree2 forward for
        # each letter on this edge
        for idx, letter in enumerate(suffix):
            if ptr_idx == -1 or len(suffix2) <= ptr_idx:
                # pointing to new edge on tree2
                if letter in node2:
                    node2 = tree2[node2[letter]]
                    suffix2 = node2.suffix
                    if len(node2.suffix) <= 1:
                        ptr_idx = -1
                    else:
                        ptr_idx = 1
                    continue
            elif suffix2[ptr_idx] == letter:
                # carry on matching letters on this edge with
                # the edge pointed to on tree2
                ptr_idx += 1
                continue

            if letter == '$':
                return

            #print('mismatch of {0} on  {1} at {2}'.format(letter, node2, ptr_idx ))
            #print('while parsing pos {0} {1}'.format(idx, node.suffix))
            #print('')
            # string in 1 but not in 2
            shortest = list(node.suffix[0:idx+1])
            temp = node.parent
            while temp != None:
                shortest = list(temp.suffix) + shortest
                temp = temp.parent
            found = "".join(shortest)
            min_found = found if min_found is None or (len(found) < len(min_found)) else min_found
            return

        for n in node:
            child = tree1[node[n]]
            child.parent = node
            child.depth = node.depth + len(node.suffix)
            dfr(child, (node2, ptr_idx))
        return

    dfr(tree1[0], ptr)
    return min_found

p = sys.stdin.readline ().strip ()
q = sys.stdin.readline ().strip ()

ans = solve (p, q)

sys.stdout.write (ans + '\n')
