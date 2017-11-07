# python3
import sys


def find_pattern(pattern, text):
  """
  Find all the occurrences of the pattern in the text
  and return a list of all positions in the text
  where the pattern starts in the text.
  """
  pat_text = pattern + '$' + text

  prefixes = [None] * len(pat_text)

  prefixes[0] = 0
  border = 0
  matches = []
  for idx, letter in enumerate(pat_text[1:], start=1):
    while border > 0 and letter != pat_text[border]:
      border = prefixes[border - 1]
    if letter == pat_text[border]:
      border = border + 1
    else:
      border = 0

    if border == len(pattern):
      matches.append(idx - len(pattern) - border)
    prefixes[idx] = border

  return matches


if __name__ == '__main__':
  pattern = sys.stdin.readline().strip()
  text = sys.stdin.readline().strip()
  result = find_pattern(pattern, text)
  print(" ".join(map(str, result)))

