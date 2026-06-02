# Reactive Chess Game Algorithm

## Overview
The game continuously reacts to player moves by validating input, updating the board, and checking game conditions.

## Algorithm

1. Initialize a chess board with all pieces in their starting positions.
2. Display the current board to the players.
3. Wait for the current player to enter a move.
4. Validate the move using the chess rules.
5. If the move is invalid:
   Display an error message.
   Request another move.
6. If the move is valid:
   Update the board state.
   Remove any captured pieces.
   Record the move in the game history.
7. Check for special game conditions:
   Check
   Checkmate
   Stalemate
   Draw
8. Update the user interface to reflect the new board state.
9. Switch the turn to the opposing player.
10. Repeat steps 3–9 until the game ends.
11. Display the game result and allow players to start a new game or exit.





Start
  |
Initialize Board
  |
Display Board
  |
Get Player Move
  |
Is Move Legal?
 /           \
No           Yes
 |             |
Show Error   Update Board
 |             |
Retry      Check Game Status
               |
         Game Over?
          /      \
        No       Yes
        |         |
   Switch Turn  Show Result
        |
   Get Player Move

## Pseudocode

start new chess board
BEGIN

WHILE game is not over

    Display Board

    Generate Legal Moves for Current Player

    Get Player Move

    IF move is in Legal Moves THEN

        Execute Move
        Update Board State
        Record Move in History

        IF opponent is in Check THEN
            Display "Check"
        END IF

        IF Checkmate THEN
            Display Winner
            End Game
        ELSE IF Stalemate OR Draw THEN
            Display Draw
            End Game
        ELSE
            Switch Player Turn
        END IF

    ELSE
        Display "Invalid Move"
    END IF

END WHILE

END
    
