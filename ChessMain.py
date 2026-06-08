import pygame as p
import ChessEngine
import ChessAI  # Import new ChessAI module
import chess

p.init()

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = WIDTH // DIMENSION
MAX_FPS = 15
IMAGES = {}


def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    loadImages()

    running = True
    sqSelected = ()  # no square is selected, keep track of the last click of the user (Tuple: (row,col))
    playerClicks = []
    validSquares = []

    # Adding Config Variables
    playerOne = True    # Set to True if human is playing white, set to False if AI
    playerTwo = False   # Set to True if human is playing black, set to False if AI
    gs.player = playerOne
    while running:
        # Determine if it's currently a human's turn to play
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        is_over = gs.game_over()

        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN and humanTurn and not is_over:
                location = p.mouse.get_pos()  # (x, y) location of mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE

                if sqSelected == (row, col):  # the user clicked the same square twice
                    sqSelected = ()  # deselect
                    playerClicks = []  # clear player clicks
                    validSquares = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)  # append for both 1st and 2nd clicks

                # After first click, show legal destination squares for that piece
                if len(playerClicks) == 1:
                    startRow, startCol = playerClicks[0]
                    selected_square = chess.square(startCol, 7 - startRow)
                    validSquares = []

                    for move in gs.logic_board.legal_moves:
                        if move.from_square == selected_square:
                            to_col = chess.square_file(move.to_square)
                            to_row = 7 - chess.square_rank(move.to_square)
                            validSquares.append((to_row, to_col))

                    # If clicked square has no legal moves, deselect it
                    if not validSquares:
                        playerClicks = []
                        sqSelected = ()

                if len(playerClicks) == 2:  # after 2nd click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    if gs.is_legal(move):  # Tests if move is Legal
                        print(move.getChessNotation())
                        gs.makeMove(move)
                        sqSelected = ()
                        playerClicks = []
                        validSquares = []
                    else:
                        print("Invalid move")
                        sqSelected = ()
                        playerClicks = []
                        validSquares = []

        if not running:
            break

        # AI move
        if not humanTurn and not is_over:
            ai_move = ChessAI.get_best_move(gs, depth=3)
            if ai_move is not None:
                print(f"AI Move: {ai_move.getChessNotation()}")
                gs.makeMove(ai_move)
                validSquares = []
            else:
                print("No moves left for AI")

        if gs.game_over():
            game_ended, reason = gs.game_over()
            if game_ended:
                print(f"Game Over: {reason}")
                running = False

        drawGameState(screen, gs, validSquares)
        clock.tick(MAX_FPS)
        p.display.flip()


def drawGameState(screen, gs, validSquares):
    drawBoard(screen)
    highlightSquares(screen, validSquares)
    drawPieces(screen, gs.board)


def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def highlightSquares(screen, validSquares):
    highlight = p.Surface((SQ_SIZE, SQ_SIZE))
    highlight.set_alpha(120)
    highlight.fill(p.Color("yellow"))

    for row, col in validSquares:
        screen.blit(highlight, (col * SQ_SIZE, row * SQ_SIZE))


if __name__ == "__main__":
    main()
