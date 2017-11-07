# python3
import sys


def preprocessBWT(bwt):
  sorted_text = sorted(bwt)

  bwt_array = []
  counts = {'A': 0, 'G': 0, 'C': 0, 'T': 0}
  for idx, letter in enumerate(bwt):
      if letter == '$':
          bwt_array.append((letter,0))
          continue
      counts[letter] = counts[letter] + 1
      bwt_array.append((letter, counts[letter]))


  sorted_map = {'A': [], 'G': [], 'C': [], 'T': [], '$': []}
  for idx, letter in enumerate(sorted_text):
      sorted_map[letter].append(idx)


  return bwt_array, sorted_map

def count_occurrences(pattern, bwt, bwt_array, sorted_map):
  occurs = sorted_map[pattern[-1]]
  if len(occurs) > 0:
    first = occurs[0]
    last = occurs[-1]
  else:
    return 0

  if len(pattern) == 1:
    return last - first + 1

  '''
  print(sorted(bwt))
  print(bwt)
  print(bwt_array)
  print(sorted_map)
  '''

  n = len(pattern) - 2 
  while n >= 0:
    letter = pattern[n]

    #print('first: {0} last: {1}'.format(first, last))
    # look for first and last occurrences in bwt
    first_match = None
    last_match = None
    for x in range(first, last+1):
      if first_match is None and bwt[x] == letter:
        first_match = x
        break

    if first_match is None:
      # can't continue, no matches
      return 0

    for x in range(last, first_match, -1):
      if bwt[x] == letter:
        last_match = x
        break

    # letter to look for in sorted array
    first_letter = bwt_array[first_match]
    if last_match == None:
      number_matches = 1
    else:
      last_letter = bwt_array[last_match]
      # matches are not necessarily consecutive in the segment
      # of bwt under insepection, so look for difference in positions
      # of the letter stored in the bwt array
      number_matches = last_letter[1] - first_letter[1] + 1 

    # pull out new first and last pointers
    first = sorted_map[first_letter[0]][first_letter[1]-1] 
    last = first + number_matches - 1
    n -= 1

  return last - first + 1


if __name__ == '__main__':
  bwt = sys.stdin.readline().strip()
  pattern_count = int(sys.stdin.readline().strip())
  patterns = sys.stdin.readline().strip().split()
  # Preprocess the BWT once to get starts and occ_count_before.
  # For each pattern, we will then use these precomputed values and
  # spend only O(|pattern|) to find all occurrences of the pattern
  # in the text instead of O(|pattern| + |text|).  
  bwt_array, sorted_map = preprocessBWT(bwt)
  occurrence_counts = []
  for pattern in patterns:
    occurrence_counts.append(count_occurrences(pattern, bwt, bwt_array, sorted_map))
  print(' '.join(map(str, occurrence_counts)))
