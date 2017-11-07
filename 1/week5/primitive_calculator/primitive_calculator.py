# Uses python3
import sys

def optimal_sequence(n):
    sequence = []
    # init n=1, takes 0 operations to get here
    sequence.append(0)

    for a in range(2, n+1):
        candidates = []
        if a % 3 == 0:
            candidates.append(sequence[(a // 3)-1])
        if a % 2 == 0:
            candidates.append(sequence[(a // 2)-1])
        candidates.append(sequence[a-2])

        sequence.append(min(candidates) + 1)

    # traverse back down the list to get one of the possible shortest sequences
    answer = []
    answer.append(n)
    a = n
    while a > 1:
        steps = sequence[a-1]

        # find an instance of steps - 1
        for b in range(a-1, 0, -1):
            if sequence[b-1] == steps - 1:
                answer.append(b)
                a = b
                break

    return reversed(answer)

input = sys.stdin.read()
n = int(input)
sequence = list(optimal_sequence(n))
print(len(sequence) - 1)
for x in sequence:
    print(x, end=' ')
