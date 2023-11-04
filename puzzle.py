from __future__ import division
from __future__ import print_function

import sys
import math
import time
import queue as Q
import resource

#### SKELETON CODE ####
## The Class that Represents the Puzzle
class PuzzleState(object):
    """
        The PuzzleState stores a board configuration and implements
        movement instructions to generate valid children.
    """
    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        """
        :param config->List : Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        """
        if n*n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")
        if set(config) != set(range(n*n)):
            raise Exception("Config contains invalid/duplicate entries : ", config)

        self.n        = n
        self.cost     = cost
        self.parent   = parent
        self.action   = action
        self.config   = config
        self.children = []

        # Get the index and (row, col) of empty block
        self.blank_index = self.config.index(0)

    def display(self):
        """ Display this Puzzle state as a n*n board """
        for i in range(self.n):
            print(self.config[3*i : 3*(i+1)])

    def move_up(self):
        if self.blank_index <= 2:
            return None
        config = self.config[:]
        temp = config[self.blank_index]
        config[self.blank_index] = config[self.blank_index - 3]
        config[self.blank_index - 3] = temp
        return PuzzleState(config, 3, parent=self, action="Up", cost=self.cost+1)
        

        """ 
        Moves the blank tile one row up.
        :return a PuzzleState with the new configuration
        """
      
    def move_down(self):
        if self.blank_index >= 6:
            return None
        config = self.config[:]
        temp = config[self.blank_index]
        config[self.blank_index] = config[self.blank_index + 3]
        config[self.blank_index + 3] = temp
        return PuzzleState(config, 3, parent=self, action="Down", cost=self.cost+1)

        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """
      
    def move_left(self):
        if self.blank_index == 0 or self.blank_index == 3 or self.blank_index == 6:
            return None
        config = self.config[:]
        temp = config[self.blank_index]
        config[self.blank_index] = config[self.blank_index - 1]
        config[self.blank_index - 1] = temp
        return PuzzleState(config, 3, parent=self, action="Left", cost=self.cost+1)

        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """

    def move_right(self):
        if self.blank_index == 2 or self.blank_index == 5 or self.blank_index == 8:
            return None
        config = self.config[:]
        temp = config[self.blank_index]
        config[self.blank_index] = config[self.blank_index + 1]
        config[self.blank_index + 1] = temp
        return PuzzleState(config, 3, parent=self, action="Right", cost=self.cost+1)

        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """

    def expand(self):
        """ Generate the child nodes of this node """
        
        # Node has already been expanded
        if len(self.children) != 0:
            return self.children
        
        # Add child nodes in order of UDLR
        children = [
            self.move_up(),
            self.move_down(),
            self.move_left(),
            self.move_right()]

        # Compose self.children of all non-None children states
        self.children = [state for state in children if state is not None]
        return self.children

# Function that Writes to output.txt

### Students need to change the method to have the corresponding parameters
def writeOutput(output):
    with open('output.txt', 'w') as f:
        f.write("path_to_goal: " + str(get_path(output[0])) + "\n")
        f.write("cost_of_path: " + str(output[0].cost) + "\n")
        f.write("nodes_expanded: " + str(len(output[2]) - 1) + "\n")
        f.write("search_depth: " + str(output[0].cost) + "\n")
        f.write("max_search_depth: " + str(output[1]) + "\n")
        f.write("running_time: " + format(output[4], '.8f') + "\n")
        f.write("max_ram_usage: " + format(output[3], '.8f') + "\n")


def bfs_search(initial_state):
    frontier = Q.Queue()
    frontier.put(initial_state)
    nodes_expanded = 0
    max_search_depth = 0
    explored = set()
    bfs_start_ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    start_time = time.time()
    while frontier:
        state = frontier.get()
        explored.add(tuple(state.config))
        if test_goal(state):
            temp = []
            temp.append(state)
            temp.append(max_search_depth)
            temp.append(explored)
            bfs_ram = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - bfs_start_ram)/(2**20)
            runtime = time.time() - start_time
            temp.append(bfs_ram)
            temp.append(runtime)
            return temp
        children = state.expand()
        nodes_expanded += 1
        for child in children:
            if tuple(child.config) not in explored:
                frontier.put(child)
                if child.cost > max_search_depth:
                    max_search_depth = child.cost
    return None

def dfs_search(initial_state):
    frontier = Q.LifoQueue()
    frontier.put(initial_state)
    frontier_set = set()
    frontier_set.add(tuple(initial_state.config))
    nodes_expanded = 0
    max_search_depth = 0
    explored = set()
    start_time = time.time()
    dfs_start_ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    while not frontier.empty():
        state = frontier.get()
        frontier_set.remove(tuple(state.config))
        explored.add(tuple(state.config))
        if test_goal(state):
            temp = []
            temp.append(state)
            temp.append(max_search_depth)
            temp.append(explored)
            runtime = time.time() - start_time
            dfs_ram = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - dfs_start_ram)/(2**20)
            temp.append(dfs_ram)
            temp.append(runtime)
            return temp
        children = state.expand()[::-1]
        nodes_expanded += 1
        for child in children:
            if tuple(child.config) not in explored and tuple(child.config) not in frontier_set:
                frontier.put(child)
                frontier_set.add(tuple(child.config))
                if child.cost > max_search_depth:
                    max_search_depth = child.cost
    return None


    """DFS search"""

def A_star_search(initial_state):
    frontier = Q.PriorityQueue()
    frontier.put((calculate_total_cost(initial_state), 0 ,initial_state))
    nodes_expanded = 0
    max_search_depth = 0
    explored = set()
    frontier_set = set()
    frontier_set.add(tuple(initial_state.config))
    second_priority = 0
    ast_start_ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    start_time = time.time()

    while frontier:
        a, b, state = frontier.get()
        frontier_set.remove(tuple(state.config))
        explored.add(tuple(state.config))
        if test_goal(state):
            temp = []
            temp.append(state)
            temp.append(max_search_depth)
            temp.append(explored)
            ast_ram = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - ast_start_ram)/(2**20)
            runtime = time.time() - start_time
            temp.append(ast_ram)
            temp.append(runtime)
            return temp
        children = state.expand()
        nodes_expanded += 1
        for child in children:
            if tuple(child.config) not in explored and tuple(child.config) not in frontier_set:
                first_priority = int(calculate_total_cost(child))
                frontier.put((first_priority, second_priority, child))
                frontier_set.add(tuple(child.config))
                second_priority += 1
                if child.cost > max_search_depth:
                    max_search_depth = child.cost
    return None

    

    """A * search"""

def get_path(state):
    path = []
    n = state
    while n.parent is not None:
        path.append(n.action)
        n = n.parent
    return path[::-1]
    

def calculate_total_cost(state):
    total_cost = state.cost
    for i in range(len(state.config)):
        if state.config[i] == 0:
            continue
        total_cost += calculate_manhattan_dist(i, state.config[i], 3)
    return total_cost

    """calculate the total estimated cost of a state"""

def calculate_manhattan_dist(idx, value, n):
    row = (idx // n) - (value // n) 
    col = (idx % n) - (value % n) 
    
    return abs(row) + abs(col)

    """calculate the manhattan distance of a tile"""

def test_goal(puzzle_state):
    if puzzle_state.config == [0,1,2,3,4,5,6,7,8]:
        return True
    else:
        return False
    """test the state is the goal state or not"""

# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    search_mode = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = list(map(int, begin_state))
    board_size  = int(math.sqrt(len(begin_state)))
    hard_state  = PuzzleState(begin_state, board_size)
    start_time  = time.time()
    
    if   search_mode == "bfs": output = bfs_search(hard_state)
    elif search_mode == "dfs": output = dfs_search(hard_state)
    elif search_mode == "ast": output = A_star_search(hard_state)
    else: 
        print("Enter valid command arguments !")
        
    end_time = time.time()
    max_ram_usage = 0
    writeOutput(output)
    print("Program completed in %.3f second(s)"%(end_time-start_time))

if __name__ == '__main__':
    main()
