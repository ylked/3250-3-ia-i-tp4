''' Bühler-Dekhli AI
'''

from __future__ import annotations  # postpones the evaluation of the type hints, hence they do not need to be imported

NONE = '.'
BLACK = 'B'
WHITE = 'W'

# This variable will contain the color of our IA player
THIS_PLAYER_COLOR = NONE


class Node:
    def __init__(self, game):
        """
        Create a new node containing a game state

        Args:
            game: The game state

        Returns:
            None

        """

        self.game = game
        self.board = self.game.get_board()
        self.rows = self.game.get_rows()
        self.cols = self.game.get_columns()
        self.corners = ((0, 0), (self.rows - 1, 0), (0, self.cols - 1), (self.rows - 1, self.cols - 1))

    def _get_definitive_corner(self):
        """
        Gets the coordinates of the corners that contain pieces owned by our IA player

        Returns:
            list[tuple[int, int]]: The coordinates of the corners that contain pieces owned by our IA player
        """
        corners = []
        for i, j in self.corners:
            if self.board[i][j] == THIS_PLAYER_COLOR:
                corners.append((i, j))

        return corners


    def _count_definitive(self):
        """
        Counts the number of pieces that are definitive and owned by our IA player

        Returns:
            int: The number of pieces that are definitive and owned by our IA player
        """

        def get_step_i_or_j(corner_i_or_j):
            return 1 if corner_i_or_j == 0 else - 1

        def get_end_i(_corner_i):
            return self.rows if _corner_i == 0 else 0

        def get_end_j(_corner_j):
            return self.cols if _corner_j == 0 else 0

        def_count = 0

        for corner_i, corner_j in self._get_definitive_corner():
            for j in range(corner_j, get_end_j(corner_j), get_step_i_or_j(corner_j)):
                if self.board[corner_i][j] != THIS_PLAYER_COLOR:
                    break

                for i in range(corner_i, get_end_i(corner_i), get_step_i_or_j(corner_i)):
                    if self.board[i][j] == THIS_PLAYER_COLOR:
                        def_count += 1
                    else:
                        break

        return def_count

    def _get_penalty_for_near_corners(self):
        """
        Gets a penalty score for each piece owned by our IA player that is placed
        near a corner (X or C cells)

        Returns:
            int: The penalty score
        """
        total_penalty = 0
        penalty_for_each = 5000

        if self.board[0][0] != THIS_PLAYER_COLOR:
            if self.board[0][1] == THIS_PLAYER_COLOR: total_penalty += penalty_for_each
            if self.board[1][0] == THIS_PLAYER_COLOR: total_penalty += penalty_for_each
            if self.board[1][1] == THIS_PLAYER_COLOR: total_penalty += penalty_for_each
        if self.board[0][self.cols - 1] != THIS_PLAYER_COLOR:
            if self.board[0][self.cols - 2] == THIS_PLAYER_COLOR: total_penalty += penalty_for_each
            if self.board[1][self.cols - 1] == THIS_PLAYER_COLOR: total_penalty += penalty_for_each
            if self.board[1][self.cols - 2] == THIS_PLAYER_COLOR: total_penalty += penalty_for_each
        if self.board[self.rows - 1][0] != THIS_PLAYER_COLOR:
            if self.board[self.rows - 1][1] == THIS_PLAYER_COLOR: total_penalty += penalty_for_each
            if self.board[self.rows - 2][0] == THIS_PLAYER_COLOR: total_penalty += penalty_for_each
            if self.board[self.rows - 2][1] == THIS_PLAYER_COLOR: total_penalty += penalty_for_each
        if self.board[self.rows - 1][self.cols - 1] != THIS_PLAYER_COLOR:
            if self.board[self.rows - 1][self.cols - 2] == THIS_PLAYER_COLOR: total_penalty += penalty_for_each
            if self.board[self.rows - 2][self.cols - 1] == THIS_PLAYER_COLOR: total_penalty += penalty_for_each
            if self.board[self.rows - 2][self.cols - 2] == THIS_PLAYER_COLOR: total_penalty += penalty_for_each

        return total_penalty

    @staticmethod
    def _color_inverse(color):
        """
        Gets the inverse of a given color (WHITE <-> BLACK)

        Args:
            color(str): The color to invert

        Returns:
            str: The inverted color
        """
        assert color in (WHITE, BLACK)

        return BLACK if color == WHITE else WHITE

    def eval(self):
        """
        Gets the global evaluation score of the current game contained in this node. The better the score,
        the better the situation is for our IA player.

        Returns:
            int: The evaluation score
        """

        # penalty for badly placed pieces
        penalty = self._get_penalty_for_near_corners()

        # number of definitive pieces owned by our IA player
        definitive = self._count_definitive()

        # difference between the score of our IA player and the one of the adversary
        score = self.game.get_scores(THIS_PLAYER_COLOR) - self.game.get_scores(self._color_inverse(THIS_PLAYER_COLOR))

        return definitive * 1000 + score * 10 - penalty

    def alphabeta(self, parent_score, min_or_max, depth):
        """
        Runs the alphabeta algorithm on the current game contained in this node.

        Args:
            parent_score(int | None): The current obtained score of the parent node. Useful to prune the tree. None if there is no parent
            min_or_max(int): 1 if the algorithm must **maximise**, -1 if it must **minimise**.
            depth(int): The remaining tree depth to explore. The algorithm stops and evaluates the obtained node once the depth reaches zero.

        Returns:
            tuple[int, tuple[int, int]]: A tuple containing the obtained score and the operator that leaded to it
        """
        assert min_or_max in (1, -1)
        assert depth >= 0

        if self.game.is_game_over() or depth <= 0:
            return self.eval(), None

        op = None
        node_score = None

        for row, col in self.game.get_possible_move():
            new_game = self.game.copy_game()
            new_game.move(row, col)
            new_node = Node(new_game)
            res_score, _ = new_node.alphabeta(node_score, -min_or_max, depth - 1)

            if node_score is None or res_score * min_or_max > node_score * min_or_max:
                op = (row, col)
                node_score = res_score

                if node_score is not None and parent_score is not None:
                    if node_score * min_or_max > parent_score * min_or_max:
                        break
        return node_score, op


class Buehler_Dekhli:
    '''The name of this class must be the same as its file.
    '''

    def __init__(self):
        pass

    def next_move(self, board: othello.OthelloGame) -> tuple[int, int]:
        """Returns the next move to play.

        Args:
            board (othello.OthelloGame): The current board to play with

        Returns:
            tuple[int, int]: the next move (for instance: (2, 3) for (row, column), starting from 0)
        """

        global THIS_PLAYER_COLOR
        THIS_PLAYER_COLOR = board.get_turn()

        node = Node(board)
        _, op = node.alphabeta(None, 1, 5)
        return op

    def __str__(self):
        return "Buehler_Dekhli"
