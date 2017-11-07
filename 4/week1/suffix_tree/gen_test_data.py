

with open('long_input.txt', 'w') as f:
    for _ in range(0, 500):
        f.write('AAAAAAAAAA')
    f.write('$')