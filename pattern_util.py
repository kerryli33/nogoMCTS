"""
pattern_util.py
Utility functions for rule based simulations.
"""

import numpy as np
from pattern import pat3set
import random
from board_util import GoBoardUtil, EMPTY, PASS, BORDER


class PatternUtil(object):

    @staticmethod
    def generate_move_with_filter(board, use_pattern, check_selfatari):
        """
        Arguments
        ---------
        check_selfatari: filter selfatari moves?
        Note that even if True, this filter only applies to pattern moves
        use_pattern: Use pattern policy?
        """
        move = None
        if use_pattern:
            moves = PatternUtil.generate_pattern_moves(board)
            move = PatternUtil.filter_moves_and_generate(board, moves,
                                                         check_selfatari)
        if move == None:
            move = GoBoardUtil.generate_random_move(board, board.current_player,True)
        return move

    @staticmethod
    def playGame(board, color, **kwargs):
        """
        Run a simulation game according to give parameters.
        """
        # komi = kwargs.pop('komi', 0)
        limit = kwargs.pop('limit', 1000)
        random_simulation = kwargs.pop('random_simulation',True)
        use_pattern = kwargs.pop('use_pattern',True)
        check_selfatari = kwargs.pop('check_selfatari',True)
        if kwargs:
            raise TypeError('Unexpected **kwargs: %r' % kwargs)
        nuPasses = 0
        for _ in range(limit):
            color = board.current_player
            if random_simulation:
                move = GoBoardUtil.generate_random_move(board,color,False)
            else:
                move = PatternUtil.generate_move_with_filter(board,use_pattern,check_selfatari)
            board.play_move(move, color)
            if move == PASS:
                nuPasses += 1
            else:
                nuPasses = 0
            if nuPasses >= 2:
                break
        winner,_ = board.score(0)
        return winner
