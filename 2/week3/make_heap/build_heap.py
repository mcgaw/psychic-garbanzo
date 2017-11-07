# python3

class HeapBuilder:
  def __init__(self):
    self._swaps = []
    self._data = []

  def ReadData(self):
    n = int(input())
    self._data = [int(s) for s in input().split()]
    assert n == len(self._data)

  def WriteResponse(self):
    print(len(self._swaps))
    for swap in self._swaps:
      print(swap[0], swap[1])

  def GenerateSwaps(self):
    # The following naive implementation just sorts 
    # the given sequence using selection sort algorithm
    # and saves the resulting sequence of swaps.
    # This turns the given array into a heap, 
    # but in the worst case gives a quadratic number of swaps.
    #
    # TODO: replace by a more efficient implementation

    for i in range(len(self._data)):
      for j in range(i + 1, len(self._data)):
        if self._data[i] > self._data[j]:
          self._swaps.append((i, j))
          self._data[i], self._data[j] = self._data[j], self._data[i]

  def generate_swaps(self):
    size = len(self._data)
    for i in range(size//2, -1, -1):
      val = self._data[i]

      # sift down, min heap
      def sift_down(heap, idx, val):
        #print(self._swaps)
        left = 2*idx+1
        right = 2*idx+2
        left_diff = 0 
        right_diff = 0 
        if left <= size-1 and val > heap[left]:
          left_diff = val - heap[left]
        if right <= size-1 and val > heap[right]:
          right_diff = val - heap[right]

        target = None
        if right_diff > left_diff:
          target = right
        elif left_diff > right_diff:
          target = left
        if target:
          temp = heap[idx] 
          self._swaps.append((idx, target))
          heap[idx] = heap[target]
          heap[target] = temp
          sift_down(heap, target, val)

      sift_down(self._data, i, val)

  def Solve(self):
    self.ReadData()
    #self.GenerateSwaps()
    self.generate_swaps()
    self.WriteResponse()

if __name__ == '__main__':
    heap_builder = HeapBuilder()
    heap_builder.Solve()
