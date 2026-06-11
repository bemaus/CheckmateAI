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





