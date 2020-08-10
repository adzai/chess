#!/bin/python
import pygame
import chess
import chess.polyglot
import ai
from collections import defaultdict


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


class Game():
    def __init(self):
        self.clock = None
        self.screen = None
        self.font = None
        self.check_mate_text = None
        self.check_mate_text_rect = None

    def game_init(self, screen_width, screen_height):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('freesansbold.ttf', 40)
        self.check_mate_text = self.font.render('Game Over!', True,
                                                (255, 0, 0))
        self.check_mate_text_rect = self.check_mate_text.get_rect(
            center=self.screen.get_rect().center)

    def game_loop(self, board):
        initial_square = Square()
        drop_square = Square()
        # False for ai with white pieces
        white = True
        player_turn = True
        white_maximizing = not player_turn
        value = 0
        square_under_mouse = Square(None, None, None, False)
        last_square = None
        ai_played_square = None
        while True:
            if not player_turn and not board.board_text.is_game_over():
                opening_moves = []
                with chess.polyglot.open_reader("Eman.bin") as reader:
                    for entry in reader.find_all(board.board_text):
                        opening_moves.append(entry.move)
                if len(opening_moves) > 0:
                    board.board_text.push(opening_moves[0])
                    ai_played_square = str(opening_moves[0])[2:4]
                else:
                    mv = board.minimax(3, -10000, 10000, True, white_maximizing)
                    value = mv[0]
                    print("Val:", value)
                    print("Move:", mv[1])
                    ai_played_square = mv[1][2:4]
                    board.board_text.push_uci(mv[1])
                    white_mv = board.minimax(2, -10000, 10000, True, True)
                    print(f"White_recommended move: {white_mv[1]}, value: {white_mv[0]}")
                white = not white
                player_turn = not player_turn
                if board.board_text.is_game_over():
                    board.board_surf.blit(
                        self.check_mate_text,
                        self.check_mate_text_rect)
                board.rect_board = board.fen_to_board()
            else:
                square_under_mouse = board.get_square_under_mouse()
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
                                uci, promotion = board.board_to_uci(
                                    initial_square, drop_square)
                                legal = chess.Move.from_uci(uci) in \
                                    board.board_text.legal_moves
                                if legal:
                                    last_square = drop_square
                                    if promotion:
                                        # add extra uci notation if a player is
                                        # promoting and draw the promotion
                                        # choice menu
                                        uci = uci[:-1] + board.promotion_loop(
                                            self.screen, white)
                                    promotion = False
                                    board.board_text.push_uci(uci)
                                    board.rect_board = board.fen_to_board()
                                    white = not white
                                    player_turn = not player_turn
                                if board.board_text.is_game_over():
                                    board.board_surf.blit(
                                        self.check_mate_text,
                                        self.check_mate_text_rect)
                        initial_square.can_use = False
                        drop_square.can_use = False
            self.screen.blit(board.board_surf, board.board_pos)
            if last_square and not player_turn:
                board.draw_last_piece_player(self.screen, last_square)
            if ai_played_square and player_turn:
                board.draw_last_piece_ai(self.screen, ai_played_square)
            board.draw_pieces(self.screen)
            board.draw_selector(self.screen, square_under_mouse)
            drop_square = board.draw_drag(
                self.screen, initial_square)
            # draw a req square around the king if he is in check
            if board.board_text.is_check():
                if white:
                    board.draw_king_check(
                        self.screen, 'K')
                else:
                    board.draw_king_check(
                        self.screen, 'k')
            pygame.display.flip()
            self.clock.tick(60)


class Board():
    def __init__(self, surface, board_pos):
        self.surface = surface
        self.king_squares = {'k': [0, 0], 'K': [0, 0]}
        self.tilesize = surface / 8
        self.board_pos = board_pos
        self.board_text = None
        self.rect_board = None
        self.board_surf = None
        self.sprites = {
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
        self.position_value_map = {
            'P': [0,  0,  0,  0,  0,  0,  0,  0,
             50, 50, 50, 50, 50, 50, 50, 50,
             10, 10, 20, 30, 30, 20, 10, 10,
              5,  5, 10, 27, 27, 10,  5,  5,
              0,  0,  0, 25, 25,  0,  0,  0,
              5, -5,-10,  0,  0,-10, -5,  5,
              5, 10, 10,-25,-25, 10, 10,  5,
              0,  0,  0,  0,  0,  0,  0,  0
            ],
            'N': 
            [-50,-40,-30,-30,-30,-30,-40,-50,
            -40,-20,  0,  0,  0,  0,-20,-40,
            -30,  0, 10, 15, 15, 10,  0,-30,
            -30,  5, 15, 20, 20, 15,  5,-30,
            -30,  0, 15, 20, 20, 15,  0,-30,
            -30,  5, 10, 15, 15, 10,  5,-30,
            -40,-20,  0,  5,  5,  0,-20,-40,
            -50,-40,-30,-30,-30,-30,-40,-50],
            'B': [
                -20,-10,-10,-10,-10,-10,-10,-20,
                -10,  0,  0,  0,  0,  0,  0,-10,
                -10,  0,  5, 10, 10,  5,  0,-10,
                -10,  5,  5, 10, 10,  5,  5,-10,
                -10,  0, 10, 10, 10, 10,  0,-10,
                -10, 10, 10, 10, 10, 10, 10,-10,
                -10,  5,  0,  0,  0,  0,  5,-10,
                -20,-10,-10,-10,-10,-10,-10,-20],
            'R': [
                0,  0,  0,  0,  0,  0,  0,  0,
                  5, 10, 10, 10, 10, 10, 10,  5,
                 -5,  0,  0,  0,  0,  0,  0, -5,
                 -5,  0,  0,  0,  0,  0,  0, -5,
                 -5,  0,  0,  0,  0,  0,  0, -5,
                 -5,  0,  0,  0,  0,  0,  0, -5,
                 -5,  0,  0,  0,  0,  0,  0, -5,
                  0,  0,  0,  5,  5,  0,  0,  0
            ],
            'Q': [
                -20,-10,-10, -5, -5,-10,-10,-20,
                -10,  0,  0,  0,  0,  0,  0,-10,
                -10,  0,  5,  5,  5,  5,  0,-10,
                 -5,  0,  5,  5,  5,  5,  0, -5,
                  0,  0,  5,  5,  5,  5,  0, -5,
                -10,  5,  5,  5,  5,  5,  0,-10,
                -10,  0,  5,  0,  0,  0,  0,-10,
                -20,-10,-10, -5, -5,-10,-10,-20
            ],
            'K': [
                -30,-40,-40,-50,-50,-40,-40,-30,
                -30,-40,-40,-50,-50,-40,-40,-30,
                -30,-40,-40,-50,-50,-40,-40,-30,
                -30,-40,-40,-50,-50,-40,-40,-30,
                -20,-30,-30,-40,-40,-30,-30,-20,
                -10,-20,-20,-20,-20,-20,-20,-10,
                 20, 20,  0,  0,  0,  0, 20, 20,
                 20, 30, 10,  0,  0, 10, 30, 20
                    ],
            'E': [
                 -50,-40,-30,-20,-20,-30,-40,-50,
                 -30,-20,-10,  0,  0,-10,-20,-30,
                 -30,-10, 20, 30, 30, 20,-10,-30,
                 -30,-10, 30, 40, 40, 30,-10,-30,
                 -30,-10, 30, 40, 40, 30,-10,-30,
                 -30,-10, 20, 30, 30, 20,-10,-30,
                 -30,-30,  0,  0,  0,  0,-30,-30,
                 -50,-30,-30,-30,-30,-30,-30,-50
            ],
        }
        self.value_map = {
            'R': 500,
            'N': 320,
            'B': 330,
            'Q': 900,
            'K': 20000,
            'P': 100,
            'r': 500,
            'n': 320,
            'b': 330,
            'q': 900,
            'k': 20000,
            'p': 100,
            }

    def board_init(self):
        self.board_text = chess.Board()
        self.rect_board = self.fen_to_board()
        self.board_surf = self.create_board_surf()
        for c in 'pnbrqke':
            self.position_value_map[c] = self.position_value_map[c.upper()][::-1]


    def make_pygame_rect(self, x, y, offset=0):
        return pygame.Rect(x * self.tilesize + offset,
                           y * self.tilesize + offset,
                           self.tilesize, self.tilesize)

    # Populates the board matrix with fen notation
    def fen_to_board(self):
        fen_str = self.board_text.fen()
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
                    self.king_squares[fen_char] = [x, y]
                i += 1
        return board

    def create_board_surf(self):
        board_surf = pygame.Surface((self.tilesize * 8, self.tilesize * 8))
        dark = False
        for y in range(8):
            for x in range(8):
                rect = pygame.Rect(x * self.tilesize, y * self.tilesize,
                                   self.tilesize, self.tilesize)
                pygame.draw.rect(board_surf, pygame.Color(
                    'darkgrey' if dark else 'white'), rect)
                dark = not dark
            dark = not dark
        return board_surf

    def get_square_under_mouse(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) - self.board_pos
        x, y = [int(v // self.tilesize) for v in mouse_pos]
        try:
            if x >= 0 and y >= 0:
                return Square(self.rect_board[y][x], x, y, True)
        except IndexError:
            pass
        return Square()

    # Blue selector, highlighting a square under the mouse
    def draw_selector(self, screen, piece):
        if piece.can_use:
            rect = self.make_pygame_rect(self.board_pos[0] + piece.x,
                                         self.board_pos[1] + piece.y)
            pygame.draw.rect(screen, (0, 0, 255, 50), rect, 2)

    # Takes x and y coordinates from the board matrix
    # and transforms them into the uci notation
    def board_to_uci(self, initial_square, drop_square):
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

    # Draws a red square when a king is in check
    def draw_king_check(self, screen, piece):
        x, y = self.king_squares[piece]
        rect = self.make_pygame_rect(self.board_pos[0] + y,
                                     self.board_pos[1] + x)
        pygame.draw.rect(screen, (255, 0, 0, 50), rect, 2)

    def draw_last_piece_ai(self, screen, square):
        letter_to_column = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5,
                            'g': 6, 'h': 7}
        row_convert = {8: 0, 7: 1, 6: 2, 5: 3, 4: 4, 3: 5, 2: 6, 1: 7}
        x = letter_to_column[square[0]] 
        y = row_convert[int(square[1])] 
        rect = self.make_pygame_rect(self.board_pos[0] + x,
                                     self.board_pos[1] + y)
        pygame.draw.rect(screen, (0, 0, 0, 50), rect, 2)


    def draw_last_piece_player(self, screen, square):
        x = square.x
        y = square.y
        rect = self.make_pygame_rect(self.board_pos[0] + x,
                                     self.board_pos[1] + y)
        pygame.draw.rect(screen, (0, 0, 0, 50), rect, 2)

    def draw_pieces(self, screen):
        for y in range(8):
            for x in range(8):
                piece = self.rect_board[y][x]
                if piece:
                    if piece.isalpha():
                        s1 = self.sprites[piece]
                        pos = self.make_pygame_rect(self.board_pos[0] + x,
                                                    self.board_pos[1] + y,
                                                    offset=1)
                        screen.blit(s1, s1.get_rect(center=pos.center))

    # Draws dragged piece and highlighting legal moves with green
    # square selectors, illegal with red
    def draw_drag(self, screen, initial_square):
        if initial_square.can_use:
            square_under_mouse = self.get_square_under_mouse()
            if square_under_mouse.can_use:
                uci, _ = self.board_to_uci(initial_square,
                                           square_under_mouse)
                rect = self.make_pygame_rect(self.board_pos[0] +
                                             square_under_mouse.x,
                                             self.board_pos[1] +
                                             square_under_mouse.y)
                if chess.Move.from_uci(uci) in self.board_text.legal_moves:
                    pygame.draw.rect(screen, (0, 255, 0, 50), rect, 2)
                else:
                    pygame.draw.rect(screen, (255, 0, 0, 50), rect, 2)
            if initial_square.fen_char.isalpha():
                s1 = self.sprites[initial_square.fen_char]
                pos = pygame.Vector2(pygame.mouse.get_pos())
                screen.blit(s1, s1.get_rect(center=pos))
            return square_under_mouse
        return initial_square

    # Draws black selectors for rects with promotion choices under the mouse,
    # returns the chosen promotion piece as a fen char
    def get_promotion_piece(self, screen, queen_rect, rook_rect,
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

    # Draws the choice menu for promotion of a piece
    def promotion_loop(self, screen, color):
        clock = pygame.time.Clock()
        if color:
            q = self.sprites['Q']
            r = self.sprites['R']
            n = self.sprites['N']
            b = self.sprites['B']
        else:
            q = self.sprites['q']
            r = self.sprites['r']
            n = self.sprites['n']
            b = self.sprites['b']
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
                self.get_promotion_piece(screen, queen_rect, rook_rect,
                                         knight_rect, bishop_rect)
                pygame.display.flip()
                if e.type == pygame.MOUSEBUTTONUP:
                    promotion_piece = self.get_promotion_piece(
                        screen, queen_rect, rook_rect,
                        knight_rect, bishop_rect, button_up=True)
                    return promotion_piece
            clock.tick(60)

    def static_eval(self, fen_str, white_maximizing):
        white, black = 0, 0
        for i, char in enumerate(fen_str):
            if char == ' ':
                if white_maximizing:
                    black = - black
                else:
                    white = - white
                return white + black, ''
            elif not char.isalpha():
                continue
            elif char.isupper():
                white += self.value_map[char]
                white += self.position_value_map[char][i]
            else:
                black += self.value_map[char]
                black += self.position_value_map[char][i]

    def minimax(self, depth, alpha, beta, maximizing_player, white_maximizing, best_move=''):
        if depth == 0 or self.board_text.is_game_over():
            return self.static_eval(self.board_text.fen(), white_maximizing)
        elif maximizing_player:
            max_ev = -1000000
            # could be parallelized for the first layer maybe
            for move in self.board_text.legal_moves:
                self.board_text.push(move)
                if self.board_text.is_checkmate() and depth == 3:
                    print('mate')
                    self.board_text.pop()
                    return 100000, str(move)
                ev, new_move = self.minimax(depth - 1, alpha, beta, not maximizing_player, white_maximizing, best_move)
                if self.board_text.is_checkmate():
                    ev += 501
                if self.board_text.is_check():
                    ev += 15
                self.board_text.pop()
                if ev > max_ev:
                    best_move = str(move)
                    max_ev = ev
                alpha = max(alpha, ev)
                if beta <= alpha:
                    break
            return max_ev, best_move
        else:
            min_ev = 1000000
            for move in self.board_text.legal_moves:
                self.board_text.push(move)
                ev, new_move = self.minimax(depth - 1, alpha, beta, not maximizing_player, white_maximizing, best_move)
                if self.board_text.is_checkmate():
                    ev -= 501
                self.board_text.pop()
                if ev < min_ev:
                    best_move = str(move)
                    min_ev = ev
                alpha = min(beta, ev)
                if beta <= alpha:
                    break
            return min_ev, best_move
