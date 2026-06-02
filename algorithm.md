# Reactive Chess Game Algorithm

## Overview
The game continuously reacts to player moves by validating input, updating the board, and checking game conditions.

## Algorithm

1. Initialize a chess board with all pieces in their starting positions.
2. Display the current board to the players.
3. Wait for the current player to enter a move.
4. Validate the move using the chess rules:
   •	Piece Selection: Identify which piece the player has selected.
   •	Move Validation: Check if the destination square is legal for the selected piece’s movement.
	•	Check Condition: Ensure the move does not put the player’s king in check.
6. If the move is invalid:
   •  Display an error message.
   •  Request another move.
7. If the move is valid:
   •  Update the board state.
   •  Remove any captured pieces.
   •  Record the move in the game history.
8. Check for special game conditions:
   •  Check
   •  Checkmate
   •  Stalemate
   •  Draw
9. Update the user interface to reflect the new board state.
10. 10. Switch the turn to the opposing player.
11. Repeat steps 3–9 until the game ends.
12. Display the game result and allow players to start a new game or exit.


Flow Chart: 

Start
  |
Initialize Board
  |
Display Board
  |
Get Player Move
  |
Identify Selected Piece
  |
Check Piece Movement
  |
Movement Valid?
 /            \
No            Yes
 |              |
Show Error   Check Destination Square
 |              |
Retry      Destination Valid?
           /              \
         No               Yes
         |                  |
   Show Error      Check King Safety
         |                  |
       Retry          King Safe?
                      /      \
                    No       Yes
                    |          |
              Show Error   Update Board
                    |          |
                  Retry   Check Game Status
                              |
                        Game Over?
                         /      \
                       No       Yes
                       |          |
                  Switch Turn  Show Result
                       |
                  Display Board
                       |
                  Get Player Move

## Pseudocode

Start Game

Initialize chess board
Set current player to White

While game is not over:

    Display board

    Wait for player input

    Player selects a piece
    Player selects a destination square

    Identify the selected piece type

    Generate legal moves for that piece
        Pawn: forward movement and diagonal capture
        Rook: horizontal and vertical movement
        Bishop: diagonal movement
        Knight: L-shaped movement
        Queen: horizontal, vertical, and diagonal movement
        King: one-square movement

    Check if the selected destination is legal

    If move is legal:
        Update the board
        Switch turns
    Else:
        Display "Invalid move"
        Ask player to choose again

    Check game status
        If checkmate:
            End game
        If stalemate or draw:
            End game

End Game
End    
