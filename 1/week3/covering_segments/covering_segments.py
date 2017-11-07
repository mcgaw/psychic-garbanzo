# Uses python3
import sys
from collections import namedtuple

Segment = namedtuple('Segment', 'start end')

def optimal_points(segments):

    # sort according to right hand point
    def end_coord(seg):
        return seg.end

    working = sorted(segments.copy(), key=end_coord)

    points = []
    while working:
        # safe to take the first segment's end
        # point as a point
        new_seg = working[0]
        del working[0]

        points.append(new_seg.end)

        # after the safe move find all the segments that are
        # crossed by this point
        walk = working.copy()
        for seg in walk:
            if seg.start <= new_seg.end and \
                seg.end >= new_seg.end:
                working.remove(seg)

    return points

if __name__ == '__main__':
    input = sys.stdin.read()
    n, *data = map(int, input.split())
    segments = list(map(lambda x: Segment(x[0], x[1]), zip(data[::2], data[1::2])))
    points = optimal_points(segments)
    print(len(points))
    for p in points:
        print(p, end=' ')
