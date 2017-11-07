# Uses python3
import sys
import random

def partition3(a, l, r):
    x = a[l] # pivot
    j = l # upper index of elements equal to pivot
    k = l # lower index of elements equal to pivot

    # elements to the right of k are equal or greater than
    # the pivot.
    # elements to the right of j are greater than the pivot
    for i in range(l + 1, r + 1):
        if a[i] < x:
            # move ith element to the bottom of the sequence
            # of identical elements then replace it with either
            # a swap or the first element after the identical
            # elements.
            temp = a[k+1]
            a[k+1] = a[i]
            if k != j:
                # swap with element after identical elements
                a[i] = a[j+1]
                a[j+1] = temp
            else:
                # simple swap
                a[i] = temp
            j += 1
            k += 1
        elif a[i] == x:
            j += 1
            a[i], a[j] = a[j], a[i]
    a[l], a[k] = a[k], a[l]
    return k, j


def partition2(a, l, r):
    x = a[l]
    j = l;
    for i in range(l + 1, r + 1):
        if a[i] <= x:
            j += 1
            a[i], a[j] = a[j], a[i]
    a[l], a[j] = a[j], a[l]
    return j


def randomized_quick_sort(a, l, r):
    if l >= r:
        return
    k = random.randint(l, r)
    a[l], a[k] = a[k], a[l]
    #use partition3
    n, m = partition3(a, l, r)
    randomized_quick_sort(a, l, n - 1);
    randomized_quick_sort(a, m + 1, r);


if __name__ == '__main__':
    input = sys.stdin.read()
    n, *a = list(map(int, input.split()))
    randomized_quick_sort(a, 0, n - 1)
    for x in a:
        print(x, end=' ')
