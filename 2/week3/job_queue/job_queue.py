# python3

from heapq import heappush, heappop, heapreplace

class JobQueue:
    def read_data(self):
        self.num_workers, m = map(int, input().split())
        self.jobs = list(map(int, input().split()))
        assert m == len(self.jobs)

    def write_response(self):
        for i in range(len(self.jobs)):
          print(self.assigned_workers[i], self.start_times[i]) 

    def _assign_jobs(self):
        # TODO: replace this code with a faster algorithm.
        self.assigned_workers = [None] * len(self.jobs)
        self.start_times = [None] * len(self.jobs)
        next_free_time = [0] * self.num_workers
        for i in range(len(self.jobs)):
          next_worker = 0
          for j in range(self.num_workers):
            if next_free_time[j] < next_free_time[next_worker]:
              next_worker = j
          self.assigned_workers[i] = next_worker
          self.start_times[i] = next_free_time[next_worker]
          next_free_time[next_worker] += self.jobs[i]

    def assign_jobs(self):
        self.assigned_workers = [] #[None] * len(self.jobs)
        self.start_times = [] #[None] * len(self.jobs)

        # two priority q's to store threads
        # priority  based on finishing time
        working_threads  = []
        # priority based on thread number
        free_threads = []

        # all threads available into the pool
        for i in range(self.num_workers):
            heappush(free_threads, (0, i))

        simulation_time = 0

        def process_job(job, thread_number):
            #print('processing job {0} on thread {1}'.format(job, thread_number))
            self.assigned_workers.append(thread_number)
            self.start_times.append(simulation_time)
            heappush(working_threads, (simulation_time+job, thread_number))

        for job in self.jobs:
            if len(free_threads) > 0:
                # can start immediately
                (_, thread_number) = heappop(free_threads)
                process_job(job, thread_number)
                continue

            # move simulation time forward to get the next available
            # thread
            (finish_time, thread_number) = heappop(working_threads)
            #print('thread {0} finished at {1}'.format(thread_number, finish_time))
            simulation_time = finish_time
            process_job(job, thread_number)


    def solve(self):
        self.read_data()
        self.assign_jobs()
        self.write_response()

if __name__ == '__main__':
    job_queue = JobQueue()
    job_queue.solve()

