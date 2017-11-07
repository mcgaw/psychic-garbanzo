# python3
from datetime import datetime

def read_input():
    return (input().rstrip(), input().rstrip())

def print_occurrences(output):
    print(str(len(output))) 
    #print(' '.join(map(str, output)))

def get_occurrences(pattern, text):

    # x and p term of poly hash function
    poly_hash_x = 1 
    poly_hash_p = 1000000000 + 7

    def compute_hash(s):
        result = 3 
        for power, char in enumerate(s):
            result += ord(char)*(pow(poly_hash_x, power)) % poly_hash_p

        return result % poly_hash_p

    def compute_hashes(pattern, text):
        last_comparison_pos = len(text) - len(pattern)

        if last_comparison_pos < 0:
            return []

        text_hashes = [None for _ in range(0, last_comparison_pos+1)]

        assert(len(text_hashes) == len(text)-len(pattern) + 1)

        # compute first hash fully to form base of comparisons
        text_hashes[len(text_hashes)-1] = compute_hash(text[last_comparison_pos:])

        # coeff of last term in hash of pattern
        last_coeff = 1
        for _ in range(1, len(pattern)+1):
            last_coeff = last_coeff * poly_hash_x % poly_hash_p

        if len(pattern) == len(text):
            return text_hashes

        for idx, char in enumerate(text[last_comparison_pos-1::-1]):
            i = idx + 1
            text_hashes[-(i+1)] = (poly_hash_x * text_hashes[-i]  \
               + ord(char) - (last_coeff * ord(text[-i]))) % poly_hash_p

        #for i in range(last_comparison_pos-1, -1, -1):
        #    text_hashes[i] = (poly_hash_x * text_hashes[i+1] \
        #        + ord(text[i]) - (last_coeff * ord(text[i+len(pattern)]))) % poly_hash_p

        return text_hashes

    pattern_hash = compute_hash(pattern)
    start = datetime.now()
    print('starting...')
    hashes = compute_hashes(pattern, text)

    matches = []
    for pos, hash_ in enumerate(hashes):
        if hash_ == pattern_hash and pattern == text[pos: pos+len(pattern)]:
            matches.append(pos)

    elapsed = (datetime.now() - start)
    print('finished matching text in {0}'.format(elapsed))
    return matches

if __name__ == '__main__':
    print_occurrences(get_occurrences(*read_input()))

