# Neon Hunt

## Game Reules
Neon Hunt is a grid-based escape AI project for Track B. The player controls the Hacker, who must reach the exit or survive while the Cyber Beast tries to catch them.

## Run
Simply run the main.py file with python interpreter:

```bash
python main.py
```

OR  

On Windows:

```bash
run_windows.bat
```

On Linux:
```bash
./run_linux.sh
```

## AI
Whole point of this project was to implement an AI algorithm to play it. The AI is implemented in `student_player_ai.py`. There are two main algorithms implemented to solve this problem:

### Minimax
This algorithm uses a recursive approach to find the best move. The minimax function is being called once for the maximizing player (the hacker) and for the minimizing player (the monster) after that.  
It uses an evaluation function as the base case to avoid searching deep nodes and preventing the execution time to explode.

### Alpha-Beta Prouning
This algorithm works same as minimax but it prunes some nodes based on the current found evaluation bound of the current node.