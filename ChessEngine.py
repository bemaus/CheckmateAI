import chess

"""
This class is responsible for storing all the information about the current state of a chess game.
"""

class GameState():
    def __init__(self):
        self.logic_board = chess.Board() # Will keep track of all moves to follow chess rules
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.whiteToMove = True
        self.moveLog =[]

    def is_legal(self, move):
        try:
            uci = move.getChessNotation()

            if move.pieceMoved[1] == "p" and (move.endRow == 0 or move.endRow == 7):
                uci += "q"

            logic_move = chess.Move.from_uci(uci)
            return logic_move in self.logic_board.legal_moves

        except ValueError:
            return False
   
    def makeMove(self, move, promotion_choice=None):
        uci = move.getChessNotation()
        if(self.logic_board.turn == self.player):
            if move.pieceMoved[1] == "p" and (move.endRow == 0 or move.endRow == 7): 
                if promotion_choice is None:
                    promotion_choice = "q"
                uci += promotion_choice
        else:
            if move.pieceMoved[1] == "p" and (move.endRow == 0 or move.endRow == 7): 
                uci += "q"
        try:
            logic_move = chess.Move.from_uci(uci)
        except ValueError:
            return False

        if logic_move not in self.logic_board.legal_moves:
            return False

        self.logic_board.push(logic_move)
        self.syncBoardFromLogic()

        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

        return True


    def evaluateBoard(self):
        if self.logic_board.is_checkmate():
            if self.logic_board.turn == chess.WHITE:
                return -9999
            else:
                return 9999

        if self.logic_board.is_stalemate() or self.logic_board.is_insufficient_material():
            return 0

        piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0
        }

        score = 0

        center_squares = [
            chess.D4, chess.E4, chess.D5, chess.E5
        ]

        extended_center_squares = [
            chess.C3, chess.D3, chess.E3, chess.F3,
            chess.C4, chess.D4, chess.E4, chess.F4,
            chess.C5, chess.D5, chess.E5, chess.F5,
            chess.C6, chess.D6, chess.E6, chess.F6
        ]

        for square, piece in self.logic_board.piece_map().items():
            value = piece_values[piece.piece_type]

            # Center occupation bonus
            if square in center_squares:
                value += 0.25
            elif square in extended_center_squares:
                value += 0.10

            # Development bonus for knights and bishops
            if piece.piece_type in [chess.KNIGHT, chess.BISHOP]:
                if piece.color == chess.WHITE and square not in [chess.B1, chess.C1, chess.F1, chess.G1]:
                    value += 0.15
                elif piece.color == chess.BLACK and square not in [chess.B8, chess.C8, chess.F8, chess.G8]:
                    value += 0.15

            # Pawn advancement bonus
            if piece.piece_type == chess.PAWN:
                rank = chess.square_rank(square)

                if piece.color == chess.WHITE:
                    value += rank * 0.03
                else:
                    value += (7 - rank) * 0.03

            if piece.color == chess.WHITE:
                score += value
            else:
                score -= value

        # Mobility bonus
        board_copy = self.logic_board.copy(stack=False)

        board_copy.turn = chess.WHITE
        white_mobility = len(list(board_copy.legal_moves))

        board_copy.turn = chess.BLACK
        black_mobility = len(list(board_copy.legal_moves))

        score += (white_mobility - black_mobility) * 0.03

        # Check bonus
        if self.logic_board.is_check():
            if self.logic_board.turn == chess.BLACK:
                score += 0.40
            else:
                score -= 0.40

        # Castling / king safety bonus
        white_king_square = self.logic_board.king(chess.WHITE)
        black_king_square = self.logic_board.king(chess.BLACK)

        if white_king_square in [chess.G1, chess.C1]:
            score += 0.35

        if black_king_square in [chess.G8, chess.C8]:
            score -= 0.35

        return score

    def forecastEvaluation(self, depth=2):
        """
        Looks ahead a few moves and returns the expected score from White's perspective.
        Positive = White is better.
        Negative = Black is better.
        """
        return self._minimaxForecast(depth, float('-inf'), float('inf'))

    def _minimaxForecast(self, depth, alpha, beta):
        if depth == 0 or self.logic_board.is_game_over():
            return self.evaluateBoard()

        legal_moves = list(self.logic_board.legal_moves)

        if self.logic_board.turn == chess.WHITE:
            best_score = float('-inf')

            for move in legal_moves:
                self.logic_board.push(move)
                score = self._minimaxForecast(depth - 1, alpha, beta)
                self.logic_board.pop()

                best_score = max(best_score, score)
                alpha = max(alpha, best_score)

                if beta <= alpha:
                    break

            return best_score

        else:
            best_score = float('inf')

            for move in legal_moves:
                self.logic_board.push(move)
                score = self._minimaxForecast(depth - 1, alpha, beta)
                self.logic_board.pop()

                best_score = min(best_score, score)
                beta = min(beta, best_score)

                if beta <= alpha:
                    break

            return best_score




    def get_GameState(self):
        # Returns interactive chess board and python-chess logic board
        return self.board, self.logic_board

    def game_over(self):
        # Returns if a game has ended and why and what color won
        reason = ''
        if self.whiteToMove:
            color = "Black"
        else:
            color = "White"
        if self.logic_board.is_checkmate():
            reason = color + " won by Checkmate!"

        elif self.logic_board.is_stalemate():
            reason = "Stalemate"

        elif self.logic_board.is_insufficient_material():
            reason = "Insufficient Material"

        elif self.logic_board.is_seventyfive_moves():
            reason = "Seventyfive Moves"

        elif self.logic_board.is_fivefold_repetition():
            reason = "Fivefold Repetition"

        elif self.logic_board.can_claim_fifty_moves():
            reason = "Claim Fifty Moves"

        elif self.logic_board.can_claim_threefold_repetition():
            reason = "Claim Three Fold Repetition"

        if reason != '':
            return True, reason
        return False

    def syncBoardFromLogic(self):
        self.board = [["--" for _ in range(8)] for _ in range(8)]

        for square, piece in self.logic_board.piece_map().items():
            row = 7 - chess.square_rank(square)
            col = chess.square_file(square)

            color = "w" if piece.color == chess.WHITE else "b"
            piece_type = piece.symbol().upper() if piece.symbol().lower() != "p" else "p"

            self.board[row][col] = color + piece_type


class Move():
    ranksToRows = {
        "1":7, "2":6, "3":5, "4":4, "5":3, "6":2, "7":1, "8":0}
    rowsToRanks = {v:k for k, v in ranksToRows.items()}
    filesToCols= {
        "a": 0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
    colsToFiles = {v:k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]




    def getChessNotation(self):
        #you can add to make this like a real chess notation
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)


    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]





