from board import Board
from search import SearchProblem, Node, STATE_SUCCESSOR, MOVE_SUCCESSOR
from random import choice, random
import util
import numpy as np


class BlokusFillProblem(SearchProblem):
    """
    A one-player Blokus game as a search problem.
    This problem is implemented for you. You should NOT change it!
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0)):
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.expanded = 0

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        """
        state: Search state
        Returns True if and only if the state is a valid goal state
        """
        return not any(state.pieces[0])

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, 1) for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return len(actions)



#####################################################
# This portion is incomplete.  Time to write code!  #
#####################################################
class BlokusCornersProblem(SearchProblem):
    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0)):
        targets = np.array([
            (0, 0),
            (board_h - 1, 0),
            (0, board_w - 1),
            (board_h - 1, board_w - 1)
        ])
        self.target_rows = targets[:,0]
        self.target_cols = targets[:,1]
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.expanded = 0

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        return state.get_position(0, 0) != -1\
               and state.get_position(0, state.board_h - 1) != -1 \
               and state.get_position(state.board_w - 1, 0) != -1 \
               and state.get_position(state.board_w - 1, state.board_h - 1) != -1

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return sum(action.piece.get_num_tiles() for action in actions)



def blokus_corners_heuristic(state, problem):
    """
    Your heuristic for the BlokusCornersProblem goes here.

    This heuristic must be consistent to ensure correctness.  First, try to come up
    with an admissible heuristic; almost all admissible heuristics will be consistent
    as well.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the other hand,
    inadmissible or inconsistent heuristics may find optimal solutions, so be careful.
    """
    return np.count_nonzero(state.state[
        problem.target_rows,
        problem.target_cols
    ] == -1) / 2


class BlokusCoverProblem(SearchProblem):
    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=[(0, 0)]):
        self.targets = np.array(targets)
        self.target_rows = self.targets[:,0]
        self.target_cols = self.targets[:,1]
        self.expanded = 0
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        for target in self.targets:
            if state.get_position(target[1], target[0]) == -1:
                return False
        return True

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return sum(action.piece.get_num_tiles() for action in actions)


def blokus_cover_heuristic(state, problem):
    return np.count_nonzero(state.state[
        problem.target_rows,
        problem.target_cols
    ] == -1) / 2


class ClosestLocationSearch:
    """
    In this problem you have to cover all given positions on the board,
    but the objective is speed, not optimality.
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=(0, 0)):
        self.expanded = 0
        self.targets = np.array(targets.copy())
        self.target_rows = self.targets[:,0]
        self.target_cols = self.targets[:,1]
        self.n_iter = 2 * board_w * board_h
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def get_successors(self, state):
        self.expanded += 1
        return [(state.do_move(0, move), move) for move in state.get_legal_moves(0)]

    def objective_function(self, state):
        return np.count_nonzero(state.state[
                                    self.target_rows,
                                    self.target_cols
                                ] == -1)

    def is_goal_state(self, state):
        return np.count_nonzero(state.state[
                self.target_rows,
                self.target_cols
                ] == -1) == 0

    def solve(self):
        """
        This method should return a sequence of actions that covers all target locations on the board.
        This time we trade optimality for speed.
        Therefore, your agent should try and cover one target location at a time. Each time, aiming for the closest uncovered location.
        You may define helpful functions as you wish.
        """
        self.n_iter = 30
        t = 0
        current = Node(self.get_start_state())
        backtrace  = []
        while True:
            if t == self.n_iter - 1 or self.is_goal_state(current.state):
                return backtrace
            successors = self.get_successors(current.state)
            successors.sort(key=lambda successor: self.objective_function(successor[STATE_SUCCESSOR]))
            if len(successors) == 0:
                return backtrace
            best_score = self.objective_function(successors[0][STATE_SUCCESSOR])
            best_successors = [successor for successor in successors
                               if self.objective_function(successor[STATE_SUCCESSOR]) == best_score]
            successor = choice(best_successors)
            candidate = Node(successor[STATE_SUCCESSOR], parent=current, spawned_action=successor[MOVE_SUCCESSOR])
            delta_e = self.objective_function(candidate.state)- self.objective_function(current.state)
            if delta_e < 0 or random() < 0.5 * (0.9 ** (t + 1)):
                current = candidate
                backtrace.append(current.spawned_action)
            t += 1



class MiniContestSearch:
    """
    Implement your contest entry here
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=(0, 0)):
        self.targets = targets.copy()
        "*** YOUR CODE HERE ***"

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def solve(self):
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

