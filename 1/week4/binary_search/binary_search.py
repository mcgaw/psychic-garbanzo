# Uses python3
import sys

def binary_search(a, x):
    left = 0
    right = len(a) - 1

    def search(left, right, a, x):
        n = right - left

        if n == 0:
            return left if a[left] == x else -1 

        mid = left + n//2

        if a[mid] >= x:
            return search(left, mid, a, x)
        else:
            return search(mid + 1, right, a, x)

    return search(left, right, a, x)


def linear_search(a, x):
    for i in range(len(a)):
        if a[i] == x:
            return i
    return -1

if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n = data[0]
    m = data[n + 1]
    a = data[1 : n + 1]
    for x in data[n + 2:]:
        # replace with the call to binary_search when implemented
        #print(linear_search(a, x), end = ' ')
        print(binary_search(a, x), end = ' ')
