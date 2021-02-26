"""
Solving 8puzzle with astar algorithm

Input files are plain text, written as 3 lines: the start state.
They must include the numbers 0-8, where 0 represents the empty space, and 1-8 the 8 tiles of the puzzle.
Here is an example of a properly formated state:
1 2 0
3 4 5
6 7 8
"""
import sys
import math
import heapq

INFINITY = 1e9
GOAL = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

def read_list_int(st):
    tmp = st.strip().split(' ')
    return [int(x.strip()) for x in tmp]

def read_input(input_file):
    """
    :param input_file:
    :return: matrix description 8 puzzle position
    """
    a = [[0 for _ in range(3)] for _ in range(3)]
    with open(input_file, "r") as f:
        for i in range(3):
            x = read_list_int(f.readline())
            for j in range(3):
                a[i][j] = x[j]
    return a
            

def is_goal(a,b):
    for i in range(3):
        for j in range(3):
            if a[i][j] != b[i][j]:
                return False
    return True

def swap(a,b):
    return(b,a)

def tile_switches_remaining(a,b):
    """number of tiles wrong
    :param a: current state
    :param b: goal
    """
    cost = 0
    for i in range(3):
        for j in range(3):
            if a[i][j] !=b [i][j] and a[i][j]!=0:
                cost += 1
    return cost

def mahattan_distance(a, b):
    """
    Mahatan distance
    :param a: current state
    :param b: goal
    """
    sum = 0
    for i in range(3):
        for j in range(3):
            tile = a[i][j]
            for m in range(3):
                for n in range(3):
                    if tile == b[m][n]:
                        sum += abs(i-m) + abs(j-n)
    return sum

def print_mat(a):
    """ Print matrix a """
    for i in range(3):
        for j in range(3):
            print(a[i][j], end=" ")
        print()

def copy_mat(a):
    """ Copy matrix a to matrix c and return it """
    c =[[0 for i in range(3)] for j in range(3)]
    for i in range(3):
        for j in range(3):
            c[i][j] = a[i][j]
    return c

def to_str(a):
    """ Convert a matrix to string """
    l = ''
    for i in range(3):
        for j in range(3):
            l += str(a[i][j])
    return l

def to_mat(l):
    """ Convert a string to matrix"""
    a = [[0 for _ in range(3)] for _ in range(3)]
    cnt = 0
    for i in range(3):
        for j in range(3):
            a[i][j] = int(l[cnt])
            cnt += 1
    return a

def get_index_blank(a):
    x, y = (-1, -1)
    for i in range(3):
        for j in range(3):
            if a[i][j] == 0:
                x, y = (i, j)
    return x, y


def astar(a, b, h):
    """ Astar algorithm for 8 puzzle problem
    params:
    a: initial state
    b: goal state
    h: heristic function
    """

    start_state = to_str(a)

    # Use list as heap
    Q = [(0, start_state)]

    # Check visited status
    visited = set()
    visited.add(start_state)
    temp_cost = dict()
    temp_cost[start_state] = 0
    g = 0

    while len(Q) > 0:
        node = heapq.heappop(Q)
        cost = node[0]
        p = to_mat(node[1])
        g += 1
        print(p)

        if is_goal(p, b):
            return (cost, g - 1, len(visited))
        
        x, y = get_index_blank(p)

        # Move Down
        if x < 2:
            ad = copy_mat(p)
            ad[x][y], ad[x+1][y] = swap(ad[x][y], ad[x+1][y])
            new_cost = cost + g + h(ad, b)
            next = to_str(ad)

            if next not in visited:
                if new_cost < temp_cost.get(next, INFINITY):
                    visited.add(next)
                    temp_cost[next] = new_cost
                    heapq.heappush(Q, (new_cost, next))
           
        # Move Up
        if x > 0:
            au = copy_mat(p)
            au[x][y], au[x-1][y] = swap(au[x][y], au[x-1][y])
            new_cost = cost + g + h(au, b)
            next = to_str(au)

            if next not in visited:
                if new_cost < temp_cost.get(next, INFINITY):
                    visited.add(next)
                    temp_cost[next] = new_cost
                    heapq.heappush(Q, (new_cost, next))
                
        # Move Right
        if y < 2:
            ar = copy_mat(p)
            ar[x][y], ar[x][y+1] = swap(ar[x][y], ar[x][y+1])
            new_cost = cost + g + h(ar, b)
            next = to_str(ar)
        
            if next not in visited:
                if new_cost < temp_cost.get(next, INFINITY):
                    visited.add(next)
                    temp_cost[next] = new_cost
                    heapq.heappush(Q, (new_cost, next))
                    
        # Move left
        if y > 0:
            al = copy_mat(p)
            al[x][y], al[x][y-1] = swap(al[x][y], al[x][y-1])
            new_cost = cost + g + h(al,b)
            next = to_str(al)

            if next not in visited:
                if new_cost < temp_cost.get(next, INFINITY):
                    visited.add(next)
                    temp_cost[next] = new_cost
                    heapq.heappush(Q, (new_cost, next))

    return (-1, -1, -1)



############################################ Main ###################################################################################
if __name__ == '__main__':
    heristic = sys.argv[2]
    if heristic == 'mahattan_distance':
        h = mahattan_distance
    elif heristic == 'tile_switches_remaining':
        h = tile_switches_remaining
    else: h = mahattan_distance
    cost, step, num_node = astar(read_input(input_file=sys.argv[1]), GOAL, h)
    print("Cost: {0}, step: {1}, total nodes expanded: {2}".format(cost, step, num_node))
