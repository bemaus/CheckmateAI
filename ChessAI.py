import random
import chess
import ChessEngine
import random

PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 200
}

def evaluate_board(logic_board):
    """
    Evaluates the board from the perspective of the player whose turn it is to move. 
    Positive score is good for the current player, negative is bad. 
    """
    if logic_board.is_checkmate():
        return -99999   # Current player has lost

    if logic_board.is_stalemate() or logic_board.is_insufficient_material():
        return 0

    score = 0
    current_turn = logic_board.turn     # True for white, False for black

    for square in chess.SQUARES:
        piece = logic_board.piece_at(square)
        if piece is not None:
            value = PIECE_VALUES[piece.piece_type]
            if piece.color == current_turn:
                score += value
            else:
                score -= value
    return score

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
        evaluation = -negamax(logic_board, depth - 1, -beta, -alpha)
        
        logic_board.pop()   # Undo move

        max_eval = max(max_eval, evaluation)
        alpha = max(alpha, evaluation)
        if alpha >= beta:
            break   # Beta cutoff
    
    return max_eval


def get_best_move(gs, depth):
    """
    Root function to trigger AI search. Returns a ChessEngine.Move object
    """
    best_logic_move = None
    max_eval = float('-inf')
    alpha = float('-inf')
    beta = float('-inf')

    legal_moves = list(gs.logic_board.legal_moves)
    if not legal_moves:
        return None

    # Shuffling prevents AI from repeating openings every game
    random.shuffle(legal_moves)

    for move in legal_moves:
        gs.logic_board.push(move)
        evaluation = -negamax(gs.logic_board, depth - 1, -beta, -alpha)
        gs.logic_board.pop()

        if evaluation > max_eval:
            max_eval = evaluation
            best_logic_move = move
        
        alpha = max(alpha, evaluation)

    # Translate python-chess Move object back to custom ChessEngine.Move
    if best_logic_move:
        uci = best_logic_move.uci()     # Format: e.g., "e2e4"

        start_sq = (ChessEngine.Move.ranksToRows[uci[1]], ChessEngine.Move.filesToCols[uci[0]])
        end_sq = (ChessEngine.Move.ranksToRows[uci[3]], ChessEngine.Move.filesToCols[uci[2]])

        return ChessEngine.Move(start_sq, end_sq, gs.board)
    
    return None

DIFFICULTY_PROFILES = {
    "easy":  {2: 0.7, 3: 0.2, 4: 0.1},
    "medium": {5: 0.6, 6: 0.3, 7: 0.1},
    "hard": {7: 0.5, 8: 0.3, 9: 0.2}
}

def difficulty(weight_map):
    depths = list(weight_map.keys())
    weights = list(weight_map.values())
    return random.choices(depths, weights=weights, k=1)[0]

def pick_search_depth(profile_name):
    weight_map = DIFFICULTY_PROFILES[profile_name]
    depths = list(weight_map.keys())
    weights = list(weight_map.values())
    return random.choices(depths, weights=weights, k=1)[0]

def play_style():
    return