# python3
import sys

def InverseBWT(bwt):
    sorted_text = sorted(bwt)

    trans_array = []
    counts = {'A': 0, 'G': 0, 'C': 0, 'T': 0}
    for idx, letter in enumerate(sorted_text):
        if letter == '$':
            trans_array.append((letter,0))
            continue
        counts[letter] = counts[letter] + 1
        trans_array.append((letter, counts[letter]))

    nth_letter = {'A': [], 'G': [], 'C': [], 'T': [], '$': []}
    for idx, letter in enumerate(bwt):
        nth_letter[letter].append(idx)

    letter = sorted_text[0]
    sorted_pos = nth_letter[letter[0]][0]
    n = 0
    original = []
    while n < len(bwt):
        letter = trans_array[sorted_pos]
        original.append(letter[0])
        if letter == '$':
            sorted_pos = sorted_text.index('$')
        else:
            sorted_pos = nth_letter[letter[0]][letter[1]-1]
        n += 1

    return ''.join(original)

if __name__ == '__main__':
    bwt = sys.stdin.readline().strip()
    print(InverseBWT(bwt))