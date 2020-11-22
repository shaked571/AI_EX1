from unittest import TestCase
from board import Board


class TestMLETrain(TestCase):
    board = Board([[0, -1, 2, 3, 4],
                   [0, -1, -1, 3, 3],
                   [0, -1, 2, 3, 4],
                   [1, 1, 1, 1, 4],
                   [0, -1, 2, 3, 4]], 5)

    def test_get_value(self):
        res = self.board.get_value(0, 0)
        self.assertEqual(0, res)

    def test_node_value(self):
        res = self.board.nodes[(0, 0)].value
        self.assertEqual(0, res)

    def test_not_diagonal_move(self):
        res = self.board.diagonal_cliff(3, 0, "LU")
        self.assertEqual(False, res)

    def test_not_take_cliff_neighbour_in_diagonal(self):
        res = self.board.diagonal_cliff(0, 2, "LU")
        self.assertEqual(True, res)

    def test_correct_successors(self):
        res = self.board.nodes[(0, 0)].successors
        self.assertEqual(1, len(res))
        self.assertEqual([self.board.nodes[(0, 1)]], res)

    def test_value_illegal(self):
        res = self.board.value_illegal(-1, 4)
        self.assertTrue(res)

