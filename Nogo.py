#!/usr/local/bin/python3
#/usr/bin/python3
# Set the path to your python3 above

from gtp_connection import GtpConnection, point_to_coord, format_point
from board_util import GoBoardUtil
from simple_board import SimpleGoBoard
from pattern_util import PatternUtil
from ucb import runUcb
import numpy as np
import argparse
import sys


class Nogo():
    def __init__(self, sim, move_select, sim_rule, move_filter, size=7, limit=100):
        """
        Passe/resigns only at the end of game.

        """
        self.name = "NoGoAssignment2"
        self.version = 1.0
        self.sim = sim
        self.limit = limit
        self.use_ucb = False if move_select =='simple' else True
        self.random_simulation = True if sim_rule == 'random' else False
        self.use_pattern = not self.random_simulation
        self.check_selfatari = move_filter
        
    def get_move(self, board, color):
            """
            Run one-ply MC simulations to get a move to play.
            """
            cboard = board.copy()
            emptyPoints = board.get_empty_points()
            moves = []
            for p in emptyPoints:
                if board.is_legal(p, color):
                    moves.append(p)
            if not moves:
                return None
            moves.append(None)
            if self.use_ucb:
                C = 0.4 #sqrt(2) is safe, this is more aggressive
                best = runUcb(self, cboard, C, moves, color)
                return best
            else:
                moveWins = []
                for move in moves:
                    wins = self.simulateMove(cboard, move, color)
                    moveWins.append(wins)
                writeMoves(cboard, moves, moveWins, self.sim)
                return select_best_move(board, moves, moveWins)
        
    def simulateMove(self, board, move, toplay):
        """
        Run simulations for a given move.
        """
        wins = 0
        for _ in range(self.sim):
            result = self.simulate(board, move, toplay)
            if result == toplay:
                wins += 1
        return wins

    def simulate(self, board, move, toplay):
        cboard = board.copy()
        cboard.play_move(move, toplay)
        opp = GoBoardUtil.opponent(toplay)
        return PatternUtil.playGame(cboard,
                                    opp,
                                    komi=self.komi,
                                    limit=self.limit,
                                    random_simulation = self.random_simulation,
                                    use_pattern = self.use_pattern,
                                    check_selfatari = self.check_selfatari)
def run():
    """
    start the gtp connection and wait for commands.
    """
    board = SimpleGoBoard(7)
    con = GtpConnection(Nogo(), board)
    con.start_connection()

def byPercentage(pair):
    return pair[1]

def writeMoves(board, moves, count, numSimulations):
    """
    Write simulation results for each move.
    """
    gtp_moves = []
    for i in range(len(moves)):
        if moves[i] != None:
            x, y = point_to_coord(moves[i], board.size)
            gtp_moves.append((format_point((x, y)),
                              float(count[i])/float(numSimulations)))
        else:
            gtp_moves.append(('Pass',float(count[i])/float(numSimulations)))
    sys.stderr.write("win rates: {}\n"
                     .format(sorted(gtp_moves, key = byPercentage,
                                    reverse = True)))
    sys.stderr.flush()

def select_best_move(board, moves, moveWins):
    """
    Move select after the search.
    """
    max_child = np.argmax(moveWins)
    return moves[max_child]

if __name__=='__main__':
    run()
