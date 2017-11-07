# python3

import sys
import threading

sys.setrecursionlimit(10**7)  # max depth of recursion
threading.stack_size(2**27)  # new thread will get stack of such size


class Node:
    def __init__(self, label, parent=None, children=None):
        self.parent = parent
        if children is None:
            self.children = []
        else:
            self.children = children
        self.label = label

    def add_child(self, node):
        self.children.append(node)

    def set_parent(self, node):
        self.parent = node

    def __repr__(self):
        return '{0} -> {1}'.format(self.parent.label
                                   if self.parent else 'None',
                                   [child.label for child in self.children])


class TreeHeight:

    root = None
    nodes = None
    max_height = 0

    def read(self):
        self.n = int(sys.stdin.readline())
        parents = list(map(int, sys.stdin.readline().split()))

        # build tree
        root = None
        nodes = [None for i in range(0, self.n)]
        for i, parent in enumerate(parents):
            node = nodes[i]
            if node is None:
                nodes[i] = Node(str(i))
                node = nodes[i]

            if parent == -1:
                root = node
            else:
                if nodes[parent] is None:
                    nodes[parent] = Node(str(parent), children=[node])
                else:
                    nodes[parent].add_child(node)
                node.set_parent(nodes[parent])
            #print(nodes)
        self.nodes = nodes
        self.root = root

    def compute_height(self):
        def traverse(node, current_height):
            if node.children == []:
                if current_height > self.max_height:
                    self.max_height = current_height
                return

            for child in node.children: 
                traverse(child, current_height + 1)

        traverse(self.root, 1)
        return self.max_height


def main():
    tree = TreeHeight()
    tree.read()
    print(tree.compute_height())


threading.Thread(target=main).start()
