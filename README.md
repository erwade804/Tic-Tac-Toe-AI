Tic Tac Toe Machine Learnering Program

This is a homebrew algorithm, here's how it works. It takes the board and takes each of the locations of a move (x being 1, o being -1, nothing on the location being 0), and maps them to a location in space. It then finds the distance between the current board's state, and the next closest board state that it knows, and will find all the closest board states. Once the algorithm finds all the closest board states, if there are multiple that are the same distance from the current board state, it will chose one randomly based on the amount of times that board state shows up. For example, if board state 'A' is shown 5 times, and board state 'B' is shown once, board state 'A' will have 5 chances to be chosen, and board state 'B' will have one chance. 

Once each game is finished, the program takes the moves made by the winner, and places them in its known move list. If this list is longer than 1000, it will remove some to make room. I do this so that it will only have a specific amount of memory that is ever going to be used, and will not slow down significantly while in use. 

How to use:
  On the right, you will see the program learning against a very similar program. The board on the right will update every frame, so it may be hard to see what's happening. On the left, you can see the board, the AI will move first at all times to keep things simple for itself. You can make a move by clicking on the square you would like to make your move in. 







This is by no means the best or fastest algorithm. This is an attempt to design my own machine learning algorithm with minimal research on the topic. I will be revisiting this program at a later date once I've done more research, and learn more about AI and ML.


