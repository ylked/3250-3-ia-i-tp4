''' Bühler-Dekhli AI
'''

from __future__ import annotations  # postpones the evaluation of the type hints, hence they do not need to be imported

from src.app_othello import othello

color = othello.NONE


class Node:
    def __init__(self, game):
        self.game: othello.OthelloGame = game
        self.board = self.game.get_board()

        self.rows = self.game.get_rows()
        self.cols = self.game.get_columns()

        self.corners = ((0, 0), (self.rows - 1, 0), (0, self.cols - 1), (self.rows - 1, self.cols - 1))

    def final(self) -> bool:
        return self.game.is_game_over() or not self.game.get_possible_move()

    def get_definitive_corner(self):
        corners = []
        for i, j in self.corners:
            if self.board[i][j] == color:
                corners.append((i, j))

        return corners

    @staticmethod
    def get_step_i(corner_i):
        return 1 if corner_i == 0 else - 1

    @staticmethod
    def get_step_j(corner_j):
        return 1 if corner_j == 0 else - 1

    def get_end_i(self, corner_i):
        return self.rows if corner_i == 0 else 0

    def get_end_j(self, corner_j):
        return self.cols if corner_j == 0 else 0

    # TODO make sure this method counts correctly the definitive
    def count_definitive(self):
        definitive = []

        for corner_i, corner_j in self.get_definitive_corner():
            for j in range(corner_j, self.get_end_j(corner_j), self.get_step_j(corner_j)):
                if self.board[corner_i][j] != color:
                    break

                for i in range(corner_i, self.get_end_i(corner_i), self.get_step_i(corner_i)):
                    if self.board[i][j] == color:
                        definitive.append((i, j))
                    else:
                        break

        return len(definitive)

    def get_malus_for_near_corner(self):
        bonus = 0
        malus_for_near_corner = 5000

        if self.board[0][0] != color:
            if self.board[0][1] == color: bonus -= malus_for_near_corner
            if self.board[1][0] == color: bonus -= malus_for_near_corner
            if self.board[1][1] == color: bonus -= malus_for_near_corner
        if self.board[0][self.cols - 1] != color:
            if self.board[0][self.cols - 2] == color: bonus -= malus_for_near_corner
            if self.board[1][self.cols - 1] == color: bonus -= malus_for_near_corner
            if self.board[1][self.cols - 2] == color: bonus -= malus_for_near_corner
        if self.board[self.rows - 1][0] != color:
            if self.board[self.rows - 1][1] == color: bonus -= malus_for_near_corner
            if self.board[self.rows - 2][0] == color: bonus -= malus_for_near_corner
            if self.board[self.rows - 2][1] == color: bonus -= malus_for_near_corner
        if self.board[self.rows - 1][self.cols - 1] != color:
            if self.board[self.rows - 1][self.cols - 2] == color: bonus -= malus_for_near_corner
            if self.board[self.rows - 2][self.cols - 1] == color: bonus -= malus_for_near_corner
            if self.board[self.rows - 2][self.cols - 2] == color: bonus -= malus_for_near_corner

        return bonus

    @staticmethod
    def color_inverse(_color):
        return othello.BLACK if _color == othello.WHITE else othello.WHITE

    def eval(self):
        malus = self.get_malus_for_near_corner()
        definitive = self.count_definitive()
        score = self.game.get_scores(color) - self.game.get_scores(self.color_inverse(color))

        return definitive * 1000 + score * 10 + malus

    # TODO make min and max in the same method to avoid code duplicate
    def min(self, parent_score, depth) -> (int, (int, int)):
        if self.game.is_game_over() or depth <= 0:
            return self.eval(), None

        min_node_score = None
        min_op = None

        for row, col in self.game.get_possible_move():
            new_game = self.game.copy_game()
            new_game.move(row, col)
            new_node = Node(new_game)
            res_score, _ = new_node.max(min_node_score, depth - 1)

            # self.children.append(new_node)

            if min_node_score is None or res_score < min_node_score:
                min_op = (row, col)
                min_node_score = res_score

                if min_node_score is not None and parent_score is not None:
                    if min_node_score < parent_score:
                        break

        return min_node_score, min_op

    # TODO make min and max in the same method to avoid code duplicate
    def max(self, parent_score, depth) -> (int, (int, int)):
        if self.game.is_game_over() or depth <= 0:
            return self.eval(), None

        max_op = None
        max_node_score = None

        for row, col in self.game.get_possible_move():
            new_game = self.game.copy_game()
            new_game.move(row, col)
            new_node = Node(new_game)
            res_score, _ = new_node.min(max_node_score, depth - 1)

            if max_node_score is None or res_score > max_node_score:
                max_op = (row, col)
                max_node_score = res_score

                if max_node_score is not None and parent_score is not None:
                    if max_node_score > parent_score:
                        break
        return max_node_score, max_op


class Buehler_Dekhli_v5:
    '''The name of this class must be the same as its file.
    '''

    def __init__(self):
        pass

    def next_move(self, board: othello.OthelloGame) -> tuple[int, int]:
        """Returns the next move to play.

        Args:
            board (othello.OthelloGame): _description_

        Returns:
            tuple[int, int]: the next move (for instance: (2, 3) for (row, column), starting from 0)
        """
        global color
        color = board.get_turn()

        node = Node(board)
        score, op = node.max(None, 5)
        # TODO remove the following DEBUG line
        print("score for choice = " + str(score))
        return op

    def __str__(self):
        return "Buehler_Dekhli_v5"
