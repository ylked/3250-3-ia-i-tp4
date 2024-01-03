''' Bühler-Dekhli AI
'''

from __future__ import annotations # postpones the evaluation of the type hints, hence they do not need to be imported
import random

from src.app_othello import othello

color = othello.NONE

class Node:
    def __init__(self, game):
        self.game:othello.OthelloGame = game

    def final(self) -> bool:
        return self.game.is_game_over() or not self.game.get_possible_move()

    def eval(self):
        bonus_for_corner = 50
        malus_for_near_corner = 100
        bonus = 0

        board = self.game.get_board()
        rows = self.game.get_rows()
        cols = self.game.get_columns()
        current_color = othello.BLACK if self.game.get_turn() == othello.WHITE else othello.WHITE

        if board[0][0] == current_color: bonus += bonus_for_corner
        if board[0][cols-1] == current_color: bonus += bonus_for_corner
        if board[rows-1][0] == current_color: bonus += bonus_for_corner
        if board[rows-1][cols-1] == current_color: bonus += bonus_for_corner

        if board[0][1] == current_color: bonus -= malus_for_near_corner
        if board[0][cols-2] == current_color: bonus -= malus_for_near_corner
        if board[1][0] == current_color: bonus -= malus_for_near_corner
        if board[1][cols-1] == current_color: bonus -= malus_for_near_corner
        if board[1][1] == current_color: bonus -= malus_for_near_corner
        if board[1][cols-2] == current_color: bonus -= malus_for_near_corner

        if board[rows-1][1] == current_color: bonus -= malus_for_near_corner
        if board[rows-1][cols-2] == current_color: bonus -= malus_for_near_corner
        if board[rows-2][0] == current_color: bonus -= malus_for_near_corner
        if board[rows-2][cols-1] == current_color: bonus -= malus_for_near_corner
        if board[rows-2][1] == current_color: bonus -= malus_for_near_corner
        if board[rows-2][cols-2] == current_color: bonus -= malus_for_near_corner

        return self.game.get_scores(current_color) + bonus

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

            #self.children.append(new_node)

            if min_node_score is None or res_score < min_node_score:
                min_op = (row, col)
                min_node_score = res_score

                if min_node_score is not None and parent_score is not None:
                    if min_node_score < parent_score:
                        break

        return min_node_score, min_op

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


class Buehler_Dekhli_v4:
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
        _, op = node.max(None, 5)
        return op

    def __str__(self):
        return "Buehler_Dekhli_v4"