from search import *
from node import Node
from problem import Problem
from eight_puzzle import EightPuzzle

if __name__== '__main__':
    puzzle = EightPuzzle((2, 4, 3, 1, 5, 6, 7, 8, 0))
    puzzle.check_solvability((2, 4, 3, 1, 5, 6, 7, 8, 0))

    breadth_first_tree_search(puzzle)
    depth_first_tree_search(puzzle)
    astar_search(puzzle).solution()

    
