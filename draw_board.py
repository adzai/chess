import pygame


def draw_board(the_board, **kwargs):
    """ Draws starting chess position. """

    white_turn = kwargs['white_turn']
    init = kwargs['init']
    white = (255, 255, 255)
    blue = (0, 0, 128) 
    brown = (94, 61, 61)
    black = (0, 0, 0)
    colors = [brown, white]    # Set up colors [red, black]

    n = the_board         # This is an NxN chess board.
    surface_sz = 720           # Proposed physical surface size.
    sq_sz = surface_sz // n    # sq_sz is length of a square.
    surface_sz = n * sq_sz     # Adjust to exactly fit n squares.

    # Create the surface of (width, height), and its window.
    surface = pygame.display.set_mode((surface_sz + 20, surface_sz + 20))

    black_queen = pygame.image.load("sprites/blackQueen.png")
    black_king = pygame.image.load("sprites/blackKing.png")
    black_knight = pygame.image.load("sprites/blackKnight.png")
    black_bishop = pygame.image.load("sprites/blackBishop.png")
    black_pawn = pygame.image.load("sprites/blackPawn.png")
    black_rook = pygame.image.load("sprites/blackRook.png")
    white_queen = pygame.image.load("sprites/whiteQueen.png")
    white_king = pygame.image.load("sprites/whiteKing.png")
    white_knight = pygame.image.load("sprites/whiteKnight.png")
    white_bishop = pygame.image.load("sprites/whiteBishop.png")
    white_pawn = pygame.image.load("sprites/whitePawn.png")
    white_rook = pygame.image.load("sprites/whiteRook.png")
    # ball = pygame.transform.scale(ball, (100, 100))
    # Use an extra offset to centre the ball in its square.
    # If the square is too small, offset becomes negative,
    #   but it will still be centered :-)
    black_bishop_offset = (sq_sz-black_bishop.get_width()) // 2
    black_king_offset = (sq_sz-black_king.get_width()) // 2
    black_knight_offset = (sq_sz-black_knight.get_width()) // 2
    black_bishop_offset = (sq_sz-black_bishop.get_width()) // 2
    black_pawn_offset = (sq_sz-black_pawn.get_width()) // 2
    black_rook_offset = (sq_sz-black_rook.get_width()) // 2
    white_queen_offset = (sq_sz-white_queen.get_width()) // 2
    white_king_offset = (sq_sz-white_king.get_width()) // 2
    white_knight_offset = (sq_sz-white_knight.get_width()) // 2
    white_bishop_offset = (sq_sz-white_bishop.get_width()) // 2
    white_pawn_offset = (sq_sz-white_pawn.get_width()) // 2
    white_rook_offset = (sq_sz-white_rook.get_width()) // 2

    
    # Look for an event from keyboard, mouse, etc.
    ev = pygame.event.poll()
    surface.fill((black))
    
    if white_turn:
        # Draw a fresh background (a blank chess board)
        for row in range(n):           # Draw each row of the board.
            c_indx = row % 2           # Alternate starting color
            for col in range(n):       # Run through cols drawing squares
                the_square = (col*sq_sz, row*sq_sz, sq_sz, sq_sz)
                surface.fill(colors[c_indx], the_square)
                # Now flip the color index for the next square
                c_indx = (c_indx + 1) % 2

        
        # trying to annotate board
        width = sq_sz / 2
        for letter in 'ABCDEFGH':
            font = pygame.font.Font('freesansbold.ttf', 18) 
            text = font.render(letter, True, white, black)
            textRect = text.get_rect()
            textRect.center = (width, 730) 
            width += sq_sz
            surface.blit(text, textRect)

        height = 720 - sq_sz / 2 
        for num in range(1, 9):
            font = pygame.font.Font('freesansbold.ttf', 18) 
            text = font.render(str(num), True, white, black)
            textRect = text.get_rect()
            textRect.center = (730, height) 
            height -= sq_sz
            surface.blit(text, textRect)

        # pygame.display.flip()
    else:
        # Draw a fresh background (a blank chess board)
        colors = [white, brown]
        for row in range(n):           # Draw each row of the board.
            c_indx = row % 2           # Alternate starting color
            for col in range(n):       # Run through cols drawing squares
                the_square = (col*sq_sz, row*sq_sz, sq_sz, sq_sz)
                surface.fill(colors[c_indx], the_square)
                # Now flip the color index for the next square
                c_indx = (c_indx + 1) % 2

        
        # trying to annotate board
        width = sq_sz / 2
        for letter in reversed('ABCDEFGH'):
            font = pygame.font.Font('freesansbold.ttf', 18) 
            text = font.render(letter, True, white, black)
            textRect = text.get_rect()
            textRect.center = (width, 730) 
            width += sq_sz
            surface.blit(text, textRect)

        height = 720 - sq_sz / 2 
        for num in reversed(range(1, 9)):
            text = font.render(str(num), True, white, black)
            textRect = text.get_rect()
            textRect.center = (730, height) 
            height -= sq_sz
            surface.blit(text, textRect)

    if init:

        if white_turn:
            c = [0, 7, 1, 6]
        else:
            c = [7, 0, 6, 1]
        # Now that squares are drawn, draw the queens.
        for (col, row) in enumerate(range(0, the_board)):
            # surface.blit(black_bishop,
            #           (col*sq_sz+black_bishop_offset,row*sq_sz+black_bishop_offset))
            if col == c[0]:
                surface.blit(black_rook, (0*sq_sz+black_rook_offset,col*sq_sz+black_rook_offset))
                surface.blit(black_rook, (7*sq_sz+black_rook_offset,col*sq_sz+black_rook_offset))
                surface.blit(black_knight, (1*sq_sz+black_rook_offset,col*sq_sz+black_rook_offset))
                surface.blit(black_knight, (6*sq_sz+black_rook_offset,col*sq_sz+black_rook_offset))
                surface.blit(black_bishop, (2*sq_sz+black_rook_offset,col*sq_sz+black_rook_offset))
                surface.blit(black_bishop, (5*sq_sz+black_rook_offset,col*sq_sz+black_rook_offset))
                if c[0] == 0:
                    surface.blit(black_queen, (3*sq_sz+black_rook_offset,col*sq_sz+black_rook_offset))
                    surface.blit(black_king, (4*sq_sz+black_rook_offset,col*sq_sz+black_rook_offset))
                else:
                    surface.blit(black_queen, (4*sq_sz+black_rook_offset,col*sq_sz+black_rook_offset))
                    surface.blit(black_king, (3*sq_sz+black_rook_offset,col*sq_sz+black_rook_offset))

            if col == c[1]:
                surface.blit(white_rook, (0*sq_sz+black_rook_offset,col*sq_sz+black_rook_offset))
                surface.blit(white_rook, (7*sq_sz+black_rook_offset,col*sq_sz+black_rook_offset))
                surface.blit(white_knight, (1*sq_sz+black_rook_offset,col*sq_sz+black_rook_offset))
                surface.blit(white_knight, (6*sq_sz+black_rook_offset,col*sq_sz+black_rook_offset))
                surface.blit(white_bishop, (2*sq_sz+black_rook_offset,col*sq_sz+black_rook_offset))
                surface.blit(white_bishop, (5*sq_sz+black_rook_offset,col*sq_sz+black_rook_offset))
                if c[1] == 7:
                    surface.blit(white_queen, (3*sq_sz+black_rook_offset,col*sq_sz+black_rook_offset))
                    surface.blit(white_king, (4*sq_sz+black_rook_offset,col*sq_sz+black_rook_offset))
                else:
                    surface.blit(white_queen, (4*sq_sz+black_rook_offset,col*sq_sz+black_rook_offset))
                    surface.blit(white_king, (3*sq_sz+black_rook_offset,col*sq_sz+black_rook_offset))


            if col == c[2]:
                for row in range(0, 9):
                    surface.blit(black_pawn,
                       (row*sq_sz+black_bishop_offset,col*sq_sz+black_bishop_offset))

            if col == c[3]:
                for row in range(0, 9):
                    surface.blit(white_pawn,
                       (row*sq_sz+white_bishop_offset,col*sq_sz+white_bishop_offset))
    pygame.display.flip()
        


if __name__ == "__main__":
    draw_board([0, 1, 2, 3, 4, 5, 6, 7], True)
