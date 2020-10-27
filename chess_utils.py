#!/bin/python
import pygame
import chess
import time
from collections import defaultdict
from ai import Ai


class Square:
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

class Game:
    def game_init(self, screen_width, screen_height):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 40)
        self.check_mate_text = self.font.render("Game Over!",
                                                True, (255, 0, 0))
        self.check_mate_text_rect = self.check_mate_text.get_rect(
            center=self.screen.get_rect().center
        )
        # default settings
        self.screen_width = 720
        self.screen_height = 820
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.grey = (192, 192, 192)
        self.light_grey = (211, 211, 211)
        self.beige = (245, 245, 220)
        self.bright_red = (255, 0, 0)
        self.bright_green = (0, 255, 0)
        self.block_color = (53, 115, 255)
        self.game_display = pygame.display.set_mode(
            (self.screen_width, self.screen_height)
        )
        self.board = Board(self.screen_width, (0, 0))
        self.board = self.board.board_init()
        self.move_history = []
        self.redo_buffer = []
        self.color_playing = None
        self.last_square = None
        self.ai_played_square = None
        self.captured_white = []
        self.captured_black = []

    def game_loop(self, board):
        pygame.display.set_caption("PyChess")
        self.game_intro()

    def chess_game_loop(self, ai=None, color=None):
        initial_square = Square()
        drop_square = Square()
        # False for ai with white pieces
        white = color
        player_turn = color
        self.color_playing = True
        white_maximizing = not player_turn
        value = 0
        square_under_mouse = Square(None, None, None, False)
        ai_player = Ai()
        ######## TESTING FONT UNDER BOARD ########
        ######## TESTING FONT UNDER BOARD ########
        while True:
            if ai and (not player_turn and not
                       self.board.board_text.is_game_over()):
                value, mv = ai_player.get_move(
                    white_maximizing=white_maximizing, board=self.board.board_text)
                print("Val:", value)
                print("Move:", mv)
                self.ai_played_square = mv[2:4]
                self.board.board_text.push_uci(mv)
                try:
                    self.board.current_fen = self.board.board_text.fen()
                except:
                    print("game over")
                self.redo_buffer = []
                self.move_history.append(mv)
                player_turn = not player_turn
                self.color_playing = not self.color_playing
                if self.board.board_text.is_game_over():
                    self.board.board_surf.blit(
                        self.check_mate_text, self.check_mate_text_rect
                    )
                self.board.rect_board = self.board.fen_to_board()
            else:
                square_under_mouse = self.board.get_square_under_mouse()
                events = pygame.event.get()
                for e in events:
                    if e.type == pygame.QUIT:
                        self.game_init(self.screen_width, self.screen_height)
                        self.game_intro()
                    if e.type == pygame.MOUSEBUTTONDOWN:
                        if square_under_mouse.can_use:
                            initial_square.set_square(
                                square_under_mouse.fen_char,
                                square_under_mouse.x,
                                square_under_mouse.y,
                            )
                    if e.type == pygame.MOUSEBUTTONUP:
                        if drop_square.can_use:
                            if initial_square != drop_square:
                                uci, promotion = self.board.board_to_uci(
                                    initial_square, drop_square
                                )
                                legal = (
                                    chess.Move.from_uci(uci)
                                    in self.board.board_text.legal_moves
                                )
                                if legal:
                                    self.last_square = drop_square
                                    if promotion:
                                        # add extra uci notation if a player is
                                        # promoting and draw the promotion
                                        # choice menu
                                        # TODO improve knowing color of current turn player
                                        if not white:
                                            uci = uci[:-1] + self.board.promotion_loop(
                                                self.screen, not player_turn
                                            )
                                        else:
                                            uci = uci[:-1] + self.board.promotion_loop(
                                                self.screen, player_turn
                                            )

                                    promotion = False
                                    self.board.board_text.push_uci(uci)
                                    try:
                                        self.board.current_fen = self.board.board_text.fen()
                                    except:
                                        print("game over")
                                    self.last_square = uci[2:4]
                                    self.redo_buffer = []
                                    self.move_history.append(uci)
                                    self.board.rect_board = self.board.fen_to_board()
                                    player_turn = not player_turn
                                    self.color_playing = not self.color_playing
                                if self.board.board_text.is_game_over():
                                    self.board.board_surf.blit(
                                        self.check_mate_text, self.check_mate_text_rect
                                    )
                        initial_square.can_use = False
                        drop_square.can_use = False
            self.move_displayer(self.color_playing)
            self.button(
                "Undo",
                10,
                740,
                self.screen_width // 8 + 30,
                720//8,
                self.grey,
                self.bright_green,
                action=self.undo_move,
                board=self.board,
                ai=ai
            )
            self.button(
                "Redo",
                150,
                740,
                self.screen_width // 8 + 30,
                720//8,
                self.grey,
                self.bright_green,
                action=self.redo_move,
                board=self.board,
                ai=ai
            )
            self.button(
                "Flip",
                290,
                740,
                self.screen_width // 8 + 30,
                720//8,
                self.grey,
                self.bright_green,
                action=self.flip_board,
                board=self.board
            )
            self.screen.blit(self.board.board_surf, self.board.board_pos)
            if self.last_square and not player_turn:
                self.board.draw_last_piece(self.screen, self.last_square)
            if ai:
                if self.ai_played_square and player_turn:
                    self.board.draw_last_piece(
                        self.screen, self.ai_played_square)
            elif self.last_square and player_turn:
                self.board.draw_last_piece(self.screen, self.last_square)

            self.board.draw_pieces(self.screen)
            self.board.draw_selector(self.screen, square_under_mouse)
            drop_square = self.board.draw_drag(self.screen, initial_square)
            # draw a req square around the king if he is in check
            if self.board.board_text.is_check():
                side = player_turn if not white else not player_turn
                if side:
                    self.board.draw_king_check(self.screen, "k")
                else:
                    self.board.draw_king_check(self.screen, "K")
            pygame.display.flip()
            self.clock.tick(60)

    def flip_board(self, board=None, **kwargs):
        board.flip = not board.flip
        self.board.board_surf = self.board.create_board_surf()
        self.board.rect_board = self.board.fen_to_board()

    def move_displayer(self, player_turn):
        color = "white" if player_turn else "black"
        font = pygame.font.SysFont('arial', 30)
        textsurface = font.render(f"Move: {color}", True, (0, 0, 0))
        rect = pygame.Rect(500, 765, 720//8, 720//8)
        text_display = pygame.display.set_mode((1000, 840))
        text_display.fill(self.light_grey)
        text_display.blit(textsurface, rect)

    def redo_move(self, board=None, ai=None):
        try:
            num = 2 if ai else 1
            new_history = self.move_history + self.redo_buffer[:num]
            new_redo_buffer = self.redo_buffer[num:]
            self.board = self.board.board_init(history=new_history)
            self.board.draw_pieces(self.screen)
            self.move_history = new_history
            if ai:
                self.ai_played_square = self.move_history[-1][2:4]
            else:
                self.last_square = self.move_history[-1][2:4]
            self.redo_buffer = new_redo_buffer
        except Exception as e:
            print(e)

    def undo_move(self, board, ai=None):
        try:
            # > 2 so that you can't take ai's turn
            # TODO Find something better
            if ai and len(self.move_history) > 2:
                board.board_text.pop()
                self.redo_buffer = [
                    (self.move_history.pop())] + self.redo_buffer
                board.board_text.pop()
                self.redo_buffer = [
                    (self.move_history.pop())] + self.redo_buffer
                self.ai_played_square = self.move_history[-1][2:4]
            elif not ai:
                board.board_text.pop()
                self.redo_buffer = [
                    (self.move_history.pop())] + self.redo_buffer
                self.last_square = self.move_history[-1][2:4]
                self.color_playing = not self.color_playing
        except Exception as e:
            print(e)
        self.board = self.board.board_init(history=self.move_history)
        self.board.draw_pieces(self.screen)


    def text_objects(self, text, font):
        text_surface = font.render(text, True, self.black)
        return text_surface, text_surface.get_rect()

    def select_color(self, ai=None, color=None, action=None):
        time.sleep(0.1)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            top_gap = self.screen_height // 3
            bottom_gap = self.screen_height // 6
            x = self.screen_width // 4
            rect_total_height = self.screen_height - (top_gap + bottom_gap)
            rect_height = rect_total_height // 3
            gap = rect_height // 6
            rect_height -= gap
            y = top_gap
            rect_height = 50
            large_text = pygame.font.SysFont("comicsansms", 70)
            text_surf, text_rect = self.text_objects(
                "Select your color", large_text)
            text_rect.center = ((self.screen_width // 2), (top_gap // 2))
            self.game_display.fill(self.beige)
            self.game_display.blit(text_surf, text_rect)
            self.button(
                "White",
                x,
                y,
                self.screen_width // 2,
                rect_height,
                self.grey,
                self.bright_green,
                self.chess_game_loop,
                ai=ai,
                color=True,
            )
            y += 100
            self.button(
                "Black",
                x,
                y,
                self.screen_width // 2,
                rect_height,
                self.grey,
                self.bright_green,
                self.chess_game_loop,
                ai=ai,
                color=False,
            )
            y += 100
            self.button(
                "Back to menu",
                x,
                y,
                self.screen_width // 2,
                rect_height,
                self.grey,
                self.bright_green,
                self.game_intro,
            )
            pygame.display.update()
            self.clock.tick(15)

    def button(self, msg, x, y, w, h, ic, ac, action=None, ai=None, color=None, board=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(self.game_display, ac, (x, y, w, h))

            if click[0] == 1 and action != None:
                time.sleep(0.1)
                if board:
                    action(board=board, ai=ai)
                else:
                    action(ai=ai, color=color)
        else:
            pygame.draw.rect(self.game_display, ic, (x, y, w, h))

        small_text = pygame.font.SysFont("comicsansms", 50)
        text_surf, textRect = self.text_objects(msg, small_text)
        textRect.center = ((x + (w // 2)), (y + (h // 2)))
        self.game_display.blit(text_surf, textRect)

    def game_intro(self, **kwargs):
        intro = True
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            # Calculate menu dimensions
            top_gap = self.screen_height // 4
            bottom_gap = self.screen_height // 8
            x = self.screen_width // 4
            rect_total_height = self.screen_height - (top_gap + bottom_gap)
            rect_height = rect_total_height // 3
            gap = rect_height // 3
            rect_height -= gap
            y = top_gap

            self.game_display.fill(self.beige)
            large_text = pygame.font.SysFont("comicsansms", 90)
            text_surf, text_rect = self.text_objects("PyChess", large_text)
            text_rect.center = ((self.screen_width // 2), (top_gap // 2))
            self.game_display.blit(text_surf, text_rect)

            self.button(
                "Player vs Player",
                x,
                y,
                self.screen_width // 2,
                rect_height,
                self.grey,
                self.bright_green,
                self.chess_game_loop,
                ai=False,
                color=True,
            )
            y += gap + rect_height
            self.button(
                "Player vs Ai",
                x,
                y,
                self.screen_width // 2,
                rect_height,
                self.grey,
                self.bright_green,
                self.select_color,
                ai=True,
            )
            y += gap + rect_height
            self.button(
                "Exit",
                x,
                y,
                self.screen_width // 2,
                rect_height,
                self.grey,
                self.bright_red,
                self.quitgame,
            )

            pygame.display.update()
            self.clock.tick(15)

    def quitgame(self, **kwargs):
        pygame.quit()
        quit()


class Board:
    def __init__(self, surface, board_pos):
        self.surface = surface
        self.king_squares = {"k": [0, 0], "K": [0, 0]}
        self.tilesize = surface / 8
        self.board_pos = board_pos
        self.flip = False
        self.current_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        self.sprites = {
            "P": pygame.image.load("sprites/whitePawn.png"),
            "K": pygame.image.load("sprites/whiteKing.png"),
            "N": pygame.image.load("sprites/whiteKnight.png"),
            "B": pygame.image.load("sprites/whiteBishop.png"),
            "Q": pygame.image.load("sprites/whiteQueen.png"),
            "R": pygame.image.load("sprites/whiteRook.png"),
            "p": pygame.image.load("sprites/blackPawn.png"),
            "k": pygame.image.load("sprites/blackKing.png"),
            "n": pygame.image.load("sprites/blackKnight.png"),
            "b": pygame.image.load("sprites/blackBishop.png"),
            "q": pygame.image.load("sprites/blackQueen.png"),
            "r": pygame.image.load("sprites/blackRook.png"),
        }

    def board_init(self, fen_str=None, history=False):
        if fen_str:
            self.board_text = chess.Board(fen_str)
        else:
            self.board_text = chess.Board()
        if history:
            self.restore_board(history)
        self.rect_board = self.fen_to_board()
        self.board_surf = self.create_board_surf()
        return self

    def restore_board(self, history):
        for move in history:
            self.board_text.push_uci(move)
            try:
                self.board.current_fen = self.board.board_text.fen()
            except:
                ("game over")

    def get_number_of_captures(self):
        # TODO Fix promotions
        d1 = defaultdict(int)
        d2 = defaultdict(int)
        orig_fen_str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
        for c in self.current_fen.split(" ")[0]:
            if c.isalpha():
                d1[c] += 1
        for c in orig_fen_str:
            # Init with 0 if piece was taken out of fen completely
            d1[c]
            if c.isalpha():
                d2[c] += 1
        diff = {k: d2[k] - d1[k] for k in d1 if k in d2 and d1[k] != d2[k]}
        captures = []
        for k in diff:
            for num in range(diff[k]):
                if k.islower():
                    color = "b"
                else:
                    color = "w"
                captures.append((color, self.sprites[k]))
        return captures


    def make_pygame_rect(self, x, y, offset=0):
        return pygame.Rect(
            x * self.tilesize + offset,
            y * self.tilesize + offset,
            self.tilesize,
            self.tilesize,
        )

    # Populates the board matrix with fen notation
    def fen_to_board(self):
        fen_str = self.board_text.fen().split(" ")[0]
        fen_str = fen_str[::-1] if self.flip else fen_str
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
                if fen_char in "kK":
                    self.king_squares[fen_char] = [x, y]
                i += 1
        return board

    def create_board_surf(self):
        board_surf = pygame.Surface((self.tilesize * 8, self.tilesize * 8))
        dark = False
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        letters = letters[::-1] if self.flip else letters
        numbers = list(map(str, (reversed(range(1, 9)))))
        numbers = numbers[::-1] if self.flip else numbers
        font_size = 20
        font = pygame.font.SysFont('arial', font_size)
        for y in range(8):
            for x in range(8):
                rect = pygame.Rect(
                    x * self.tilesize, y * self.tilesize, self.tilesize, self.tilesize
                )
                pygame.draw.rect(
                    board_surf, pygame.Color(
                        "darkgrey" if dark else "white"), rect
                )
                if x == 7:
                    textsurface = font.render(numbers[0], True, (0, 0, 0))
                    numbers.pop(0)
                    numbers_rect = pygame.Rect(
                        x * self.tilesize + self.tilesize - font_size, y * self.tilesize, self.tilesize, self.tilesize)
                    board_surf.blit(textsurface, numbers_rect)
                if y == 7:
                    textsurface = font.render(letters[0], True, (0, 0, 0))
                    letters.pop(0)
                    letters_padding = 5
                    text_rect = pygame.Rect(
                        x * self.tilesize, y * self.tilesize + self.tilesize - font_size - letters_padding, self.tilesize, self.tilesize)
                    board_surf.blit(textsurface, text_rect)

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
            rect = self.make_pygame_rect(
                self.board_pos[0] + piece.x, self.board_pos[1] + piece.y
            )
            pygame.draw.rect(screen, (0, 0, 255, 50), rect, 2)

    # Takes x and y coordinates from the board matrix
    # and transforms them into the uci notation
    def board_to_uci(self, initial_square, drop_square):
        letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
        nums1 = reversed(range(0, 8)) if self.flip else range(0, 8)
        column_to_letter = {k: v for k, v in zip(nums1, letters)}
        nums2 = reversed(range(0, 9)) if self.flip else range(1, 9)
        row_convert = {k: v for k, v in zip(reversed(range(0, 8)), nums2)}
        lt1_pos = str(column_to_letter[initial_square.x])
        row1_pos = str(row_convert[initial_square.y])
        lt2_pos = str(column_to_letter[drop_square.x])
        row2_pos = str(row_convert[drop_square.y])
        uci = lt1_pos + row1_pos + lt2_pos + row2_pos
        promotion = False
        if uci[:2] == uci[2:]:
            uci = "0000"
        elif initial_square.fen_char in "pP" and (uci[-1] == "8" or uci[-1] == "1"):
            # placeholder promotion for checking legality of the move
            uci += "q"
            promotion = True
        return uci, promotion

    # Draws a red square when a king is in check
    def draw_king_check(self, screen, piece):
        x, y = self.king_squares[piece]
        rect = self.make_pygame_rect(
            self.board_pos[0] + y, self.board_pos[1] + x)
        pygame.draw.rect(screen, (255, 0, 0, 50), rect, 2)

    def draw_last_piece(self, screen, square):
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        nums1 = reversed(range(0, 8)) if self.flip else range(0, 8)
        letter_to_column = {k: v for k, v in zip(letters, nums1)}
        nums2 = reversed(range(0, 9)) if self.flip else range(1, 9)
        row_convert = {k: v for k, v in zip(nums2, reversed(range(0, 8)))}
        x = letter_to_column[square[0]]
        y = row_convert[int(square[1])]
        rect = self.make_pygame_rect(
            self.board_pos[0] + x, self.board_pos[1] + y)
        pygame.draw.rect(screen, (0, 0, 0, 50), rect, 2)

    def draw_pieces(self, screen):
        # TODO Refactor capture drawing
        font = pygame.font.SysFont('arial', 30)
        textsurface_black = font.render(f"Black's captured", True, (0, 0, 0))
        textsurface_white = font.render(f"White's captured", True, (0, 0, 0))
        rect_black = pygame.Rect(730, 50, 720//8, 720//8)
        rect_white = pygame.Rect(730, 450, 720//8, 720//8)
        # text_display = pygame.display.set_mode((1000, 840))
        # text_display.fill(self.light_grey)
        screen.blit(textsurface_black, rect_black)
        screen.blit(textsurface_white, rect_white)
        captures = self.get_number_of_captures()
        capture_x_b = 730
        capture_y_b = 100
        capture_x_w = 730
        capture_y_w = 500
        for capture in captures:
            color, sprite = capture
            if color == "b":
                screen.blit(sprite, (capture_x_b, capture_y_b))
                capture_x_b += 50
                if capture_x_b >= 900:
                    capture_x_b = 730
                    capture_y_b += 50 
            else:
                screen.blit(sprite, (capture_x_w, capture_y_w))
                capture_x_w += 50
                if capture_x_w >= 900:
                    capture_x_w = 730
                    capture_y_w += 50 

        for y in range(8):
            for x in range(8):
                piece = self.rect_board[y][x]
                if piece:
                    if piece.isalpha():
                        s1 = self.sprites[piece]
                        pos = self.make_pygame_rect(
                            self.board_pos[0] + x, self.board_pos[1] + y, offset=1
                        )
                        screen.blit(s1, s1.get_rect(center=pos.center))

    # Draws dragged piece and highlighting legal moves with green
    # square selectors, illegal with red
    def draw_drag(self, screen, initial_square):
        if initial_square.can_use:
            square_under_mouse = self.get_square_under_mouse()
            if square_under_mouse.can_use:
                uci, _ = self.board_to_uci(initial_square, square_under_mouse)
                rect = self.make_pygame_rect(
                    self.board_pos[0] + square_under_mouse.x,
                    self.board_pos[1] + square_under_mouse.y,
                )
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
    def get_promotion_piece(
        self, screen, queen_rect, rook_rect, knight_rect, bishop_rect, button_up=False
    ):
        y = range(250, 410)
        queen_x = range(16, 177)
        rook_x = range(192, 353)
        knight_x = range(368, 529)
        bishop_x = range(544, 705)
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        if mouse_pos[1] in y:
            if mouse_pos[0] in queen_x:
                if button_up:
                    return "q"
                pygame.draw.rect(screen, (0, 0, 0, 50), queen_rect, 1)
            if mouse_pos[0] in rook_x:
                if button_up:
                    return "r"
                pygame.draw.rect(screen, (0, 0, 0, 50), rook_rect, 1)
            if mouse_pos[0] in knight_x:
                if button_up:
                    return "n"
                pygame.draw.rect(screen, (0, 0, 0, 50), knight_rect, 1)
            if mouse_pos[0] in bishop_x:
                if button_up:
                    return "b"
                pygame.draw.rect(screen, (0, 0, 0, 255), bishop_rect, 1)

    # Draws the choice menu for promotion of a piece
    def promotion_loop(self, screen, color):
        clock = pygame.time.Clock()
        if color:
            q = self.sprites["Q"]
            r = self.sprites["R"]
            n = self.sprites["N"]
            b = self.sprites["B"]
        else:
            q = self.sprites["q"]
            r = self.sprites["r"]
            n = self.sprites["n"]
            b = self.sprites["b"]
        while True:
            left = 16
            top = 250
            width = 160
            height = 160
            filled = 0
            pygame.draw.rect(
                screen, [211, 211, 211], [left, top, width, height], filled
            )
            queen_rect = pygame.Rect(left, top, width, height)
            screen.blit(q, q.get_rect(center=queen_rect.center))
            left += width + 16
            pygame.draw.rect(
                screen, [211, 211, 211], [left, top, width, height], filled
            )
            rook_rect = pygame.Rect(left, top, width, height)
            screen.blit(r, r.get_rect(center=rook_rect.center))
            left += width + 16
            knight_rect = pygame.Rect(left, top, width, height)
            pygame.draw.rect(
                screen, [211, 211, 211], [left, top, width, height], filled
            )
            screen.blit(n, n.get_rect(center=knight_rect.center))
            left += width + 16
            pygame.draw.rect(
                screen, [211, 211, 211], [left, top, width, height], filled
            )
            bishop_rect = pygame.Rect(left, top, width, height)
            screen.blit(b, b.get_rect(center=bishop_rect.center))
            events = pygame.event.get()
            for e in events:
                self.get_promotion_piece(
                    screen, queen_rect, rook_rect, knight_rect, bishop_rect
                )
                pygame.display.flip()
                if e.type == pygame.MOUSEBUTTONUP:
                    promotion_piece = self.get_promotion_piece(
                        screen,
                        queen_rect,
                        rook_rect,
                        knight_rect,
                        bishop_rect,
                        button_up=True,
                    )
                    return promotion_piece
            clock.tick(60)
