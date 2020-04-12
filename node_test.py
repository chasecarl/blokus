import unittest
from search import Node
from search import SearchProblem


class MockProblem(SearchProblem):
    
    def get_start_state(self):
        return 1


class TestNode(unittest.TestCase):

    def test_root_with_mock_problem(self):
        try:
            root = Node.root(MockProblem())
        except RecursionError:
            self.fail(msg="Recursion problem.")

    def test_root_with_mock_problem_with_child(self):
        try:
            root = Node.root(MockProblem())
            child = Node(0, parent=root)
        except RecursionError:
            self.fail(msg="Recursion problem.")

    def test_root_with_mock_problem_with_child_and_grandchild(self):
        try:
            root = Node.root(MockProblem())
            child = Node(0, parent=root)
            grandchild = Node(2, parent=child)
        except RecursionError:
            self.fail(msg="Recursion problem.")



if __name__ == '__main__':
    unittest.main()

