import pygame
from draw_board import draw_board
from pieces import WhiteKing, WhiteBishop, BlackKing
import sys

if len(sys.argv) > 1:
    if sys.argv[1].lower() == '-w':
        white_turn = True
    else:
        white_turn = False
else:
    white_turn = True
pygame.init()

white,black,red = (255,255,255),(0,0,0),(255,0,0)

gameDisplay = pygame.display.set_mode((720, 720))

pygame.display.set_caption("ChessBoard")

gameExit = False

draw_board(8, white_turn=white_turn, init=True)
n = 8
surface_sz = 720           # Proposed physical surface size.
sq_sz = surface_sz // n    # sq_sz is length of a square.
surface = pygame.display.set_mode((surface_sz + 20, surface_sz + 20))
wk = WhiteKing(sq_sz, surface) 
wb = WhiteBishop(sq_sz, surface)
bk = BlackKing(sq_sz, surface)

while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True

        draw_board(8, white_turn=white_turn, init=True)
        pygame.display.flip()

#quit from pygame & python
pygame.quit()
quit()

