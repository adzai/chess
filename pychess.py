#!/bin/python
import chess
import pygame
import board_utils


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((720, 720))
    font = pygame.font.Font('freesansbold.ttf', 40)
    check_mate_text = font.render('Game Over!', True, (255, 0, 0))
    check_mate_text_rect = check_mate_text.get_rect(
        center=screen.get_rect().center)
    board_text = chess.Board()
    king_squares = {'k': [0, 0], 'K': [0, 0]}
    rect_board = board_utils.fen_to_board(board_text.fen(), king_squares)
    board_surf = board_utils.create_board_surf()
    initial_square = board_utils.Square()
    drop_square = board_utils.Square()
    white = True
    while True:
        square_under_mouse = board_utils.get_square_under_mouse(rect_board)
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
                        uci, promotion = board_utils.board_to_uci(
                            initial_square, drop_square)
                        legal = chess.Move.from_uci(uci) in \
                            board_text.legal_moves
                        if legal:
                            if promotion:
                                # add extra uci notation if a player is
                                # promoting and draw the promotion choice menu
                                uci = uci[:-1] + board_utils.promotion_loop(
                                    screen, white)
                            promotion = False
                            board_text.push_uci(uci)
                            rect_board = board_utils.fen_to_board(
                                board_text.fen(), king_squares)
                            white = not white
                        if board_text.is_game_over():
                            board_surf.blit(check_mate_text,
                                            check_mate_text_rect)
                initial_square.can_use = False
                drop_square.can_use = False
            screen.blit(board_surf, board_utils.BOARD_POS)
        board_utils.draw_pieces(screen, rect_board, initial_square)
        board_utils.draw_selector(screen, square_under_mouse)
        drop_square = board_utils.draw_drag(
            screen, rect_board, initial_square, board_text)
        # draw a req square around the king if he is in check
        if board_text.is_check():
            if white:
                board_utils.draw_king_check(
                    screen, rect_board, 'K', king_squares)
            else:
                board_utils.draw_king_check(
                    screen, rect_board, 'k', king_squares)
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
