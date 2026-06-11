import pygame as p
import ChessEngine
import ChessAI  # Import new ChessAI module
import chess

p.init()

WIDTH = 512
HEIGHT = 552
TOP_BAR = 40
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
    playerOne, playerTwo, ai_depth = chooseGameMode(screen)
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
                
                undoRect = p.Rect(10, 10, 80, 30)

                if undoRect.collidepoint(location):
                    undo_count = 2 if (not playerOne or not playerTwo) else 1

                    for _ in range(undo_count):
                        if len(gs.logic_board.move_stack) > 0:
                            gs.logic_board.pop()

                    gs.syncBoardFromLogic()
                    gs.whiteToMove = gs.logic_board.turn
                    continue
                
                col = location[0] // SQ_SIZE
                row = (location[1] - TOP_BAR) // SQ_SIZE

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

                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)

                    if gs.is_legal(move):
                        promotion_choice = None

                        if move.pieceMoved[1] == "p" and (move.endRow == 0 or move.endRow == 7):
                            promotion_choice = choosePromotion(screen, move.pieceMoved[0])

                        gs.makeMove(move, promotion_choice)

                    else:
                        print("Invalid move")

                    sqSelected = ()
                    playerClicks = []
                    validSquares = []

        if not running:
            break

        # AI move
        if not humanTurn and not is_over:
            ai_move = ChessAI.get_best_move(gs, depth=ai_depth)
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
    drawUndo(screen)


def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE + TOP_BAR, SQ_SIZE, SQ_SIZE))

def drawUndo(screen):
    font = p.font.SysFont("arial", 20)

    p.draw.rect(screen, p.Color("lightgray"), (10, 10, 80, 30))
    p.draw.rect(screen, p.Color("black"), (10, 10, 80, 30), 2)

    text = font.render("Undo", True, p.Color("black"))
    screen.blit(text, (22, 15))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE + TOP_BAR, SQ_SIZE, SQ_SIZE))


def highlightSquares(screen, validSquares):
    highlight = p.Surface((SQ_SIZE, SQ_SIZE))
    highlight.set_alpha(120)
    highlight.fill(p.Color("yellow"))

    for row, col in validSquares:
        screen.blit(highlight, (col * SQ_SIZE, row * SQ_SIZE + TOP_BAR))

def choosePromotion(screen, color): #ui element
    choices = ["Q", "R", "B", "N"]
    menu_width = SQ_SIZE * 4
    menu_height = SQ_SIZE
    x = (WIDTH - menu_width) // 2
    y = (HEIGHT - menu_height) // 2

    while True:
        p.draw.rect(screen, p.Color("lightgray"), (x, y, menu_width, menu_height))

        for i, piece in enumerate(choices):
            piece_code = color + piece
            rect = p.Rect(x + i * SQ_SIZE, y, SQ_SIZE, SQ_SIZE)
            p.draw.rect(screen, p.Color("white"), rect)
            screen.blit(IMAGES[piece_code], rect)

        p.display.flip()

        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                quit()

            if e.type == p.MOUSEBUTTONDOWN:
                mx, my = p.mouse.get_pos()

                if y <= my <= y + SQ_SIZE and x <= mx <= x + menu_width:
                    index = (mx - x) // SQ_SIZE
                    return choices[index].lower()


def chooseGameMode(screen):
    font = p.font.SysFont("arial", 28)

    playerOne = True
    playerTwo = False
    ai_depth = 3

    buttons = {
        "p1_person": p.Rect(180, 120, 120, 45),
        "p1_ai":     p.Rect(310, 120, 120, 45),
        "p2_person": p.Rect(180, 200, 120, 45),
        "p2_ai":     p.Rect(310, 200, 120, 45),
        "minus":     p.Rect(230, 285, 50, 45),
        "plus":      p.Rect(300, 285, 50, 45),
        "start":     p.Rect(156, 390, 200, 55)
    }

    while True:
        screen.fill(p.Color("white"))

        screen.blit(font.render("Choose Game Mode", True, p.Color("black")), (130, 50))

        screen.blit(font.render("Player 1:", True, p.Color("black")), (60, 125))
        screen.blit(font.render("Player 2:", True, p.Color("black")), (60, 205))
        screen.blit(font.render(f"Depth: {ai_depth}", True, p.Color("black")), (60, 292))

        for name, rect in buttons.items():
            color = p.Color("lightgray")

            if name == "p1_person" and playerOne:
                color = p.Color("lightblue")
            if name == "p1_ai" and not playerOne:
                color = p.Color("lightblue")
            if name == "p2_person" and playerTwo:
                color = p.Color("lightblue")
            if name == "p2_ai" and not playerTwo:
                color = p.Color("lightblue")
            if name == "start":
                color = p.Color("lightgreen")

            p.draw.rect(screen, color, rect)
            p.draw.rect(screen, p.Color("black"), rect, 2)

        labels = {
            "p1_person": "Person",
            "p1_ai": "AI",
            "p2_person": "Person",
            "p2_ai": "AI",
            "minus": "-",
            "plus": "+",
            "start": "Start"
        }

        for name, text in labels.items():
            rect = buttons[name]
            label = font.render(text, True, p.Color("black"))
            screen.blit(label, (
                rect.centerx - label.get_width() // 2,
                rect.centery - label.get_height() // 2
            ))

        p.display.flip()

        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                quit()

            if e.type == p.MOUSEBUTTONDOWN:
                pos = p.mouse.get_pos()

                if buttons["p1_person"].collidepoint(pos):
                    playerOne = True
                elif buttons["p1_ai"].collidepoint(pos):
                    playerOne = False
                elif buttons["p2_person"].collidepoint(pos):
                    playerTwo = True
                elif buttons["p2_ai"].collidepoint(pos):
                    playerTwo = False
                elif buttons["minus"].collidepoint(pos):
                    ai_depth = max(1, ai_depth - 1)
                elif buttons["plus"].collidepoint(pos):
                    ai_depth = min(5, ai_depth + 1)
                elif buttons["start"].collidepoint(pos):
                    return playerOne, playerTwo, ai_depth



if __name__ == "__main__":
    main()
