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
        if move.pieceMoved == "--":
            return False

        if self.whiteToMove and move.pieceMoved[0] != "w":
            return False

        if not self.whiteToMove and move.pieceMoved[0] != "b":
            return False

        if move.pieceCaptured != "--" and move.pieceCaptured[0] == move.pieceMoved[0]:
            return False
        
        # Pawn movement logic
        if move.pieceMoved[1] == "p":
            return self.is_valid_pawn_move(move)

        piece_type = move.pieceMoved[1]

        if piece_type == "K" and not self.is_valid_king_move(move):
            return False

        if piece_type == "Q" and not self.is_valid_queen_move(move):
            return False

        if self.move_leaves_king_in_check(move):
            return False

        return True
    

    def is_valid_pawn_move(self, move):
        piece_color = move.pieceMoved[0]

        row_change = move.endRow - move.startRow
        col_change = move.endCol - move.startCol

        # White pawns move up the board, row goes down
        if piece_color == "w":
            direction = -1
            start_row = 6

        # Black pawns move down the board, row goes up
        else:
            direction = 1
            start_row = 1

        # Move forward 1 square
        if col_change == 0 and row_change == direction:
            if move.pieceCaptured == "--":
                return True
            
        
        # Move forward 2 squares from the starting row
        if col_change == 0 and row_change == 2 * direction:
            if move.startRow == start_row:
                middle_row = move.startRow + direction
                if self.board[middle_row][move.startCol] == "--" and move.pieceCaptured == "--":
                    return True
        
        # Capture diagonally
        if abs(col_change) -- 1 and row_change == direction:
            if move.pieceCaptured != "--":
                return True
        
        return False

    def is_valid_king_move(self, move):
        row_change = abs(move.endRow - move.startRow)
        col_change = abs(move.endCol - move.startCol)

        # Normal king move
        if row_change <= 1 and col_change <= 1:
            return True

        # Castling move
        if row_change == 0 and col_change == 2:
            return self.is_valid_castle_move(move)

        return False

    def is_valid_queen_move(self, move):
        row_change = abs(move.endRow - move.startRow)
        col_change = abs(move.endCol - move.startCol)

        # Queen moves like a rook: same row or same column
        if move.startRow == move.endRow or move.startCol == move.endCol:
            return self.path_is_clear(move)
    
        # Queen moves like a bishop: diagonal
        if row_change == col_change:
            return self.path_is_clear(move)
    
        return False

    def is_valid_castle_move(self, move):
        # King must move two columns and stay on same row
        if move.pieceMoved[1] != "K":
            return False
    
        if move.startRow != move.endRow:
            return False
    
        if abs(move.endCol - move.startCol) != 2:
            return False
    
        # King cannot currently be in check
        if self.square_under_attack(move.startRow, move.startCol, move.pieceMoved[0]):
            return False
    
        # Determine direction
        if move.endCol > move.startCol:
            # Kingside castle
            rook_col = 7
            step = 1
        else:
            # Queenside castle
            rook_col = 0
            step = -1
    
        # Rook must be in the corner
        rook = self.board[move.startRow][rook_col]
        if rook != move.pieceMoved[0] + "R":
            return False

        # Squares between king and rook must be empty
        current_col = move.startCol + step
        while current_col != rook_col:
            if self.board[move.startRow][current_col] != "--":
                return False
            current_col += step
    
        # King cannot move through check
        current_col = move.startCol
        for i in range(2):
            current_col += step
            if self.square_under_attack(move.startRow, current_col, move.pieceMoved[0]):
                return False
    
        return True

    def path_is_clear(self, move):
        row_direction = 0
        col_direction = 0

        if move.endRow > move.startRow:
            row_direction = 1
        elif move.endRow < move.startRow:
            row_direction = -1

        if move.endCol > move.startCol:
            col_direction = 1
        elif move.endCol < move.startCol:
            col_direction = -1

        current_row = move.startRow + row_direction
        current_col = move.startCol + col_direction

        while current_row != move.endRow or current_col != move.endCol:
            if self.board[current_row][current_col] != "--":
                return False

            current_row += row_direction
            current_col += col_direction

        return True

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved

        logic_move = chess.Move.from_uci(move.getChessNotation()) # Updates Logic Board to track valid moves
        self.logic_board.push(logic_move)

        self.pawn_promotion(move)

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


    def pawn_promotion(self, move):
        logic_move = chess.Move.from_uci(move.getChessNotation())
        if move.pieceMoved == "wp" or move.pieceMoved == "bp":
            from_sqr = logic_move.uci()[:2]
            to_sqr = logic_move.uci()[2:]
            if to_sqr[1] == "1" or to_sqr[1] == "8":
                square1= chess.parse_square(from_sqr)
                square2 = chess.parse_square(to_sqr)
                piece = input("Enter Piece (Q,R,K,B): ")
                x = True
                bw = ""
                if self.whiteToMove:
                    bw = "w"
                else:
                    bw = "b"
                while x:
                    if piece == "Q":
                        chess.Move(square1, square2, promotion=5)
                        x = False
                        self.board[move.endRow][move.endCol] = bw+ "Q"
                    elif piece == "R":
                        chess.Move(square1, square2, promotion=4)
                        x = False
                        move.pieceMoved = bw+ "R"
                        self.board[move.endRow][move.endCol] = bw + "R"
                    elif piece == "K":
                        chess.Move(square1, square2, promotion=2)
                        x = False
                        move.pieceMoved = bw+ "K"
                        self.board[move.endRow][move.endCol] = bw + "K"
                    elif piece == "B":
                        chess.Move(square1, square2, promotion= 3)
                        x = False
                        move.pieceMoved = bw+ "B"
                        self.board[move.endRow][move.endCol] = bw + "B"
                    else:
                        print("Invalid Piece")




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





