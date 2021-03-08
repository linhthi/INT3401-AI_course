import random
import torch
import time

# Set random seed
def global_seed(random_seed):
    torch.manual_seed(random_seed + 1)
    random.seed(random_seed + 10)


class Board:

    def __init__(self, N, start, time_limit=60):
        self.N = N

        # Flag for break
        self.found = False

        self.Q = [-1 for i in range(N)]

        self.col = [0 for i in range(N)]
        self.d1 = [0 for i in range(2*N - 1)]
        self.d2 = [0 for i in range(2*N - 1)]

        self.start_time = time.time()
        self.time_limit = time_limit
        self.add(0, start)

    def add(self, i, pos):

        self.Q[i] = pos
        self.col[pos] = 1
        self.d1[i + pos] = 1
        self.d2[i - pos + self.N] = 1

    def remove(self, i, pos):
        self.col[pos] = 0
        self.d1[i + pos] = 0
        self.d2[i - pos + self.N] = 0

    def check_condition(self, i, pos):
        return (self.col[pos] == 0) and\
               (self.d1[i + pos] == 0) and\
               (self.d2[i - pos + self.N] == 0)

    # Iterated to place the queen row i
    def run_backtracking(self, i):

        if time.time() - self.start_time > self.time_limit:
            print('Run in: ', time.time() - self.start_time )
            print('Time Limit Exceed')
            return True

        if i == self.N:
            # Return the config

            self.found = True
            return True

        for j in range(self.N):
            if self.check_condition(i, j):
                self.add(i, j)
                if self.run_backtracking(i+1):
                    return True

                self.remove(i, j)

        return False


if __name__ == "__main__":

    # size = int(sys.argv[1])
    # start_pos = int(sys.argv[2])

    n = 22
    start = 1

    # Run example
    board = Board(N=n, start=start)
    board.run_backtracking(1)
    print('Run in: ', time.time() - board.start_time)

    with open("output.txt", "w") as f:
        f.write("%i %i\n" % (n, start))
        for k in range(n):
            f.write("%i\n" % board.Q[k])
