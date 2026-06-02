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

while game_not_over:
    display_board()

    move = get_player_move()

    if move_is_legal(move):
        make_move(move)
        update_display()

        if checkmate:
            end_game()
    else:
        show_error()
    
