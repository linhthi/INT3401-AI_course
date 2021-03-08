import random
import time
import math


class Board():

    def __init__(self, N):
        self.N = N
        self.board = []  # Stores the board
        self.r_conflicts = [0] * (N)  # Row conflicts
        self.dr_conflicts = [0] * ((2 * N) - 1)  # Right diagonal conflicts
        self.dl_conflicts = [0] * ((2 * N) - 1)  # Left diagonal conflicts

    def changeConflicts(self, col, row, val):
        self.r_conflicts[row] += val
        self.dr_conflicts[col + row] += val
        self.dl_conflicts[col + (self.N - row - 1)] += val

    def numConflicts(self, col, row):
        return self.r_conflicts[row] \
               + self.dr_conflicts[col + row] \
               + self.dl_conflicts[col + (self.N - row - 1)]

    def minConflictPos(self, col):
        minConflicts = self.N
        minConflictRows = []

        for row in range(self.N):
            conflicts = self.numConflicts(col, row)
            if conflicts == 0:
                return row

            if conflicts < minConflicts:
                minConflictRows = [row]
                minConflicts = conflicts

            elif conflicts == minConflicts:
                minConflictRows.append(row)

        choice = random.choice(minConflictRows)
        return choice

    # Sets up the board using a greedy algorithm
    def createBoard(self):

        # an ordered set of all possible row values
        rowSet = set(range(0, self.N))

        # a list to keep track of which queens have not been placed
        notPlaced = []

        for col in range(0, self.N):
            # Pop the next possible row location to test
            testRow = rowSet.pop()
            conflicts = self.numConflicts(col, testRow)

            if conflicts == 0:
                self.board.append(testRow)
                self.changeConflicts(col, self.board[col], 1)

            else:
                rowSet.add(testRow)
                testRow2 = rowSet.pop()
                conflicts2 = self.numConflicts(col, testRow2)

                if conflicts2 == 0:
                    self.board.append(testRow2)
                    self.changeConflicts(col, self.board[col], 1)

                else:
                    rowSet.add(testRow2)
                    self.board.append(None)
                    notPlaced.append(col)

        for col in notPlaced:
            self.board[col] = rowSet.pop()
            self.changeConflicts(col, self.board[col], 1)

    # Finds the column has max conflicts
    def findMaxConflictCol(self):
        conflicts = 0
        maxConflicts = 0
        maxConflictCols = []

        for col in range(0, self.N):
            row = self.board[col]
            conflicts = self.numConflicts(col, row)

            if (conflicts > maxConflicts):
                maxConflictCols = [col]
                maxConflicts = conflicts

            elif conflicts == maxConflicts:
                maxConflictCols.append(col)

        choice = random.choice(maxConflictCols)
        return choice, maxConflicts


# Sets up the board using createBoard() and then solves it with a min-conflict algorithm
def solveNQueens(N):
    b = Board(N)
    b.createBoard()
    iteration = 0
    maxIteration = 0.6 * N  # Define the maximum iterations as 0.6 * size of board

    while (iteration < maxIteration):
        col, numConflicts = b.findMaxConflictCol()

        if (numConflicts > 3):
            newLocation = b.minConflictPos(col)

            if (newLocation != b.board[col]):
                b.changeConflicts(col, b.board[col], -1)
                b.board[col] = newLocation
                b.changeConflicts(col, newLocation, 1)

        elif numConflicts == 3:  # It means only queen in that position
            return (True, b.board)

        iteration += 1
    return (False, -1)


def writeToFile(board):
    with open('output.txt', 'w') as f:
        f.write("%i %i\n" % (len(board), board[0]))
        for x in range(len(board)):
            f.write("%i\n" % board[x])
    f.close()


def main():
    N = 1000

    start = time.time()
    solved = False
    print("Searching for board configuration of size %i ..." % N)

    while (not solved):
        solved, board = solveNQueens(N)

    print("Board configuration found for size %i" % N)

    writeToFile(board)
    end = time.time()
    print(end - start)


if __name__ == '__main__':
    main()
