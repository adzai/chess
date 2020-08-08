import chess
import pygame
import time


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
TILESIZE = surface // 8
BOARD_POS = (0, 0)


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

def get_promotion_piece(screen, queen_rect, rook_rect, knight_rect, bishop_rect, button_up=False):
    y = range(250, 410)
    queen_x = range(16, 177)
    rook_x = range(192, 353)
    knight_x = range(368, 529)
    bishop_x = range(544, 705)
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
    if mouse_pos[1] in y:
        if mouse_pos[0] in queen_x:
            if button_up:
                return 'q'
            pygame.draw.rect(screen, (0, 0, 0, 50), queen_rect, 1)
        if mouse_pos[0] in rook_x:
            if button_up:
                return 'r'
            pygame.draw.rect(screen, (0, 0, 0, 50), rook_rect, 1)
        if mouse_pos[0] in knight_x:
            if button_up:
                return 'n'
            pygame.draw.rect(screen, (0, 0, 0, 50), knight_rect, 1)
        if mouse_pos[0] in bishop_x:
            if button_up:
                return 'b'
            pygame.draw.rect(screen, (0, 0, 0, 255), bishop_rect, 1)

def draw_king_check(screen, board, color):
    for i in range(8):
        for j in range(8):
            if board[i][j] == (color, 'king'):
                rect = (BOARD_POS[0] + j * TILESIZE, BOARD_POS[1] + i * TILESIZE, TILESIZE, TILESIZE)
                pygame.draw.rect(screen, (255, 0, 0, 50), rect, 2)

def fen_to_rect(fen_str):
    board = []
    fen_map = {'p': ('black', 'pawn'), 'n': ('black', 'knight'), 'b': ('black', 'bishop'),
               'q': ('black', 'queen'), 'k': ('black', 'king'), 'r' : ('black', 'rook'),
               'P': ('white', 'pawn'), 'N': ('white', 'knight'), 'B': ('white', 'bishop'),
               'Q': ('white', 'queen'), 'K': ('white', 'king'), 'R' : ('white', 'rook'),    }
    new_fen_str = ""
    for char in fen_str:
        if char.isdigit():
             new_fen_str += int(char) * char
        elif char == "/":
             pass
        else:
             new_fen_str += char
    i = 0
    for y in range(8):
        board.append([])
        for x in range(8):
            board[y].append(None)
    for x in range(8):
        for y in range(8):
            try:
                board[x][y] = fen_map[new_fen_str[i]]
            except:
                pass
            i += 1
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
        pygame.draw.rect(screen, (0, 0, 255, 50), rect, 2)

def draw_promotion_selector(screen, rect_bool, rect):
    if rect_bool:
        pygame.draw.rect(screen, (255, 0, 0, 50), rect, 2)

def draw_drag(screen, board, selected_piece, font, start_piece, column_to_letter, row_convert):
    if selected_piece and selected_piece[0] != 0:
        piece, x, y = get_square_under_mouse(board)
        start_pos = x, y
        if x != None:
            rect = (BOARD_POS[0] + x * TILESIZE, BOARD_POS[1] + y * TILESIZE, TILESIZE, TILESIZE)
            lt1_pos = str(column_to_letter[start_piece[0]])
            row1_pos = str(row_convert[start_piece[1]]) 
            lt2_pos = str(column_to_letter[x])
            row2_pos = str(row_convert[y]) 
            if lt1_pos + row1_pos == lt2_pos + row2_pos:
                uci = '0000'
            else:
                uci = lt1_pos + row1_pos + lt2_pos + row2_pos
            if (selected_piece[0][1] == 'pawn' and (uci[-1] == '8' or uci[-1] == '1')):
                uci += 'q'
            if chess.Move.from_uci(uci) in board_text.legal_moves:
                pygame.draw.rect(screen, (0, 255, 0, 50), rect, 2)
            else:
                pygame.draw.rect(screen, (255, 0, 0, 50), rect, 2)

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
    
def promotion_loop(screen, piece_color):
    if piece_color == 'white':
        q = wq
        r = wr
        n = wn
        b = wb
    else:
        q = bq
        r = br
        n = bn
        b = bb
    while True:
        events = pygame.event.get()
        for e in events:
            left=16
            top=250
            width=160
            height=160
            filled=0
            pygame.draw.rect(screen, [211, 211, 211], [left, top, width, height], filled)
            queen_rect = pygame.Rect(left, top, width, height)
            screen.blit(q, q.get_rect(center=queen_rect.center))
            left+= width + 16
            pygame.draw.rect(screen, [211, 211, 211], [left, top, width, height], filled)
            rook_rect = pygame.Rect(left, top, width, height)
            screen.blit(r, r.get_rect(center=rook_rect.center))
            left+= width + 16
            knight_rect = pygame.Rect(left, top, width, height)
            pygame.draw.rect(screen, [211, 211, 211], [left, top, width, height], filled)
            screen.blit(n, n.get_rect(center=knight_rect.center))
            left+= width + 16
            pygame.draw.rect(screen, [211, 211, 211], [left, top, width, height], filled)
            bishop_rect = pygame.Rect(left, top, width, height)
            screen.blit(b, b.get_rect(center=bishop_rect.center))
            get_promotion_piece(screen, queen_rect, rook_rect, knight_rect, bishop_rect)
            pygame.display.flip()
            if e.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
                promotion_piece = get_promotion_piece(screen, queen_rect, rook_rect,
                                                                       knight_rect, bishop_rect, button_up=True)
                return promotion_piece

def main():
    column_to_letter = {0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f',
            6:'g', 7:'h'}
    row_convert = {0:8, 1:7, 2:6, 3:5, 4:4, 5:3, 6:2, 7:1}
    pygame.init()
    screen = pygame.display.set_mode((720, 720))
    font = pygame.font.Font('freesansbold.ttf', 40)
    check_mate_text = font.render('Game Over!', True, (255, 0, 0))
    check_text = font.render('Check!', True, (0, 0, 0))
    check_text_rect = check_text.get_rect(center=screen.get_rect().center) 
    check_mate_text_rect = check_mate_text.get_rect(center=screen.get_rect().center) 
    board = fen_to_rect(board_text.fen())
    board_surf = create_board_surf()
    clock = pygame.time.Clock()
    selected_piece = None
    drop_pos = None
    white = True
    start_piece = 0, 0
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
                        fen_str = ""
                        if (selected_piece[0][1] == 'pawn' and (uci[-1] == '8' or uci[-1] == '1')):
                            uci += promotion_loop(screen, selected_piece[0][0])
                        legal = chess.Move.from_uci(uci) in board_text.legal_moves
                        if legal:
                            board_text.push_uci(uci)
                            board = fen_to_rect(board_text.fen())
                            white = not white
                        if board_text.is_game_over():
                            board_surf.blit(check_mate_text, check_mate_text_rect)  
                            print('checkm8')
                selected_piece = None
                drop_pos = None
        screen.blit(board_surf, BOARD_POS)
        draw_pieces(screen, board, font, selected_piece)
        draw_selector(screen, piece, x, y)
        drop_pos = draw_drag(screen, board, selected_piece, font, start_piece, column_to_letter, row_convert)
        if board_text.is_check():
            if white:
                draw_king_check(screen, board, 'white')
            else:
                draw_king_check(screen, board, 'black')
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
