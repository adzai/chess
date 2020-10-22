import chess
from values import init_val_map, init_pos_map

class Ai:
    def __init__(self):
        self.depth = 3
        self.best_move = ""
        self.value = 0
        self.board = False
        self.position_value_map = init_pos_map()
        self.value_map = init_val_map()

    def init_game(self, fen_str):
       self.board = chess.Board(fen_str) 

    def get_move(self, white_maximizing, board=False):
        if not board:
            board = self.board
        self.minimax(board, white_maximizing, self.depth, True, -10000, 10000)
        return self.value, self.best_move

    def minimax(self, board, white_maximizing, depth, maximizing_player, alpha, beta):
        if depth == 0 or board.board_text.is_game_over():
            return self.static_eval(board, board.board_text.fen(), white_maximizing)
        elif maximizing_player:
            max_ev = -1000000
            # could be parallelized for the first layer maybe
            for move in board.board_text.legal_moves:
                board.board_text.push(move)
                if board.board_text.is_checkmate() and depth == self.depth:
                    print("mate")
                    board.board_text.pop()
                    self.best_move = str(move)
                    self.value = 100000
                    return 100000
                ev = self.minimax(board, white_maximizing, depth-1, not maximizing_player, alpha, beta)
                if board.board_text.is_checkmate():
                    ev += 10000
                elif board.board_text.is_check():
                    ev += 15
                board.board_text.pop()
                if ev > max_ev:
                    best_move = str(move)
                    max_ev = ev
                if board.board_text.can_claim_threefold_repetition() or board.board_text.is_stalemate():
                    if max_ev < -500:
                        max_ev += 500
                    else:
                        max_ev -= 10000
                alpha = max(alpha, max_ev)
                if alpha >= beta:
                    break
            if depth == self.depth:
                self.best_move = best_move
                self.value = max_ev
            return max_ev
        else:
            min_ev = 1000000
            for move in board.board_text.legal_moves:
                board.board_text.push(move)
                ev = self.minimax(board, white_maximizing, depth-1, not maximizing_player, alpha, beta)
                if board.board_text.is_checkmate():
                    ev -= 10000
                board.board_text.pop()
                if ev < min_ev:
                    best_move = str(move)
                    min_ev = ev
                if board.board_text.can_claim_threefold_repetition() or board.board_text.is_stalemate():
                    if min_ev > 500:
                        min_ev -= 5000
                    else:
                        min_ev += 1000
                beta = min(beta, min_ev)
                if beta <= alpha:
                    break
            return min_ev

    def static_eval(self, board, fen_str, white_maximizing):
        white, black = 0, 0
        for i, char in enumerate(fen_str):
            if char == " ":
                if white_maximizing:
                    black = -black
                else:
                    white = -white
                return white + black
            elif not char.isalpha():
                continue
            elif char.isupper():
                white += self.value_map[char]
                white += self.position_value_map[char][i]
            else:
                black += self.value_map[char]
                black += self.position_value_map[char][i]
