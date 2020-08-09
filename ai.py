#!/bin/python
import chess
import time


value_map = {
    'R': 50,
    'N': 30,
    'B': 30,
    'Q': 90,
    'K': 900,
    'P': 10,
    'r': +50,
    'n': +30,
    'b': +30,
    'q': +90,
    'k': +900,
    'p': +10,
}

def static_eval(fen_str, white_maximizing):
    white, black = 0, 0
    for char in fen_str:
        if char == ' ':
            if white_maximizing:
                black = - black
            else:
                white = - white
            return white + black, ''
        elif char.isupper():
            try:
                white += value_map[char]
            except KeyError:
                pass
        else:
            try:
                black += value_map[char]
            except KeyError:
                pass

def minimax(board, depth, alpha, beta, maximizing_player, white_maximizing, prev_move, best_move=''):
    if depth == 0 :
        return static_eval(board.fen(), white_maximizing)
    elif maximizing_player:
        max_ev = -1000000
        for move in board.legal_moves:
            board.push_uci(str(move))
            ev, new_move = minimax(board, depth - 1, alpha, beta, not maximizing_player, white_maximizing, prev_move, best_move)
            if board.is_check():
                ev += 10
            board.pop()
            if str(move) != prev_move:
                if ev > max_ev:
                    best_move = str(move)
                    max_ev = ev
            else:
                ev -= 5000
                if ev > max_ev:
                    best_move = str(move)
                    max_ev = ev
            alpha = max(alpha, ev)
            if beta <= alpha:
                break
        return max_ev, best_move
    else:
        min_ev = 1000000
        for move in board.legal_moves:
            board.push_uci(str(move))
            ev, new_move = minimax(board, depth - 1, alpha, beta, not maximizing_player, white_maximizing, prev_move, best_move)
            board.pop()
            if ev < min_ev:
                best_move = str(move)
                min_ev = ev
            alpha = min(beta, ev)
            if beta <= alpha:
                break
        return min_ev, best_move

if __name__ == '__main__':
    board = chess.Board()
    board.legal_moves  
    chess.Move.from_uci("a8a1") in board.legal_moves
    board.push_san("e4")
    board.push_uci("e7e5")
    board.push_san("d4")
    board.push_san("d4")
    board.push_san("c3")
    board.push_san("c3")
    board.push_san("a4")
    board.push_san("b2")
    board.push_san("h4")
    board.push_uci("b2a1q")
    print(board.fen())
    print(board)


# x = minimax(board, 4, -10000, 10000, False)
# print(x)
# board.push_uci(x[1])
# print(board)
# y = minimax(board, 4, -10000, 10000, True)
# print(y)
# board.push_uci(y[1])
# print(board)
# z = minimax(board, 4, -10000, 10000, False)
# print(z)
# board.push_uci(z[1])
# print(board.fen())
# a = minimax(board, 4, -10000, 10000, True)
# print(a)
# board.push_uci(a[1])
# print(board)
# b = minimax(board, 4, -10000, 10000, False)
# print(b)
# board.push_uci(b[1])
# print(board)
# c = minimax(board, 4, -10000, 10000, True)
# print(c)
# board.push_uci(c[1])
# print(board)
# d = minimax(board, 4, -10000, 10000, False)
# print(d)
# board.push_uci(d[1])
# print(board)
# e = minimax(board, 4, -10000, 10000, True)
# print(e)
# board.push_uci(e[1])
# print(board)
# f = minimax(board, 4, -10000, 10000, False)
# print(f)
# board.push_uci(f[1])
# print(board)
    play = True
    white = True
# 0 black, 1 white
    prev_move = ["", "", "", ""]
    i = 0
    while play:
        mv = minimax(board, 3, -10000, 10000, True, white, prev_move[i])
        prev_move[i] = mv[1]
        print(mv[0])
        board.push_uci(mv[1])
        white = not white
        print(board)
        if board.is_game_over():
            play = False
        i += 1
        i %= 4
    print(board.is_checkmate())
    print(board.can_claim_draw())
    print(board)
