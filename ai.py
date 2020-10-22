import chess
import chess.polyglot
from values import init_val_map, init_pos_map


class Ai:
    def __init__(self):
        self.depth = 3
        self.best_move = ""
        self.value = 0
        self.board = False
        self.position_value_map = init_pos_map()
        self.value_map = init_val_map()
        self.opening_moves = []

    def init_game(self, fen_str):
        self.board = chess.Board(fen_str)

    def get_move(self, white_maximizing=None, fen_str=None, board=None):
        if board is None:
            if fen_str is None:
                return "Error, no fen provided"
            elif fen_str.find("w") == -1:
                white_maximizing = False
            else:
                white_maximizing = True
            self.init_game(fen_str)
        else:
            self.board = board
        with chess.polyglot.open_reader("eman.bin") as reader:
            self.opening_moves = []
            for entry in reader.find_all(self.board):
                self.opening_moves.append(entry.move)
        if len(self.opening_moves) > 0:
            self.best_move = str(self.opening_moves[0])
            print(self.best_move)
            return -1, self.best_move

        self.minimax(self.board, white_maximizing,
                     self.depth, True, -10000, 10000)
        print(self.best_move)
        return self.value, self.best_move

    def minimax(self, board, white_maximizing, depth, maximizing_player, alpha, beta):
        if depth == 0 or board.is_game_over():
            return self.static_eval(board, board.fen(), white_maximizing)
        elif maximizing_player:
            max_ev = -1000000
            # could be parallelized for the first layer maybe
            for move in board.legal_moves:
                board.push(move)
                if board.is_checkmate() and depth == self.depth:
                    print("mate")
                    board.pop()
                    self.best_move = str(move)
                    self.value = 100000
                    return 100000
                ev = self.minimax(board, white_maximizing,
                                  depth-1, not maximizing_player, alpha, beta)
                if board.is_checkmate():
                    ev += 10000
                elif board.is_check():
                    ev += 15
                board.pop()
                if ev > max_ev:
                    best_move = str(move)
                    max_ev = ev
                if board.can_claim_threefold_repetition() or board.is_stalemate():
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
            for move in board.legal_moves:
                board.push(move)
                ev = self.minimax(board, white_maximizing,
                                  depth-1, not maximizing_player, alpha, beta)
                if board.is_checkmate():
                    ev -= 10000
                board.pop()
                if ev < min_ev:
                    best_move = str(move)
                    min_ev = ev
                if board.can_claim_threefold_repetition() or board.is_stalemate():
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
