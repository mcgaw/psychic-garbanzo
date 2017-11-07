# Uses python3

import random

n = int(input())
a = [int(x) for x in input().split()]
assert(len(a) == n)

def max_product(numbers):

    max1 = 0
    max2 = 0

    for i in numbers:
        if i > max1:
            max2 = max1
            max1 = i
        elif i > max2:
            max2 = i

    print(max1*max2)

max_product(a)

def stress_test(): 
    while(True):
        input_size = random.randint(1, 10)
        number = []
        for n in range(0, input_size):
            number.append(random.randint(1, 1000))