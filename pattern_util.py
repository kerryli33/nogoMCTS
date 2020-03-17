"""
pattern_util.py
Utility functions for rule based simulations.
"""

import numpy as np
import random
from board_util import GoBoardUtil, EMPTY, PASS, BORDER, BLACK, WHITE


class PatternUtil(object):

    @staticmethod
    def neighborhood_33(board, point):
        """
        Get the pattern around point.
        Returns lookup value for table to get pattern weight
        """
        positions = [point-board.NS-1, point-board.NS, point-board.NS+1,
                     point-1, point, point+1,
                     point+board.NS-1, point+board.NS, point+board.NS+1]
        code = 0
        j = 0
        for i in range (9):
            if i == 4:
                continue
            else:
                pos = board.board[positions[j]]
                if pos == board.current_player:
                    code += (1 * pow( 4 , j ))
                elif pos == GoBoardUtil.opponent(board.current_player):
                    code += (2 * pow( 4 , j ))
                elif pos == BORDER:
                    code += (3 * pow( 4 , j ))
                j += 1
        return code
    
    @staticmethod
    def generate_pattern_moves(board):
        """
        Generate a list of moves that match pattern.
        This only checks moves that are neighbors of the moves in the last two steps.
        See last_moves_empty_neighbors() in simple_board for detail.
        """
        color = board.current_player
        # pattern_checking_set = board.last_moves_empty_neighbors()
        empty_pts = board.get_empty_points()
        legal_mvs = [ move for move in empty_pts if board.is_legal( move , color ) ]

        moves = {}
        for p in legal_mvs:
            code = PatternUtil.neighborhood_33(board, p)
            value = board.pattern_table.get(code)
            print(code)
            if ( value != -1 and value != "1.0"):
                assert p not in moves
                assert board.board[p] == EMPTY
                moves[p] = value
        return moves

    @staticmethod
    def generate_move(board, use_pattern):
        """
        Arguments
        ---------
        board: GoBoard
        use_pattern: Use pattern policy?
        """
        move = None
        if use_pattern:
            moves = PatternUtil.generate_pattern_moves(board)
            mvs , vals = PatternUtil.calc_probabilities(board, moves)
            move = np.random.choice(mvs, len(mvs), vals)

        if move == None:
            move = GoBoardUtil.generate_random_move(board, board.current_player,True)
        return move

    @staticmethod
    def calc_probabilities(moves):
        """
        Arguments
        ---------
        moves: move set based on generated pattern
        ---------
        Returns probility of generating each move
        """
        val_sum = 0
        mvs = []
        values = []
        for k,v in moves.items():
            val_sum += v
        for k,v in moves.items():
            mvs.append(k)
            values.append((v / val_sum ))
        return mvs , values

    @staticmethod
    def playGame(board, color, **kwargs):
        """
        Run a simulation game according to give parameters.
        """
        # komi = kwargs.pop('komi', 0)
        limit = kwargs.pop('limit', 1000)
        random_simulation = kwargs.pop('random_simulation',True)
        use_pattern = kwargs.pop('use_pattern',True)
        if kwargs:
            raise TypeError('Unexpected **kwargs: %r' % kwargs)
        for _ in range(limit):
            color = board.current_player
            if random_simulation:
                move = GoBoardUtil.generate_random_move(board,color,False)
            else:
                move = PatternUtil.generate_move_with_filter(board,use_pattern,check_selfatari)
            if move == PASS:
                break
            board.play_move(move, color)
        winner = GoBoardUtil.opponent(color)
        return winner


def point_to_coord(point, boardsize):
    """
    Transform point given as board array index 
    to (row, col) coordinate representation.
    Special case: PASS is not transformed
    """
    if point == PASS:
        return PASS
    else:
        NS = boardsize + 1
        return divmod(point, NS)

def format_point(move):
    """
    Return move coordinates as a string such as 'a1', or 'pass'.
    """
    column_letters = "ABCDEFGHJKLMNOPQRSTUVWXYZ"
    #column_letters = "abcdefghjklmnopqrstuvwxyz"
    if move == PASS:
        return "pass"
    row, col = move
    if not 0 <= row < MAXSIZE or not 0 <= col < MAXSIZE:
        raise ValueError
    return column_letters[col - 1]+ str(row) 
    