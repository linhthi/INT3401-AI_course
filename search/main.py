from search.search_strategy import *
from search.node import Node
from search.problem import Problem
from search.eight_puzzle import EightPuzzle
from search.car_environment import CarEnvironment

if __name__== '__main__':
    puzzle = EightPuzzle((2, 4, 3, 1, 5, 6, 7, 8, 0))
    puzzle.check_solvability((2, 4, 3, 1, 5, 6, 7, 8, 0))

    breadth_first_tree_search(puzzle)
    depth_first_tree_search(puzzle)
    astar_search(puzzle).solution()

    #TODO: solve car driving problem


    
