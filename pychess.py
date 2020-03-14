import chess
import pygame


board_text = chess.Board()
wp = pygame.image.load("sprites/whitePawn.png")
wk = pygame.image.load("sprites/whiteKing.png")
wn = pygame.image.load("sprites/whiteKnight.png")
wb = pygame.image.load("sprites/whiteBishop.png")
wq = pygame.image.load("sprites/whiteQueen.png")
wr = pygame.image.load("sprites/whiteRook.png")
bp = pygame.image.load("sprites/blackPawn.png")
bk = pygame.image.load("sprites/blackKing.png")
bn = pygame.image.load("sprites/blackKnight.png")
bb = pygame.image.load("sprites/blackBishop.png")
bq = pygame.image.load("sprites/blackQueen.png")
br = pygame.image.load("sprites/blackRook.png")
surface = 720
TILESIZE = surface / 8
BOARD_POS = (10, 10)
def create_board_surf():
    board_surf = pygame.Surface((TILESIZE*8, TILESIZE*8))
    dark = False
    for y in range(8):
        for x in range(8):
            rect = pygame.Rect(x*TILESIZE, y*TILESIZE, TILESIZE, TILESIZE)
            pygame.draw.rect(board_surf, pygame.Color('darkgrey' if dark else 'white'), rect)
            dark = not dark
        dark = not dark
    return board_surf

def get_square_under_mouse(board):
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) - BOARD_POS
    x, y = [int(v // TILESIZE) for v in mouse_pos]
    try: 
        if x >= 0 and y >= 0: return (board[y][x], x, y)
    except IndexError: pass
    return None, None, None

def create_board():
    board = []
    for y in range(8):
        board.append([])
        for x in range(8):
            board[y].append(None)
    board[0][0], board[0][7] = ('black', 'rook'), ('black', 'rook')
    board[0][1], board[0][6] = ('black', 'knight'), ('black', 'knight')
    board[0][2], board[0][5] = ('black', 'bishop'), ('black', 'bishop')
    board[0][3] = ('black', 'queen')
    board[0][4] = ('black', 'king') 
    board[7][0], board[7][7] = ('white', 'rook'), ('white', 'rook')
    board[7][1], board[7][6] = ('white', 'knight'), ('white', 'knight')
    board[7][2], board[7][5] = ('white', 'bishop'), ('white', 'bishop')
    board[7][3] = ('white', 'queen')
    board[7][4] = ('white', 'king') 
    for x in range(0, 8):
        board[1][x] = ('black', 'pawn')
    for x in range(0, 8):
        board[6][x] = ('white', 'pawn') 

    return board

def draw_pieces(screen, board, font, selected_piece):
    sx, sy = None, None
    if selected_piece:
        piece, sx, sy = selected_piece

    for y in range(8):
        for x in range(8): 
            piece = board[y][x]
            if piece:
                selected = x == sx and y == sy
                color, type = piece
                # s1 = font.render(type[0], True, pygame.Color('red' if selected else color))
                # s2 = font.render(type[0], True, pygame.Color('darkgrey'))
                if color == 'white':
                    if type == 'pawn':
                        s1 = wp
                        s2 = wp
                    if type == 'king':
                        s1 = wk
                        s2 = wk
                    if type == 'knight':
                        s1 = wn
                        s2 = wn
                    if type == 'bishop':
                        s1 = wb
                        s2 = wb
                    if type == 'queen':
                        s1 = wq
                        s2 = wq
                    if type == 'rook':
                        s1 = wr
                        s2 = wr
                else:
                    if type == 'pawn':
                        s1 = bp
                        s2 = bp
                    if type == 'king':
                        s1 = bk
                        s2 = bk
                    if type == 'knight':
                        s1 = bn
                        s2 = bn
                    if type == 'bishop':
                        s1 = bb
                        s2 = bb
                    if type == 'queen':
                        s1 = bq
                        s2 = bq
                    if type == 'rook':
                        s1 = br
                        s2 = br
                pos = pygame.Rect(BOARD_POS[0] + x * TILESIZE+1, BOARD_POS[1] + y * TILESIZE + 1, TILESIZE, TILESIZE)
                screen.blit(s2, s2.get_rect(center=pos.center).move(1, 1))
                screen.blit(s1, s1.get_rect(center=pos.center))

def draw_selector(screen, piece, x, y):
    if piece != None and piece != 0:
        rect = (BOARD_POS[0] + x * TILESIZE, BOARD_POS[1] + y * TILESIZE, TILESIZE, TILESIZE)
        pygame.draw.rect(screen, (255, 0, 0, 50), rect, 2)

def draw_drag(screen, board, selected_piece, font):
    if selected_piece and selected_piece[0] != 0:
        piece, x, y = get_square_under_mouse(board)
        start_pos = x, y
        if x != None:
            rect = (BOARD_POS[0] + x * TILESIZE, BOARD_POS[1] + y * TILESIZE, TILESIZE, TILESIZE)
        pygame.draw.rect(screen, (0, 255, 0, 50), rect, 2)

        color, type = selected_piece[0]
        # s1 = font.render(type[0], True, pygame.Color(color))
        # s2 = font.render(type[0], True, pygame.Color('darkgrey'))
        if color == 'white':
            if type == 'pawn':
                s1 = wp
                s2 = wp
            if type == 'king':
                s1 = wk
                s2 = wk
            if type == 'knight':
                s1 = wn
                s2 = wn
            if type == 'bishop':
                s1 = wb
                s2 = wb
            if type == 'queen':
                s1 = wq
                s2 = wq
            if type == 'rook':
                s1 = wr
                s2 = wr
        else:
            if type == 'pawn':
                s1 = bp
                s2 = bp
            if type == 'king':
                s1 = bk
                s2 = bk
            if type == 'knight':
                s1 = bn
                s2 = bn
            if type == 'bishop':
                s1 = bb
                s2 = bb
            if type == 'queen':
                s1 = bq
                s2 = bq
            if type == 'rook':
                s1 = br
                s2 = br

        pos = pygame.Vector2(pygame.mouse.get_pos())
        screen.blit(s2, s2.get_rect(center=pos + (1, 1)))
        screen.blit(s1, s1.get_rect(center=pos))
        selected_rect = pygame.Rect(BOARD_POS[0] + selected_piece[1] * TILESIZE, BOARD_POS[1] + selected_piece[2] * TILESIZE, TILESIZE, TILESIZE)
        # debug drag line
        # pygame.draw.line(screen, pygame.Color('red'), selected_rect.center, pos)
        return (x, y, selected_piece[0], start_pos)

def main():
    column_to_letter = {0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f',
            6:'g', 7:'h'}
    row_convert = {0:8, 1:7, 2:6, 3:5, 4:4, 5:3, 6:2, 7:1}
    pygame.init()
    screen = pygame.display.set_mode((720, 720))
    font = pygame.font.Font('freesansbold.ttf', 40)
    text = font.render('Game Over!', True, (255, 0, 0))
    textRect = text.get_rect(center=screen.get_rect().center) 
    board = create_board()
    board_surf = create_board_surf()
    clock = pygame.time.Clock()
    selected_piece = None
    drop_pos = None
    while True:
        piece, x, y = get_square_under_mouse(board)
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                return
            if e.type == pygame.MOUSEBUTTONDOWN:
                if piece != None:
                    selected_piece = piece, x, y
                    start_piece = x, y
            
            if e.type == pygame.MOUSEBUTTONUP:
                if drop_pos:
                    moved_piece = drop_pos[2]
                    drop_pos = drop_pos[0], drop_pos[1]
                    if start_piece != drop_pos:
                        lt1_pos = str(column_to_letter[start_piece[0]])
                        row1_pos = str(row_convert[start_piece[1]]) 
                        lt2_pos = str(column_to_letter[drop_pos[0]])
                        row2_pos = str(row_convert[drop_pos[1]]) 
                        uci = lt1_pos + row1_pos + lt2_pos + row2_pos
                        print(uci)
                        print(board_text.legal_moves)
                        legal = chess.Move.from_uci(uci) in board_text.legal_moves
                        if legal:
                            board_text.push_uci(uci)
                            piece, old_x, old_y = selected_piece
                            board[old_y][old_x] = 0
                            new_x, new_y = drop_pos
                            board[new_y][new_x] = piece
                        if board_text.is_game_over():
                            board_surf.blit(text, textRect)  
                            print('checkm8')
                selected_piece = None
                drop_pos = None

        screen.fill(pygame.Color('grey'))
        screen.blit(board_surf, BOARD_POS)
        draw_pieces(screen, board, font, selected_piece)
        draw_selector(screen, piece, x, y)
        drop_pos = draw_drag(screen, board, selected_piece, font)
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
