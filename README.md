# Game-Theory-NIM-game-with-boxes


Project sets up to make a functional game of NIM using Game Theory.

There are two parts in my project.

The first one is the backend that is made of two classes: Board - which creates all the boxes that need to be moved; Game - where it processes all the AI movements and requests, validates and does the player movements.

(There is also a LegacyGame which remains there since it was the first iteration of this project, but is not used anywhere)

The AI is making it's moves by applying a Parity Strategy onto a MinMax Strategy. It checks if a move is to it's benefit leaving the board in a stable state and if it cannot it leaves it in the most stable unstable state it can. For this problem the AI understands that the more to the left it is the more unstable the state is whether the more to the right it is it becomes more stable.

It tries to find a solution similar to AI algoritms in chess, but does not optimize between soulutions found and such may lead to lengthy games and some amuzing moves, though they still can lead to the players defeat.

The player inputs what box he wishes to move and where to move it and if the two parameters are validated the program moves it.

The program loops until a winner is found, after which it states it.

The second one is the frontend that is a basic UI that contains a few boxes and a start button to announc that you or the computer must make another move.
