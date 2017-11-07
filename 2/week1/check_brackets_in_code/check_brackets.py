# python3

import sys

class Bracket:
    def __init__(self, bracket_type, position):
        self.bracket_type = bracket_type
        self.position = position

    def Match(self, c):
        if self.bracket_type == '[' and c == ']':
            return True
        if self.bracket_type == '{' and c == '}':
            return True
        if self.bracket_type == '(' and c == ')':
            return True
        return False

if __name__ == "__main__":
    text = sys.stdin.read().rstrip()

    answer = None
    opening_brackets_stack = []
    for i, next in enumerate(text):
        if next == '(' or next == '[' or next == '{':
            opening_brackets_stack.append(Bracket(next, i))

        if next == ')' or next == ']' or next == '}':
            if len(opening_brackets_stack) == 0:
                answer = str(i+1)
                break
            pop = opening_brackets_stack.pop()
            if not pop.Match(next):
                answer = str(i+1)
                break

    if not answer:
        if len(opening_brackets_stack) != 0:
            # got to end but some bracket not closed
            answer = str(opening_brackets_stack.pop().position+1)
        else:
            answer = 'Success'

    # Printing answer, write your code here
    print(answer)