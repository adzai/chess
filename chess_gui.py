#!/bin/python
from chess_utils import Board, Game


if __name__ == '__main__':
    game = Game()
    game.game_init(720, 720)
    board = Board(720, (0, 0))
    board.board_init()
    game.game_loop(board)
