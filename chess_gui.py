#!/bin/python
from chess_utils import Board, Game


if __name__ == '__main__':
    game = Game()
    game.game_init(1000, 840)
    game.game_loop()
