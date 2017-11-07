# python3

import collections

class Request:
    def __init__(self, arrival_time, process_time):
        self.arrival_time = arrival_time
        self.process_time = process_time


class Response:
    def __init__(self, dropped, start_time):
        self.dropped = dropped
        self.start_time = start_time


class Buffer:
    def __init__(self, size):
        self.size = size
        self.finish_time_ = []
        self.q = collections.deque([], size)
        # procssing start time of current request.
        self.start_time = None
        # the time required to elapse before the buffer is processed.
        self.current_wait = 0

    def Process(self, request):
        new_time = request.arrival_time
        q = self.q


        # move time forward, and process
        # the buffer.
        if len(q) > 0:
            current_request = q[len(q)-1]
            end_time = self.start_time + current_request.process_time
            while end_time <= new_time:
                popped = q.pop()
                self.current_wait -= popped.process_time
                if len(q) == 0:
                    break
                self.start_time = end_time
                current_request = q[len(q)-1]
                end_time = end_time + current_request.process_time

        if len(q) == self.size:
            return Response(True, -1)

        self.q.appendleft(request)
        if len(q) == 1:
            # start processing immediately
            self.start_time = new_time

        self.current_wait += request.process_time
        if len(q) > 0:
            processing_time = self.current_wait - (new_time - self.start_time)
        else:
            processing_time = self.current_wait

        return Response(False, new_time + processing_time - request.process_time)


def ReadRequests(count):
    requests = []
    for i in range(count):
        arrival_time, process_time = map(int, input().strip().split())
        requests.append(Request(arrival_time, process_time))
    return requests


def ProcessRequests(requests, buffer):
    responses = []
    for request in requests:
        responses.append(buffer.Process(request))
    return responses


def PrintResponses(responses):
    for response in responses:
        print(response.start_time if not response.dropped else -1)


if __name__ == "__main__":
    size, count = map(int, input().strip().split())
    requests = ReadRequests(count)

    buffer = Buffer(size)
    responses = ProcessRequests(requests, buffer)

    PrintResponses(responses)
