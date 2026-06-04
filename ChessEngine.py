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
    # Cannot move an empty square
        if move.pieceMoved == "--":
            return False

        # White can only move white pieces
        if self.whiteToMove and move.pieceMoved[0] != "w":
            return False

        # Black can only move black pieces
        if not self.whiteToMove and move.pieceMoved[0] != "b":
            return False

        # Cannot capture your own piece
        if move.pieceCaptured != "--" and move.pieceCaptured[0] == move.pieceMoved[0]:
            return False

        return True



    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved

        logic_move = chess.Move.from_uci(move.getChessNotation()) # Updates Logic Board to track valid moves
        self.logic_board.push(logic_move)

        self.moveLog.append(move) #log the move to be able to undo it later.
        self.whiteToMove = not self.whiteToMove #swap players


    def move_leaves_king_in_check(self, move):
        original_start = self.board[move.startRow][move.startCol]
        original_end = self.board[move.endRow][move.endCol]

        # make temp move
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved

        king_color = move.pieceMoved[0]
        king_row, king_col = self.find_king(king_color)

        in_check = self.square_under_attack(king_row, king_col, king_color)

        # Undo temp move
        self.board[move.startRow][move.startCol] = original_start
        self.board[move.endRow][move.endCol] = original_end

        return in_check
    

    def find_king(self, color):
        king = color + "K"
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == king:
                    return r, c
        return None
    
    def square_under_attack(self, row, col, king_color):
        opponent_color = "b" if king_color == "w" else "w"

        # Check if any opponent piece can attack this square
        # This can reuse your teammates' piece-move logic.
        return False

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





