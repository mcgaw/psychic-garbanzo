# python3
import sys
import threading
from datetime import datetime

sys.setrecursionlimit(1000000000) # max depth of recursion
threading.stack_size(2**29)  # new thread will get stack of such size

debug = False

def log(mess):
    if debug == True:
        print(mess)

class Node(dict):

    def __init__(self):
        self.suffix = ''

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
        #log('--> '+text[text_pointer:])
        #log(str(node))
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

def check_tree(trie, suffix):
    print('!!!! checking trie for {0} !!!!'.format(suffix))
    def check(node, suffix):
        if suffix == '':
            return
        expected_consume = suffix[0:len(node.suffix)]
        if node.suffix != expected_consume:
            raise RuntimeError('verify pattern failed, checked {0} against {1}'.format(node.suffix, expected_consume))
        print(node)
        remain = suffix[len(node.suffix):]
        if len(remain) == 0:
            return
        next_node = node[remain[0]]
        check(trie[next_node], remain)

    check(trie[0], suffix)
    print('!!!! check passed !!!!')


def build_suffix_tree(text):
    trie = {}
    trie[0] = Node()
    length = len(text)
    start = datetime.now()
    for pos, suffix_len in zip(range(length-1, -1, -1), range(1, length+1)):
        #log('-----------')
        update_trie(trie, text, pos)
        #log('')
        #log(trie)
        #log('')
        if False:
            suffix = text[pos:pos+suffix_len]
            check_tree(trie, suffix)
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
    end = datetime.now()
    #print(end-start)
    #return []
    return result


if __name__ == '__main__':
    text = sys.stdin.readline().strip()
    result = build_suffix_tree(text)
    print("\n".join(result))