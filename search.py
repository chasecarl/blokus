"""
In search.py, you will implement generic search algorithms
"""

import util
from itertools import chain


STATE_SUCCESSOR = 0
MOVE_SUCCESSOR = 1
COST_SUCCESSOR = 2
MOVES_DFS = 1


class Node:

    def __init__(self, state, parent=None, spawned_move=None):
        self.childs = []
        self.parent = parent
        if self.parent:
            self.parent.add_child(self)
        self.state = state
        self.spawned_move = spawned_move

    @classmethod
    def root(cls, problem):
        return Node(problem.get_start_state())

    def add_child(self, child):
        self.childs.append(child)


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def is_goal_state(self, state):
        """
        state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()




def depth_first_search(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches
    the goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.get_start_state().state)
    print("Is the start a goal?", problem.is_goal_state(problem.get_start_state()))
    print("Start's successors:", problem.get_successors(problem.get_start_state()))
    """
    visited = []
    root = Node.root(problem)
    result = dfs_helper(problem, root, visited)[MOVES_DFS].list[::-1]
    print(result)
    return result

def dfs_helper(problem, node, visited):
    if problem.is_goal_state(node.state):
        moves = util.Stack()
        moves.push(node.spawned_move)
        return True, moves
    visited.append(node.state)
    successors = problem.get_successors(node.state)[::-1]
    for successor in successors:
        state = successor[STATE_SUCCESSOR]
        if state not in visited:
            move = successor[MOVE_SUCCESSOR]
            child = Node(state, parent=node, spawned_move=move)
            is_goal_path, moves = dfs_helper(problem, child, visited)
            if not is_goal_path:
                continue
            if node.spawned_move:
                moves.push(node.spawned_move)
            return True, moves
    return False, None

def breadth_first_search(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    visited = []
    successors = (problem.get_start_state())
    return bfs_helper(problem, successors, visited)

def bfs_helper(problem, successors, visited):
    for successor in successors:
        state = successor[0]
        if state in visited:
            continue
        if problem.is_goal_state(state):
            moves = util.Stack()
            move = successor[1]
            if move:
                moves.push(move)
            return True, moves, state
        visited.append(state)
    successors = chain.from_iterable(problem.get_successors(successor[0]) for successor in successors)
    is_goal_path, moves, successor  = bfs_helper(problem, successors, visited)
    if is_goal_path:
        moves.push(successor[1])
        for node in visited:
            if successor in problem.get_successors(node):
                return True, moves, node


def uniform_cost_search(problem):
    """
    Search the node of least total cost first.
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


def null_heuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def a_star_search(problem, heuristic=null_heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search
astar = a_star_search
ucs = uniform_cost_search
