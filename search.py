"""
In search.py, you will implement generic search algorithms
"""

import util
from itertools import chain


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
    return dfs_helper(problem, problem.get_start_state(), visited)[1].list[::-1]

def dfs_helper(problem, state, visited, move=None):
    if problem.is_goal_state(state):
        moves = util.Stack()
        moves.push(move)
        return True, moves
    visited.append(state)
    for successor in problem.get_successors(state)[::-1]:
        if successor[0] not in visited:
            is_goal_path, moves = dfs_helper(problem, successor[0], visited, move=successor[1])
            if not is_goal_path:
                continue
            if move:
                moves.push(move)
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
