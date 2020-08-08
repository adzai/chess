import chess
import pygame


class Square():
    def __init__(self, fen_char=None, x=None, y=None, can_use=False):
        self.fen_char = fen_char
        self.x = x
        self.y = y
        self.can_use = can_use

    def set_square(self, fen_char, x, y):
        self.fen_char = fen_char
        self.x = x
        self.y = y
        self.can_use = True


board_text = chess.Board()
sprites = {
    'P': pygame.image.load("sprites/whitePawn.png"),
    'K': pygame.image.load("sprites/whiteKing.png"),
    'N': pygame.image.load("sprites/whiteKnight.png"),
    'B': pygame.image.load("sprites/whiteBishop.png"),
    'Q': pygame.image.load("sprites/whiteQueen.png"),
    'R': pygame.image.load("sprites/whiteRook.png"),
    'p': pygame.image.load("sprites/blackPawn.png"),
    'k': pygame.image.load("sprites/blackKing.png"),
    'n': pygame.image.load("sprites/blackKnight.png"),
    'b': pygame.image.load("sprites/blackBishop.png"),
    'q': pygame.image.load("sprites/blackQueen.png"),
    'r': pygame.image.load("sprites/blackRook.png"),
}

king_squares = {'k': [0, 0], 'K': [0, 0]}
surface = 720
TILESIZE = surface // 8
BOARD_POS = (0, 0)


def create_board_surf():
    board_surf = pygame.Surface((TILESIZE*8, TILESIZE*8))
    dark = False
    for y in range(8):
        for x in range(8):
            rect = pygame.Rect(x*TILESIZE, y*TILESIZE, TILESIZE, TILESIZE)
            pygame.draw.rect(board_surf, pygame.Color(
                'darkgrey' if dark else 'white'), rect)
            dark = not dark
        dark = not dark
    return board_surf


def get_square_under_mouse(board):
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) - BOARD_POS
    x, y = [int(v // TILESIZE) for v in mouse_pos]
    try:
        if x >= 0 and y >= 0:
            return Square(board[y][x], x, y, True)
    except IndexError:
        pass
    return Square()


def get_promotion_piece(screen, queen_rect, rook_rect,
                        knight_rect, bishop_rect, button_up=False):
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


def draw_king_check(screen, board, piece):
    x, y = king_squares[piece]
    rect = (BOARD_POS[0] + y * TILESIZE, BOARD_POS[1] + x *
            TILESIZE, TILESIZE, TILESIZE)
    pygame.draw.rect(screen, (255, 0, 0, 50), rect, 2)


def fen_to_rect(fen_str):
    board = []
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
            fen_char = new_fen_str[i]
            board[x][y] = fen_char
            if fen_char in 'kK':
                king_squares[fen_char] = [x, y]
            i += 1
    return board


def draw_pieces(screen, board, font, initial_square):
    for y in range(8):
        for x in range(8):
            piece = board[y][x]
            if piece:
                if piece.isalpha():
                    s1 = sprites[piece]
                    pos = pygame.Rect(BOARD_POS[0] + x * TILESIZE+1,
                                      BOARD_POS[1] + y * TILESIZE + 1,
                                      TILESIZE, TILESIZE)
                    screen.blit(s1, s1.get_rect(center=pos.center))


def draw_selector(screen, piece):
    if piece.fen_char:
        rect = (BOARD_POS[0] + piece.x * TILESIZE, BOARD_POS[1] +
                piece.y * TILESIZE, TILESIZE, TILESIZE)
        pygame.draw.rect(screen, (0, 0, 255, 50), rect, 2)


def draw_promotion_selector(screen, rect_bool, rect):
    if rect_bool:
        pygame.draw.rect(screen, (255, 0, 0, 50), rect, 2)


def draw_drag(screen, board, initial_square, font):
    if initial_square.can_use:
        square_under_mouse = get_square_under_mouse(board)
        if square_under_mouse.can_use:
            uci, _ = board_to_uci(initial_square, square_under_mouse)
            rect = (BOARD_POS[0] + square_under_mouse.x
                    * TILESIZE, BOARD_POS[1] + square_under_mouse.y *
                    TILESIZE, TILESIZE, TILESIZE)
            if chess.Move.from_uci(uci) in board_text.legal_moves:
                pygame.draw.rect(screen, (0, 255, 0, 50), rect, 2)
            else:
                pygame.draw.rect(screen, (255, 0, 0, 50), rect, 2)
        if initial_square.fen_char.isalpha():
            s1 = sprites[initial_square.fen_char]

            pos = pygame.Vector2(pygame.mouse.get_pos())
            screen.blit(s1, s1.get_rect(center=pos))
        return square_under_mouse
    return initial_square


def promotion_loop(screen, color):
    clock = pygame.time.Clock()
    if color:
        q = sprites['Q']
        r = sprites['R']
        n = sprites['N']
        b = sprites['B']
    else:
        q = sprites['q']
        r = sprites['r']
        n = sprites['n']
        b = sprites['b']
    while True:
        left = 16
        top = 250
        width = 160
        height = 160
        filled = 0
        pygame.draw.rect(screen, [211, 211, 211],
                         [left, top, width, height], filled)
        queen_rect = pygame.Rect(left, top, width, height)
        screen.blit(q, q.get_rect(center=queen_rect.center))
        left += width + 16
        pygame.draw.rect(screen, [211, 211, 211],
                         [left, top, width, height], filled)
        rook_rect = pygame.Rect(left, top, width, height)
        screen.blit(r, r.get_rect(center=rook_rect.center))
        left += width + 16
        knight_rect = pygame.Rect(left, top, width, height)
        pygame.draw.rect(screen, [211, 211, 211],
                         [left, top, width, height], filled)
        screen.blit(n, n.get_rect(center=knight_rect.center))
        left += width + 16
        pygame.draw.rect(screen, [211, 211, 211],
                         [left, top, width, height], filled)
        bishop_rect = pygame.Rect(left, top, width, height)
        screen.blit(b, b.get_rect(center=bishop_rect.center))
        events = pygame.event.get()
        for e in events:
            get_promotion_piece(screen, queen_rect, rook_rect,
                                knight_rect, bishop_rect)
            pygame.display.flip()
            if e.type == pygame.MOUSEBUTTONUP:
                promotion_piece = get_promotion_piece(
                    screen, queen_rect, rook_rect,
                    knight_rect, bishop_rect, button_up=True)
                return promotion_piece
        clock.tick(60)


def board_to_uci(initial_square, drop_square):
    column_to_letter = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f',
                        6: 'g', 7: 'h'}
    row_convert = {0: 8, 1: 7, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1}
    lt1_pos = str(column_to_letter[initial_square.x])
    row1_pos = str(row_convert[initial_square.y])
    lt2_pos = str(column_to_letter[drop_square.x])
    row2_pos = str(row_convert[drop_square.y])
    uci = lt1_pos + row1_pos + lt2_pos + row2_pos
    promotion = False
    if uci[:2] == uci[2:]:
        uci = '0000'
    elif (initial_square.fen_char in 'pP' and
          (uci[-1] == '8' or uci[-1] == '1')):
        # placeholder promotion for checking legality of the move
        uci += 'q'
        promotion = True
    return uci, promotion


def main():
    pygame.init()
    screen = pygame.display.set_mode((720, 720))
    font = pygame.font.Font('freesansbold.ttf', 40)
    check_mate_text = font.render('Game Over!', True, (255, 0, 0))
    check_mate_text_rect = check_mate_text.get_rect(
        center=screen.get_rect().center)
    rect_board = fen_to_rect(board_text.fen())
    board_surf = create_board_surf()
    clock = pygame.time.Clock()
    initial_square = Square()
    drop_square = Square()
    white = True
    while True:
        square_under_mouse = get_square_under_mouse(rect_board)
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                return
            if e.type == pygame.MOUSEBUTTONDOWN:
                if square_under_mouse.can_use:
                    initial_square.set_square(square_under_mouse.fen_char,
                                              square_under_mouse.x,
                                              square_under_mouse.y)
            if e.type == pygame.MOUSEBUTTONUP:
                if drop_square.can_use:
                    if initial_square != drop_square:
                        uci, promotion = board_to_uci(initial_square,
                                                      drop_square)
                        legal = chess.Move.from_uci(uci) in \
                            board_text.legal_moves
                        if legal:
                            if promotion:
                                uci = uci[:-1] + promotion_loop(screen, white)
                            promotion = False
                            board_text.push_uci(uci)
                            rect_board = fen_to_rect(board_text.fen())
                            white = not white
                        if board_text.is_game_over():
                            board_surf.blit(check_mate_text,
                                            check_mate_text_rect)
                initial_square.can_use = False
                drop_square.can_use = False
        screen.blit(board_surf, BOARD_POS)
        draw_pieces(screen, rect_board, font, initial_square)
        draw_selector(screen, square_under_mouse)
        drop_square = draw_drag(screen, rect_board, initial_square, font)
        if board_text.is_check():
            if white:
                draw_king_check(screen, rect_board, 'K')
            else:
                draw_king_check(screen, rect_board, 'k')
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
