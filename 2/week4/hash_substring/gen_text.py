text = ''.join('abRjaOnaiab' for _ in range(500000))
pattern = ''.join('abRjaOnaiab' for _ in range(50))

with open('large_input', mode='w') as file:
    file.write(pattern + '\n')
    file.write(text)