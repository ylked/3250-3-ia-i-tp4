''' Bühler-Dekhli AI
'''

from __future__ import annotations # postpones the evaluation of the type hints, hence they do not need to be imported
import random

from src.app_othello import othello

color = othello.NONE

class Node:
    def __init__(self, game):
        self.game = game
        self.children = []

    def final(self) -> bool:
        return self.game.is_game_over() or not self.game.get_possible_move()

    def eval(self):
        return self.game.get_scores(color)

    def operators(self):
        return self.game.get_possible_move()

    def min(self, depth) -> (Node, (int, int)):
        if self.final() or depth <= 0:
            return self, None

        min_node = None
        min_op = None

        for row, col in self.operators():
            new_game = self.game.copy_game()
            new_game.move(row, col)
            new_node = Node(new_game)
            res, _ = new_node.max(depth-1)

            if min_node is None or res.eval() < min_node.eval():
                min_op = (row, col)
                min_node = res

        return min_node, min_op

    def max(self, depth) -> (Node, (int, int)):
        if self.final() or depth <= 0:
            return self, None

        max_node = None
        max_op = None

        for row, col in self.operators():
            new_game = self.game.copy_game()
            new_game.move(row, col)
            new_node = Node(new_game)
            res, _ = new_node.min(depth-1)

            if max_node is None or res.eval() > max_node.eval():
                max_op = (row, col)
                max_node = res

        return max_node, max_op


    def ab_min(self, parent_max, depth) -> (Node, (int, int)):
        if self.final() or depth <= 0:
            return self, None

        min_node = None
        min_op = None

        for row, col in self.operators():
            new_game = self.game.copy_game()
            new_game.move(row, col)
            new_node = Node(new_game)
            res, _ = new_node.ab_max(min_node, depth-1)

            if min_node is None or res.eval() < min_node.eval():
                min_op = (row, col)
                min_node = res

                if min_node is not None and parent_max is not None:
                    if min_node.eval() < parent_max.eval():
                        break

        return min_node, min_op

    def ab_max(self, parent_min, depth) -> (Node, (int, int)):
        if self.final() or depth <= 0:
            return self, None

        max_node = None
        max_op = None

        for row, col in self.operators():
            new_game = self.game.copy_game()
            new_game.move(row, col)
            new_node = Node(new_game)
            res, _ = new_node.ab_min(max_node, depth-1)

            if max_node is None or res.eval() > max_node.eval():
                max_op = (row, col)
                max_node = res

                if max_node is not None and parent_min is not None:
                    if max_node.eval() > parent_min.eval():
                        break

        return max_node, max_op


class Buehler_Dekhli:
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
        _, op = node.ab_max(None, 5)
        return op

    def __str__(self):
        return "Buehler_Dekhli"