import pygame as p
import ChessEngine
import ChessAI # Import new ChessAI module

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
    sqSelected = () #no square is selected, keep track of the last click of the user (Tuple: (row,col))
    playerClicks = []

    # Adding Config Variables
    playerOne = True    # Set to True if human is playing white, set to False if AI
    playerTwo = False   # Set to True if human is playing black, set to False if AI

    while running:
        # Determine if it's currently a human's turn to play
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        is_over = gs.game_over()

        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN and humanTurn and not is_over:
                location = p.mouse.get_pos() #(x, y) location of mouse
                col = location[0] // SQ_SIZE
                row = location [1] // SQ_SIZE
                if sqSelected == (row, col): # the user clicked the same square twice
                    sqSelected = () #deselect
                    playerClicks = [] #clear player clicks
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected) # append for both 1st and 2nd clicks
                if len(playerClicks) == 2: #after 2nd click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    if gs.is_legal(move): # Tests if move is Legal
                        print(move.getChessNotation())
                        gs.makeMove(move)
                        sqSelected = () #reset user clicks
                        playerClicks = []
                    else:
                        sqSelected = ()  # reset user clicks
                        playerClicks = []
                        print("Invalid move")
                        sqSelected = ()
                        playerClicks = []
        
        if not running:
            break
        
        if not humanTurn and not is_over:
            d = ChessAI.pick_search_depth("hard")
            ai_move = ChessAI.get_best_move(gs, d)
            if ai_move is not None:
                print(f"AI Move: {ai_move.getChessNotation()}")
                gs.makeMove(ai_move)
            else:
                print("No moves left for AI")
        
        if gs.game_over():
            game_ended, reason = gs.game_over()
            if game_ended:
                print(f"Game Over: {reason}")
                running = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)


def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()