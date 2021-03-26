from collections import defaultdict
from os import system
import time
import argparse

'''
 c 0 1 2 3
r  _ _ _ _
0 |  _   $|
1 | |_|  !|
2 |_ _ _ _|
'''

# GridWorld Environment for MDP Value Iteration
class GridWorld:
    EXIT = (float("inf"), float("inf"))
    NORTH = (-1,  0)
    EAST  = ( 0, +1)
    SOUTH = (+1,  0)
    WEST  = ( 0, -1)
    DIRCS = [NORTH, EAST, SOUTH, WEST]
    index = {NORTH: 0, EAST: 1, SOUTH: 2, WEST: 3}
    GAMEOVER = (-1, -1)
    def __init__(self, shape, prob, walls, terminals):
        self.rows, self.cols = shape
        accident = (1 - prob) / 2
        self.turns = {-1: accident, 0: prob, +1: accident}
        self.walls = set(walls)
        self.terms = terminals

    def getStates(self):
        return [(i, j) for i in range(self.rows)
                    for j in range(self.cols) if (i, j) not in self.walls]

    def getTransitionStatesAndProbs(self, state, action):
        if state in self.terms:
            return [(GridWorld.GAMEOVER, 1.0)]

        result = []
        for turn in self.turns:
            dirc = GridWorld.DIRCS[(GridWorld.index[action] + turn) %
                    len(GridWorld.DIRCS)]
            row = state[0] + dirc[0]
            col = state[1] + dirc[1]
            landing = (row if 0 <= row < self.rows else state[0],
                        col if 0 <= col < self.cols else state[1])
            if landing in self.walls:
                landing = state
            prob = self.turns[turn]
            result.append( (landing, prob) )
        return result

    def getReward(self, state, action, nextState):
        if state in self.terms:
            return self.terms[state]
        else:
            return 0

    def isTerminal(self, state):
        return state == GridWorld.GAMEOVER

    def getLegalActions(self, state):
        if state in self.terms:
            return [GridWorld.EXIT]
        else:
            return GridWorld.DIRCS

    def printValues(self, values):
        output = str()
        divide = "\n" + "----------- " * self.cols + "\n"
        for i in range(self.rows):
            for j in range(self.cols):
                output += "   %+.2f   |" % values[(i, j)]
            output += divide
        print(output)

    
    def printPolicy(self, policy):
        actmap = { GridWorld.NORTH: '^', GridWorld.EAST: '>',
                GridWorld.SOUTH: 'v', GridWorld.WEST: '<' }
        divide = " _ _ _ _\n"
        actstrs = [actmap[policy[(0, j)]] for j in range(3)]
        first = '|' + ' '.join(actstrs) + " $|\n"
        actstrs = [actmap[policy[(1, j)]] for j in (0, 2)]
        second = "|" + actstrs[0] + "   " + actstrs[1] + " !|\n"
        actstrs = [actmap[policy[(2, j)]] for j in range(4)]
        third = '|' + ' '.join(actstrs) + "|\n"
        output = divide + first + second + third + divide
        print(output)


# Additive Grid Environment for MDP Value Iteration
class GridWorldAdditive(GridWorld):
    def __init__(self, shape, prob, walls, terminals, reward = -0.01):
        super(GridWorldAdditive, self).__init__(shape, prob, walls, terminals)
        self.reward = reward

    def getReward(self, state, action, nextState):
        if state in self.terms:
            return self.terms[state]
        else:
            return self.reward

clear = lambda: system('clear')

# MDP Value Iteration with Bellman update
class ValueIteration:
    def getQValueFromValues(self, mdp, state, action, values, discount):
        avg = 0
        for landing, prob in mdp.getTransitionStatesAndProbs(state, action):
            avg += prob * (mdp.getReward(state, action, landing) + discount * values[landing])
        return avg

    def valueIteration(self, mdp, discount = 0.9, iterations = 100):
        values = defaultdict(lambda: 0)
        for i in range(iterations):
            vnext = defaultdict(lambda: 0)
            for state in mdp.getStates():
                if not mdp.isTerminal(state):
                    maximum = float("-inf")
                    for action in mdp.getLegalActions(state):
                        qvalue = self.getQValueFromValues(mdp, state, action, values, discount)
                        maximum = max(maximum, qvalue)
                    vnext[state] = maximum
            values = vnext
            clear()
            print("Values after %d Iterations" %i)
            mdp.printValues(values)
            time.sleep(0.5)


        return values


    def getPolicy(self, mdp, values, discount = 0.9):
        policy = {}
        for state in mdp.getStates():
            if not mdp.isTerminal(state):
                maximum = -float("inf")
                for action in mdp.getLegalActions(state):
                    qvalue = self.getQValueFromValues(mdp, state, action, values, discount)
                    if qvalue > maximum:
                        maximum = qvalue
                        bestact = action
                policy[state] = bestact
        return policy

# Arguments
def parse_agrs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d','--discount', default=0.9, type=float)
    parser.add_argument('-p', '--prob', default=0.8, type=float)
    parser.add_argument('-r', '--livingReward', default=0, type=float)
    parser.add_argument('-i', '--iterations', default=10, type=int)
    return parser.parse_args()


# Run Value Iteration in different Grid World environments
if __name__ == "__main__":
    args = parse_agrs()

    gamma = args.discount
    prob = args.prob
    reward = args.livingReward
    iters = args.iterations

    terminals = {(0, 3): +1, (1, 3): -1}
    gw = GridWorldAdditive((3, 4), prob, [(1, 1)], terminals, reward)
    vi = ValueIteration()
    values = vi.valueIteration(gw, gamma, iters)

    print("Grid world Value Iteration with discounted rewards gamma = %.2f and reward = %.2f\n" % (gamma, reward))
    gw.printValues(values)
    policy = vi.getPolicy(gw, values, gamma)
    gw.printPolicy(policy)



