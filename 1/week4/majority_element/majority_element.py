# Uses python3
import sys

def get_majority_element(a, left, right):
    if left == right:
        return -1
    if left + 1 == right:
        return a[left]

    mid = left + (right-left)//2
    left_hand = get_majority_element(a, left, mid)
    right_hand = get_majority_element(a, mid, right)

    def scan_maj(poss):
        if poss == -1:
            return -1

        count = 0
        for i in a[left:right]:
            if i == poss:
                count += 1

        if count > (right-left)//2:
            return poss
        else:
            return -1

    if scan_maj(left_hand) > -1:
        return left_hand
    elif scan_maj(right_hand) > -1:
        return right_hand
    else:
        return -1

if __name__ == '__main__':
    input = sys.stdin.read()
    n, *a = list(map(int, input.split()))
    maj = get_majority_element(a, 0, n)
    if maj != -1:
        print(1)
    else:
        print(0)

    #print("\nMajority number is " + str(maj))
