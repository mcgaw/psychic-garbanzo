# python3
import sys

def build_trie(patterns):
    tree = {}
    tree[0] = {}
    count = 1
    for pattern in patterns:
        node = tree[0]
        for letter in pattern:
            if letter in node:
                node = tree[node[letter]]
            else:
                node[letter] = count
                tree[count] = {}
                node = tree[count]
                count += 1

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
			count += 1
			if count >= len(text):
				break
			letter = text[count]

		if node == {}:
			matches.append(start)

	return matches

text = sys.stdin.readline ().strip ()
n = int (sys.stdin.readline ().strip ())
patterns = []
for i in range (n):
	patterns += [sys.stdin.readline ().strip ()]

ans = solve (text, n, patterns)

sys.stdout.write (' '.join (map (str, ans)) + '\n')
