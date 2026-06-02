# Reactive Chess Game Algorithm

## Overview
The game continuously reacts to player moves by validating input, updating the board, and checking game conditions.

## Algorithm

1. Start a new chess board.
2. Display the board.
3. Wait for player input.
4. Validate the move.
5. If invalid, request another move.
6. If valid:
   - Update board state.
   - Refresh display.
   - Check for check, checkmate, stalemate, or draw.
7. Switch turns.
8. Repeat until game over.

## Pseudocode

start new chess board

while game is not over:
    display board
    get move from current player

    if move is legal:
        make move on board
        update display

        if player is in check:
            show check warning

        if game is over:
            show result
            break

        switch turns
    else:
        show "Invalid move"
    
