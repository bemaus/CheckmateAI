import random
import chess
import ChessEngine

PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0
}

MATE_VALUE = 100000
MATE_THRESHOLD = 90000

def evaluate_board(board):
    """Evaluate from the perspective of the side to move."""
    if board.is_checkmate():
        # Side to move has no legal moves and is in check → they lost
        return -MATE_VALUE

    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    score = 0
    turn = board.turn  # True = white, False = black

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            value = PIECE_VALUES[piece.piece_type]
            if piece.color == turn:
                score += value
            else:
                score -= value

    return score

def negate_score(score):
    """Negate score, adjusting mate distances."""
    # Detect mate scores
    if abs(score) > MATE_THRESHOLD:
        # Example: score = 100000 - n
        # Convert to mate distance
        distance = MATE_VALUE - abs(score)

        # Negate and increment distance
        new_distance = distance + 1

        if score > 0:
            return -(MATE_VALUE - new_distance)
        else:
            return +(MATE_VALUE - new_distance)

    # Normal score
    return -score


def negamax(logic_board, depth, alpha, beta):
    """
    Core Negamax functionality with Alpha-Beta pruning.
    """
    if depth == 0 or logic_board.is_game_over():
        return evaluate_board(logic_board)

    max_eval = float('-inf')

    for move in logic_board.legal_moves:
        logic_board.push(move)  # Make move on Logic Board
        
        # Recursive call using negative bounds for score maximization 
        # max(a,b) = -min(-a,-b)
        evaluation = negate_score(negamax(logic_board, depth - 1, -beta, -alpha))
        logic_board.pop()   # Undo move

        if evaluation > max_eval:
            max_eval = evaluation


        alpha = max(alpha, evaluation)
        if alpha >= beta:
            break

    return max_eval



def get_best_move(gs, depth= 3):
    """
    Root function to trigger AI search. Returns a ChessEngine.Move object
    """
    best_logic_move = None
    alpha = float('-inf')
    beta = float('inf')

    legal_moves = list(gs.logic_board.legal_moves)

    # Shuffling prevents AI from repeating openings every game
    random.shuffle(legal_moves)

    for move in legal_moves:
        gs.logic_board.push(move)
        evaluation = -negamax(gs.logic_board, depth - 1, -beta, -alpha)
        gs.logic_board.pop()

        if evaluation > alpha:
            alpha = evaluation
            best_logic_move = move


        print("Evaluation: " + str(evaluation) + "  Move: " + str(move))
        alpha = max(alpha, evaluation)

    # Translate python-chess Move object back to custom ChessEngine.Move
    if best_logic_move:
        uci = best_logic_move.uci()     # Format: e.g., "e2e4"

        start_sq = (ChessEngine.Move.ranksToRows[uci[1]], ChessEngine.Move.filesToCols[uci[0]])
        end_sq = (ChessEngine.Move.ranksToRows[uci[3]], ChessEngine.Move.filesToCols[uci[2]])

        return ChessEngine.Move(start_sq, end_sq, gs.board)
    
    return None
