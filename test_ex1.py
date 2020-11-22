from unittest import TestCase
from ex1 import IDS, UCS, ASTAR, IDASTAR
from board import Board


class TestEx1(TestCase):
    board_1 = Board([[0, -1, 2, 3, 4],
                     [0, -1, -1, 3, 3],
                     [0, -1, 2, 3, 4],
                     [1, 1, 1, 1, 4],
                     [0, -1, 2, 3, 4]], 5)

    board_2 = Board([[1, 1, 1, 1],
                     [1, -1, -1, 1],
                     [1, 1, 1, 1],
                     [1, 1, 1, 1]], 4)

    board_3 = Board([[3, 1, 2, 7],
                     [1, 2, 7, 3],
                     [2, 7, 3, 1],
                     [7, 3, 1, 2]], 4)

    board_4 = Board([[1, 1, 1, 1, 1],
                     [1, -1, -1, -1, -1],
                     [1, -1, 1, 1, 1],
                     [1, 1, 1, -1, 1],
                     [1, 1, 1, -1, 1]], 5)

    board_5 = Board([[1, -1, 1, 1, 1],
                     [1, -1, -1, -1, -1],
                     [1, -1, 1, 1, 1],
                     [1, 1, -1, 1, 1],
                     [1, -1, 1, -1, 1]], 5)


    def test_ids_simple(self):
        ids = IDS(self.board_1.nodes[(0, 0)], self.board_1.nodes[(0,2)], self.board_1)
        is_succ = ids.run_algorithm()
        path = ids.print_path()
        self.assertTrue(is_succ)
        self.assertEqual("D-D", path)

    def test_ids_simple2(self):
        ids = IDS(self.board_1.nodes[(0, 0)], self.board_1.nodes[(0,3)], self.board_1)
        is_succ = ids.run_algorithm()
        path = ids.print_path()
        self.assertTrue(is_succ)
        self.assertEqual("D-D-D", path)

    def test_ids_simple3(self):
        ids = IDS(self.board_1.nodes[(0, 0)], self.board_1.nodes[(2, 3)], self.board_1)
        is_succ = ids.run_algorithm()
        path = ids.print_path()
        self.assertTrue(is_succ)
        self.assertEqual("D-D-D-R-R", path)

    def test_ids_hard(self):
        ids = IDS(self.board_2.nodes[(0, 0)], self.board_2.nodes[(3, 3)], self.board_2)
        is_succ = ids.run_algorithm()
        path = ids.print_path()
        self.assertTrue(is_succ)
        self.assertEqual("D-D-R-R-RD", path)
        self.assertEqual(5, ids.value)
        self.assertEqual(111, ids.path_count)

    def test_ucs_hard(self):
        ucs = UCS(self.board_3.nodes[(0, 0)], self.board_2.nodes[(3, 3)], self.board_3)
        is_succ = ucs.run_algorithm()
        path = ucs.print_path()
        self.assertTrue(is_succ)
        self.assertEqual("RD-RD-RD", path)
        self.assertEqual(7, ucs.value)
        self.assertEqual(11, ucs.path_count)


    def test_ucs_hard2(self):
        ucs = UCS(self.board_4.nodes[(0, 0)], self.board_4.nodes[(1, 4)], self.board_4)
        is_succ = ucs.run_algorithm()
        path = ucs.print_path()
        self.assertTrue(is_succ)
        self.assertEqual("D-D-D-RD", path)
        self.assertEqual(4, ucs.value)
        self.assertEqual(9, ucs.path_count)

    def test_ucs_hard3(self):
        ucs = UCS(self.board_4.nodes[(0, 0)], self.board_4.nodes[(4, 4)], self.board_4)
        is_succ = ucs.run_algorithm()
        path = ucs.print_path()
        self.assertTrue(is_succ)
        print(path)
        print(ucs.value)
        print(ucs.path_count)



    def test_astar(self):
        astar = ASTAR(self.board_4.nodes[(0, 0)], self.board_4.nodes[(1, 4)], self.board_4)
        is_succ = astar.run_algorithm()
        path = astar.print_path()
        print(f"Path: {path}")
        print(f"value {astar.value}")
        print(f"path count {astar.path_count}")

    def test_astar2(self):
        astar = ASTAR(self.board_4.nodes[(0, 0)], self.board_4.nodes[(4, 4)], self.board_4)
        is_succ = astar.run_algorithm()
        path = astar.print_path()
        print(f"Path: {path}")
        print(f"value {astar.value}")
        print(f"path count {astar.path_count}")

    def test_idastar(self):
        idastar = IDASTAR(self.board_4.nodes[(0, 0)], self.board_4.nodes[(1, 4)], self.board_4)
        is_succ = idastar.run_algorithm()
        path = idastar.print_path()
        print(f"Path: {path}")
        print(f"value {idastar.value}")
        print(f"path count {idastar.path_count}")

    def test_idastar2(self):
        idastar = IDASTAR(self.board_4.nodes[(0, 0)], self.board_4.nodes[(4, 4)], self.board_4)
        is_succ = idastar.run_algorithm()
        path = idastar.print_path()
        print(f"Path: {path}")
        print(f"value {idastar.value}")
        print(f"path count {idastar.path_count}")



    def test_idastar3(self):
        idastar = IDASTAR(self.board_3.nodes[(0, 0)], self.board_3.nodes[(3, 3)], self.board_3)
        is_succ = idastar.run_algorithm()
        path = idastar.print_path()
        print(f"Path: {path}")
        print(f"value {idastar.value}")
        print(f"path count {idastar.path_count}")

    def test_idastar4(self):
        idastar = IDASTAR(self.board_5.nodes[(0, 0)], self.board_5.nodes[(4, 4)], self.board_5)
        is_succ = idastar.run_algorithm()
        self.assertFalse(is_succ)

    def test_idastar_hard(self):
        idastar = IDASTAR(self.board_2.nodes[(0, 0)], self.board_2.nodes[(3, 3)], self.board_2)
        is_succ = idastar.run_algorithm()
        path = idastar.print_path()
        self.assertTrue(is_succ)
        # self.assertEqual("D-D-R-R-RD", path)
        # self.assertEqual(5, ids.path_count)
        # self.assertEqual(111, ids.value)
        print(f"Path: {path}")
        print(f"value {idastar.value}")
        print(f"path count {idastar.path_count}")


