class Node:
    """
    A class
    Which represent a Node
    """
    def __init__(self, x, y, value, successors):
        self.value: int = value
        self.y: int = y
        self.x: int = x
        self.successors: list = successors
        self.depth = None
        self.arrived_from = []
        self.fathers = []
        RIGHT = "R"
        RIGHT_DOWN = "RD"
        DOWN = "D"
        LEFT_DOWN = "LD"
        LEFT = "L"
        LEFT_UP = "LU"
        UP = "U"
        RIGHT_UP = "RU"
        self.order = {RIGHT: 0, RIGHT_DOWN: 1, DOWN: 2, LEFT_DOWN: 3, LEFT: 4, LEFT_UP: 5, UP: 6, RIGHT_UP: 7}

    def total_value(self):
        """
        Calculate the total value to the node include itself and not include the value of the root
        :return:
        """
        return sum([f.value for f in self.fathers[1:]]) + self.value

    def __eq__(self, other):
        """equal implementation"""
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        """hash implementation"""
        return hash(str(f"{self.x},{self.y}"))

    def __lt__(self, other):
        """less than implementation"""
        if self.total_value() == other.total_value():
            return self.order[self.arrived_from[-1]] < self.order[other.arrived_from[-1]]
        return self.total_value() < other.total_value()


class Board:
    """
    A class
    which represent a Board
    """

    def __init__(self, board_raw, board_size):
        self.graph = {}
        self.nodes = {}
        self.board_raw = board_raw
        self.board_size = board_size
        self.create_nodes()
        self.assign_successors()

    def assign_successors(self):
        """
        Assighn to all the nodes their possible successors
        :return:
        """
        for cor, node in self.nodes.items():
            if node.value == -1:
                continue
            x, y = cor
            successors = self.get_successors(x, y)
            node.successors = successors
            self.graph[(x, y)] = node.successors

    def create_nodes(self):
        """
        create the nodes in the board
        :return:
        """
        for y in range(self.board_size):
            for x in range(self.board_size):
                self.nodes[(x, y)] = Node(x, y, self.get_value(x, y), [])

    def get_successors(self, x, y) -> list:
        """
        get the successors of a node (x,y)
        :param x: x coordinate
        :param y: y coordinate
        :return: guess what dummy
        """
        succ = []

        move_opt = [((x + 1, y), 'R'),
                    ((x + 1, y + 1), 'RD'),
                    ((x, y + 1),   'D'),
                    ((x - 1, y + 1), 'LD'),
                    ((x - 1, y),    'L'),
                    ((x - 1, y - 1), 'LU'),
                    ((x, y - 1),   'U'),
                    ((x + 1, y - 1), 'RU')]

        for (x_i, y_i), d in move_opt:
            if self.value_illegal(x_i, y_i) or self.is_cliff(x_i, y_i):
                continue
            if d in ['RD', 'LD', 'LU', 'RU'] and self.diagonal_cliff(x_i, y_i, d):
                continue

            succ.append(self.nodes[(x_i, y_i)])
        succ.reverse()
        return succ

    def get_value(self, x, y) -> int:
        """
        Get the value of a cell in a board
        :param x: x coordinate
        :param y: y coordinate
        :return: cell value
        """
        return self.board_raw[y][x]

    def is_cliff(self, x_i, y_i):
        """
        Check is a cell is a cliff
        :param x_i: x coordinate
        :param y_i: y coordinate
        :return: True if a cliff
        """
        return self.get_value(x_i, y_i) == -1

    def diagonal_cliff(self, x_i, y_i, d):
        """
        check if a pair is a successors option
        :param x:  x pivot coordinate
        :param y:  y pivot coordinate
        :param x_i:  x option diagonal coordinate
        :param y_i:  y option diagonal coordinate
        :return: True if you can't go there
        """
        valid_points = []

        if y_i + 1 < self.board_size and d in ["LU", "RU"] :
            valid_points.append((x_i, y_i + 1))
        if y_i - 1 > -1 and d in ["RD", "LD"] :
            valid_points.append((x_i, y_i - 1))
        if x_i + 1 < self.board_size and d != ["LD", "LU"]:
            valid_points.append((x_i + 1, y_i))
        if x_i - 1 > -1 and d != ["RD", "RU"]:
            valid_points.append((x_i - 1, y_i))

        return any([self.is_cliff(x_j, y_j) for x_j, y_j in valid_points])

    def value_illegal(self, x, y):
        """
        Check if a value exusts in the board
        :param x: x
        :param y: y
        :return: True if illegal False otherwise
        """
        return x < 0 or y < 0 or y >= self.board_size or x >= self.board_size


