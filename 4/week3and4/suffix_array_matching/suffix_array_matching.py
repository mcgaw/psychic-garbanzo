# python3
import sys
import math

char_value = {'$': 0, 'A' : 1, 'C' : 2, 'G' : 3, 'T' : 4}
value_char = ['$', 'A', 'C', 'G', 'T']

def sort_chars(text):
  """
  Compute the order array of text. The order array represents the
  ordered text. Each position of the order array stores the position
  of the char in the text array. Count sort is used to create the
  order array.
  """

  counts = [0] * len(char_value)

  for char in text:
    counts[char_value[char]] += 1
  for j in range(1, len(char_value)):
    counts[j] =  counts[j] + counts[j-1]

  order = [None] * len(text)
  for i in range(len(text)-1, -1, -1):
    char = text[i]
    counts[char_value[char]] = counts[char_value[char]] - 1
    order[counts[char_value[char]]] = i
  return order

def classes(orders, text):
  """
  Compute the class array for text. For each position in the text
  the corresponding class array position stores a class number. The
  class numbers represent different characters, established by
  going through the text in order and incrementing the class number
  when a different character is found.
  """
  class_array = [None] * len(orders)
  class_array[orders[0]] = 0

  for i in range(1, len(text)):
    if text[orders[i]] != text[orders[i-1]]:
      class_array[orders[i]] = class_array[orders[i-1]] + 1
    else:
      class_array[orders[i]] = class_array[orders[i-1]]
  return class_array

def double_sort(text, l, order, class_array):
  """
  Produce the new order array based on doubling the cyclic shift.
  This is completed in linear time by using the class array for
  the original cyclic shift to determine the new order of the double
  cyclic shift.
  The actual letters of the double cyclic shifts are never actually
  examined.
  """
  counts = [0] * len(text)
  new_order = [None] * len(text)

  # setup the count sort with the order from the sorted
  # right hand side of the double shift. this is the order
  # of the double shifts before reverse order processing.
  for i in range(0, len(text)):
    counts[class_array[i]] = counts[class_array[i]] + 1  
  for j in range(1, len(text)):
    counts[j] = counts[j-1] + counts[j]

  # reverse traverse the imaginary list of double shifs
  # and finish the count sort using the class of the
  # first part of the double shift (unsorted)
  for i in range(len(text) - 1, -1, -1):
    # start is L to the left
    start = (order[i] - l + len(text)) % len(text)
    # the corresponding class for the L characters
    # starting from start.
    cl = class_array[start]
    # ? 
    counts[cl] = counts[cl] - 1
    new_order[counts[cl]] = start

  return new_order

def update_classes(order, class_array, l):
  """
  Produce the new class array. This is achieved by processing an
  'imaginary' 2xlen(order) matrix of classes based on the original
  class array. In each iteration both the 'left' and 'right' class
  numbers are examined to determine a change in the new class array.
  """
  n = len(order)
  new_class =  [None] * n
  new_class[order[0]] = 0

  for i in range(1, n):
    cur = order[i]
    prev = order[i-1]
    mid = (cur + l) % n
    mid_prev = (prev + l) % n
    if class_array[cur] != class_array[prev] or\
      class_array[mid] != class_array[mid_prev]:
        new_class[cur] = new_class[prev] + 1
    else:
      new_class[cur] = new_class[prev]

  return new_class

def build_suffix_array(text):
  """
  Build suffix array of the string text and
  return a list result of the same length as the text
  such that the value result[i] is the index (0-based)
  in text where the i-th lexicographically smallest
  suffix of text starts.
  """
  order = sort_chars([ch for ch in text])
  class_array = classes(order, text)

  l = 1
  while l < len(text):
    order = double_sort(text, l, order, class_array)
    class_array = update_classes(order, class_array, l)
    l = 2 * l

  return order

def compare_strings(pattern, text, suffix_pos):
  for i, char in enumerate(pattern):
    if text[i + suffix_pos] == '$':
      return 1
    if char == text[i + suffix_pos]:
      continue
    if char < text[i + suffix_pos]:
      return -1
    else:
      return 1

  # pattern was exact match of whole of right or
  # prefix of right
  return 0

def find_matches(suff_arr, text, pattern):
  #print('finding {0} in {1} using {2}'.format(pattern, text, suff_arr))
  min_index = 0
  max_index = len(text) - 1

  while min_index < max_index:
    mid_index = (min_index + max_index) // 2
    if compare_strings(pattern, text, suff_arr[mid_index]) > 0:
      min_index = mid_index + 1
    else:
      max_index = mid_index
  start = min_index

  s = suff_arr[start]
  if pattern != text[s:s+len(pattern)]:
    return -1

  #print('start {0}'.format(start))
  max_index = len(text) - 1
  while min_index < max_index:
    mid_index = (min_index + max_index) // 2
    #print('min {0} max {1} mid {2}'.format(min_index, max_index, mid_index))
    if compare_strings(pattern, text, suff_arr[mid_index]) < 0:
      max_index = mid_index
    else:
      min_index = mid_index + 1

  s = suff_arr[max_index]
  if pattern == text[s:s+len(pattern)]:
    end = max_index
  else:
    end = max_index - 1

  if start > end:
    return -1
  else:
    positions = []
    x = start
    while x <= end: 
    #for x in list(range(start, end + 1)):
      positions.append(suff_arr[x])
      x += 1
    return positions
 

def find_occurrences(text, patterns):

  text = text + '$'
  occs = set()

  suff_arr = build_suffix_array(text)
  for pattern in patterns:
    matches = find_matches(suff_arr, text, pattern)
    if matches != -1:
      for match in matches:
        occs.add(match)

  return occs

if __name__ == '__main__':
  text = sys.stdin.readline().strip()
  pattern_count = int(sys.stdin.readline().strip())
  patterns = sys.stdin.readline().strip().split()
  occs = find_occurrences(text, patterns)
  print(" ".join(map(str, occs)))