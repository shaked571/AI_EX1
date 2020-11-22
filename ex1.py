from collections import deque
import copy
from functools import lru_cache
from ast import literal_eval
import sys
from priority_queue import PriorityQueue
from board import Board, Node

class GraphMaxDiagDistance:
    """
    A class that represnt the huristic function
    """
    def __init__(self, target):
        self.x_target = target.x  # note that blank is omitted
        self.y_target = target.y

    def h(self, node):
        """
        A heuristic function that takes max between the axis x distance to the axis y distance od the node to the target
        Intuitively it is corresponding to go diagonal as you can (like euclidean) and that straight to the point (like
        Manhhethen)
        :param node:
        :return:
        """
        x = node.x
        y = node.y
        return max(abs(x - self.x_target), abs(y - self.y_target))



class SerachAlgo:
    """
    An abstract class for all the search algorithms
    """
    Iterative_Deepening_Depth_First_search = 'IDS'
    Uniform_Cost_Search = 'UCS'
    A_STAR = "ASTAR"
    IDA_STAR = "IDASTAR"
    RIGHT = "R"
    RIGHT_DOWN = "RD"
    DOWN = "D"
    LEFT_DOWN = "LD"
    LEFT = "L"
    LEFT_UP = "LU"
    UP = "U"
    RIGHT_UP = "RU"
    NO_PATH = "no path"
    MAX_DEPTH = 20
    order = {RIGHT: 0, RIGHT_DOWN: 1, DOWN: 2, LEFT_DOWN: 3, LEFT: 4, LEFT_UP: 5, UP: 6, RIGHT_UP: 7}

    @staticmethod
    def g(node):
        """
        Calculate the total value of a node - cost score
        :param node:
        :return:
        """
        return node.total_value()


    def __init__(self, start_point: Node, end_point: Node, board: Board):
        """
        :param start_point: the start_point Node
        :param end_point: the end_point Node
        :param board: representatio of the board
        """
        self.start_point = start_point
        self.end_point = end_point
        self.board = board
        self.path = []
        self.__h_class = GraphMaxDiagDistance(end_point)
        self.h = self.__h_class.h
        self.f = lambda n: self.g(n) + self.h(n)


    def print_path(self):
        """
        :return: string reper of the path
        """
        return "-".join(self.path)

    @lru_cache(3500)
    def get_direction(self, x, y, x1, y1):
        """
        get the direction (x,y) -> (x1,y1)
        :param x: x pivot coordinate
        :param y: y pivot coordinate
        :param x1: x target coordinate
        :param y1: y target coordinate
        :return: the direction
        """
        if y1 > y:
            if x1 == x:
                return self.DOWN
            elif x1 > x:
                return self.RIGHT_DOWN
            else:
                return self.LEFT_DOWN
        elif y1 == y:
            if x1 > x:
                return self.RIGHT
            elif x1 < x:
                return self.LEFT
            else:
                raise ValueError("Its the same corr! not suppose to check arrival here!")
        else:
            if x1 == x:
                return self.UP
            elif x1 > x:
                return self.RIGHT_UP
            else:
                return self.LEFT_UP


class IDS(SerachAlgo):
    """
    IDS algorithm
    do an iterative L-DFS from 0 to max depth
    """

    def __init__(self, start_point, end_point, board):
        super().__init__(start_point, end_point, board)
        self.path_count = 0
        self.value = 0

    def run_algorithm(self):
        """
        run the algorithm
        :return: True is there is a path from strat to end
        """
        board_max_depth = min(self.MAX_DEPTH, self.board.board_size ** 2)
        for max_depth in range(board_max_depth):
            if self.DFS_L(max_depth):
                return True
        self.path = self.NO_PATH
        return False

    def DFS_L(self, max_depth) -> bool:
        """
        A Dfs implementation that serach until max depth
        :param max_depth:  the max depth the dfs go.
        :return:
        """
        stack = deque()
        self.start_point.depth = 0
        stack.append(self.start_point)
        self.path = []
        self.init_count()
        while not len(stack) == 0:
            n: Node = stack.pop()
            if self.end_point == n:
                self.path = n.arrived_from
                self.value = n.total_value()
                return True
            self.path_count += 1
            if len(n.arrived_from) < max_depth:
                for suc in n.successors:
                    suc.arrived_from = n.arrived_from + [self.get_direction(n.x, n.y, suc.x, suc.y)]
                    suc.fathers = n.fathers + [n]
                    stack.append(copy.deepcopy(suc))
        return False

    def init_count(self):
        """
        init the board nodes
        """
        for n in self.board.nodes.values():
            n.depth = None
            n.arrived_from = []
            n.fathers = []


class UCS(SerachAlgo):
    """
    IDS algorithm
    do an iterative L-DFS from 0 to max depth
    """

    def __init__(self, start_point, end_point, board):
        super().__init__(start_point, end_point, board)
        self.path_count = 0
        self.value = 0

    @staticmethod
    def f(node: Node):
        """
        The f function - calculte the cost to arrive to the node
        :param node:
        :return:
        """
        return node.total_value()

    def run_algorithm(self):
        """
        run the algorithm
        :return: True is there is a path from strat to end, False otherwise
        """
        open_list = PriorityQueue()
        open_list.append(self.start_point)
        closed_list = set()
        while not len(open_list) == 0:
            next_n = open_list.pop()
            closed_list.add(next_n)

            if self.end_point == next_n:
                self.value = next_n.total_value()
                self.path = next_n.arrived_from
                return True
            else:
                self.path_count += 1
            for suc in next_n.successors:
                suc.arrived_from = next_n.arrived_from + [self.get_direction(next_n.x, next_n.y, suc.x, suc.y)]
                suc.fathers = next_n.fathers + [next_n]
                if suc not in closed_list and suc not in open_list:
                    open_list.append(copy.deepcopy(suc))
                elif suc in open_list and self.f(suc) < self.f(open_list[suc]):
                    del open_list[suc]
                    open_list.append(copy.deepcopy(suc))

        self.path = self.NO_PATH
        return False




class ASTAR(SerachAlgo):
    """
    IDS algorithm
    do an iterative L-DFS from 0 to max depth
    """
    def __init__(self, start_point, end_point, board):
        super().__init__(start_point, end_point, board)
        self.path_count = 0
        self.value = 0


    def run_algorithm(self):
        """
        run the algorithm
        :return: True is there is a path from strat to end, False otherwise
        """
        open_list = PriorityQueue(f=self.f)
        open_list.append(self.start_point)
        closed_list = set()
        while not len(open_list) == 0:
            next_n = open_list.pop()
            closed_list.add(next_n)

            if self.end_point == next_n:
                self.value = next_n.total_value()
                self.path = next_n.arrived_from
                return True
            else:
                self.path_count += 1
            for suc in next_n.successors:
                suc.arrived_from = next_n.arrived_from + [self.get_direction(next_n.x, next_n.y, suc.x, suc.y)]
                suc.fathers = next_n.fathers + [next_n]
                if suc not in closed_list and suc not in open_list:
                    open_list.append(copy.deepcopy(suc))
                elif suc in open_list and self.f(suc) < open_list[suc]:
                    del open_list[suc]
                    open_list.append(copy.deepcopy(suc))

        self.path = self.NO_PATH
        return False



class IDASTAR(SerachAlgo):
    """
    IDA star algorithm
    do an iterative L-DFS from 0 to max depth
    """

    def __init__(self, start_point, end_point, board):
        super().__init__(start_point, end_point, board)
        self.path_count = 0
        self.value = 0

    def DFS_F(self, path: list, g, bound):
        """
        An helper function for IDA* as shown in the clas pseudo code
        """
        node = path[-1]
        f = g + self.h(node)
        if f > bound:
            return f
        if node == self.end_point:
            self.value = node.total_value()
            self.path = node.arrived_from
            return True
        minimum = sys.maxsize
        self.path_count += 1
        for suc in node.successors:
            if len(suc.fathers) < 20:
                suc.arrived_from = node.arrived_from + [self.get_direction(node.x, node.y, suc.x, suc.y)]
                suc.fathers = node.fathers + [node]
                path.append(suc)
                t = self.DFS_F(copy.deepcopy(path), g + suc.value, bound)
                if t == True:
                    return True
                if t < minimum:
                    minimum = t
                path.pop()
        return minimum


    def run_algorithm(self):
        """
        run the algorithm
        :return:
        :return: True is there is a path from strat to end, False otherwise
        """
        bound = self.h(self.start_point)
        path = [copy.deepcopy(self.start_point)]
        while True:
            sol = self.DFS_F(path, 0, bound)
            if sol  == True:
                return True
            if sol == sys.maxsize:
                self.path = self.NO_PATH
                return False
            bound = sol



def parse_expression(expression_literal: str) -> tuple:
    """
    tarsnfer the input string to tuple
    :param expression_literal: the expression to parse
    :return: parsed expression
    """
    return literal_eval(expression_literal.strip("\n"))


def switch_order(point):
    """
    switch the order between (y,x) -> to (x,y)
    :param point: (y,x)
    :return: (x,y)
    """
    return point[1], point[0]


def read_input(input_f):
    """
    Read the input file
    :param input_f: the input file
    :return: the parsed arguments
    """
    with open(input_f) as f:
        args = f.readlines()
        algo_name = args[0].strip("\n")
        start_point = switch_order(parse_expression(args[1]))
        end_point = switch_order(parse_expression(args[2]))
        board_size = parse_expression(args[3])
        raw_board = [list(parse_expression(r)) for r in args[4:] if r != "\n"]
        if len(raw_board) != board_size:
            raise ValueError(f"Hey dude, your board is not in the correct size!"
                             f"The given sizse is {board_size}, but there is {len(raw_board)} rows.")
    return algo_name, start_point, end_point, board_size, raw_board


def main(input_f):
    """
    classic main that run the flow
    """
    algo_name, start_point, end_point, board_size, raw_board = read_input(input_f)
    board = Board(raw_board, board_size)
    if algo_name == SerachAlgo.Iterative_Deepening_Depth_First_search:
        algorithm = IDS(board.nodes[start_point], board.nodes[end_point], board)
    elif algo_name == SerachAlgo.Uniform_Cost_Search:
        algorithm = UCS(board.nodes[start_point], board.nodes[end_point], board)
    elif algo_name == SerachAlgo.A_STAR:
        algorithm = ASTAR(board.nodes[start_point], board.nodes[end_point], board)
    elif algo_name == SerachAlgo.IDA_STAR:
        algorithm = IDASTAR(board.nodes[start_point], board.nodes[end_point], board)
    else:
        raise ValueError("Not such algorithm")

    is_path = algorithm.run_algorithm()
    path = algorithm.path
    if not is_path:
        with open("output.txt", "w") as f:
            f.write(path)
            return

    opened_nodes = algorithm.path_count
    value = algorithm.value
    with open("output.txt", "w") as f:
        f.write(f"{algorithm.print_path()} {value} {opened_nodes}")


if __name__ == '__main__':
    main("input.txt")
