# python3
import sys

def BWT(text):
    rotations = sorted([text[x:]+text[:x] for x in range(0, len(text))])
    return ''.join([rotation[len(text)-1] for rotation in rotations])

if __name__ == '__main__':
    text = sys.stdin.readline().strip()
    print(BWT(text))