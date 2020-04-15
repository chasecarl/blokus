"""
In search.py, you will implement generic search algorithms
"""

import util
from collections import deque
from queue import PriorityQueue as PQ
from dataclasses import dataclass, field
from typing import Any

STATE_SUCCESSOR = 0
MOVE_SUCCESSOR = 1
COST_SUCCESSOR = 2


def null_heuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0



class Node:

    def __init__(self, state, parent=None, spawned_action=None):
        self.children = []
        self.parent = parent
        if self.parent:
            self.parent.add_child(self)
        self.state = state
        self.spawned_action = spawned_action
    @classmethod
    def root(cls, problem):
        return cls(problem.get_start_state())

    @classmethod
    def from_successor(cls, successor, parent, heuristic=None, problem=None):
        return cls(
            successor[STATE_SUCCESSOR],
            parent=parent,
            spawned_action=successor[MOVE_SUCCESSOR]
        )

    def add_child(self, child):
        self.children.append(child)

@dataclass(order=True)
class PrioritizedNode(Node):
    priority: int
    # node: Any=field(compare=False)
    def __init__(self, state, parent=None, spawned_action=None, priority=0):
        super().__init__(state, parent=parent, spawned_action=spawned_action)
        self.priority = priority
        if self.parent:
            self.priority += self.parent.priority

    @classmethod
    def from_successor(cls, successor, parent, heuristic=None, problem=None):
        return cls(
            successor[STATE_SUCCESSOR],
            parent=parent,
            spawned_action=successor[MOVE_SUCCESSOR],
            priority=successor[COST_SUCCESSOR]
        )

# @dataclass(order=True)
class HeuristicNode(PrioritizedNode):
    def __init__(self, state, parent=None, spawned_action=None, priority=0, heuristic=null_heuristic, problem=None):
        super().__init__(state, parent=parent, spawned_action=spawned_action, priority=priority)
        self.priority+=heuristic(state, problem=problem)
    @classmethod
    def from_successor(cls, successor, parent, heuristic=null_heuristic, problem=None):
        return cls(
            successor[STATE_SUCCESSOR],
            parent=parent,
            spawned_action=successor[MOVE_SUCCESSOR],
            priority=successor[COST_SUCCESSOR],
            heuristic=heuristic,
            problem=problem
        )

class Fringe:
    
    def add(self, element):
        """
        Adds an element to the fringe
        """
        pass

    def retrieve(self):
        """
        Gets the next element and removes it from the fringe
        """
        pass

    def __bool__(self):
        pass


class Stack(Fringe):

    def __init__(self):
        self.deque = deque()

    def add(self, element):
        self.deque.append(element)

    def retrieve(self):
        return self.deque.pop()

    def __bool__(self):
        return len(self.deque) != 0


class Queue(Fringe):

    def __init__(self):
        self.deque = deque()

    def add(self, element):
        self.deque.appendleft(element)

    def retrieve(self):
        return self.deque.pop()

    def __bool__(self):
        return len(self.deque) != 0

class PriorityQueue(Fringe):
    def __init__(self):
        self.queue = PQ()

    def add(self, element):
        self.queue.put(element)

    def retrieve(self):
        return self.queue.get()

    def __bool__(self):
        return not self.queue.empty()

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


def restore_actions(goal_node):
    reverse_actions = []
    current = goal_node
    while current:
        if current.spawned_action:
            reverse_actions.append(current.spawned_action)
        current = current.parent
    return reverse_actions[::-1]


def generic_search(problem, fringe_class, node_class=Node, heuristic=null_heuristic):
    fringe = fringe_class()
    fringe.add(node_class.root(problem))
    visited = set()
    while fringe:
        current = fringe.retrieve()

        if problem.is_goal_state(current.state):
            return restore_actions(current)
        if current.state not in visited:
            for successor in problem.get_successors(current.state):
                fringe.add(node_class.from_successor(successor, current, heuristic=heuristic, problem=problem))

            visited.add(current.state)
    return None


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
    return generic_search(problem, Stack)


def breadth_first_search(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    return generic_search(problem, Queue)


def uniform_cost_search(problem):
    """
    Search the node of least total cost first.
    """
    return generic_search(problem, PriorityQueue, node_class=PrioritizedNode)


def a_star_search(problem, heuristic=null_heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    return generic_search(problem, PriorityQueue, node_class=HeuristicNode, heuristic=null_heuristic)


# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search
astar = a_star_search
ucs = uniform_cost_search
