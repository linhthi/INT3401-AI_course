from search.problem import Problem

class CarEnvironment(Problem):

    def __init__(self, start, goal, Vmax, walls):
        """ Define goal state and initialize a problem """
        super().__init__(start, goal)
        #TODO: 
        pass

    def result(self, state, action):
        #TODO: 
        pass
    
    def actions(self, state):
        #TODO: 
        pass

    def goal_test(self, state):
        #TODO:
        pass

    def path_cost(self, c, state1, action, state2):
        #TODO: 
        pass