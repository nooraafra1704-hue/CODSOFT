# 🎮 Tic-Tac-Toe AI

An unbeatable Tic-Tac-Toe AI agent built in Python, using the **Minimax algorithm** with optional **Alpha-Beta Pruning**. Play against the computer in your terminal — you can win at best a draw, never a victory!

This project demonstrates core concepts of **game theory** and **adversarial search algorithms** used widely in AI for two-player, zero-sum games.

---

## 📌 Features

- 🧠 **Unbeatable AI** powered by the Minimax algorithm
- ⚡ **Alpha-Beta Pruning** option for faster decision-making (skips exploring irrelevant branches)
- 🔁 Choose to play as **X or go first/second**
- 📊 Displays number of nodes explored and time taken by the AI for each move
- 🖥️ Simple, clean command-line interface
- 🔄 Play multiple rounds without restarting the program

---

## 🧩 How It Works

### Minimax Algorithm
Minimax is a recursive decision-making algorithm used in two-player games. It works by:
1. Simulating every possible future move.
2. Assuming the opponent always plays optimally (to minimize the AI's score).
3. The AI (maximizer) picks the move that leads to the best guaranteed outcome, while the opponent (minimizer) tries to lead to the worst outcome for the AI.
4. Scores are assigned to terminal states: `+10` for an AI win, `-10` for a human win, `0` for a draw (adjusted by depth so the AI prefers quicker wins and slower losses).

### Alpha-Beta Pruning
Alpha-Beta Pruning is an optimization on top of Minimax that **cuts off branches of the search tree that cannot possibly influence the final decision**, significantly reducing the number of nodes explored without affecting the correctness of the result.

- `alpha`: the best score the maximizer can guarantee so far
- `beta`: the best score the minimizer can guarantee so far
- If at any point `beta <= alpha`, the remaining branches are skipped ("pruned").

This project lets you toggle between **plain Minimax** and **Minimax + Alpha-Beta Pruning** so you can directly compare the number of nodes explored by each.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher (no external libraries required — uses only the standard library)

### Installation

```bash
git clone https://github.com/<nooraafra1704-hue>/tic-tac-toe-ai.git
cd tic-tac-toe-ai
```

### Run the game

```bash
python tic_tac_toe.py
```

---

## 🎯 How to Play

1. Run the script.
2. Choose the AI mode (Alpha-Beta Pruning or Plain Minimax).
3. Choose whether you want to go first.
4. Enter a number **1-9** corresponding to the board position you want to play:

```
 1 | 2 | 3
---+---+---
 4 | 5 | 6
---+---+---
 7 | 8 | 9
```

5. The AI will respond with its move, along with how many nodes it explored and how long it took.
6. The game announces the winner or a draw at the end, and you can choose to play again.

---

## 📁 Project Structure

```
tic-tac-toe-ai/
│
├── tic_tac_toe.py     # Main game logic, board, and AI implementation
└── README.md          # Project documentation
```

---

## 🛠️ Possible Extensions

- Add a GUI using `tkinter` or `pygame`
- Add difficulty levels (e.g., random AI, limited-depth Minimax)
- Support for larger boards (e.g., 4x4, 5x5) with a win-length condition
- Track and display win/loss/draw statistics across sessions
- Deploy as a web app using Flask/Django + JavaScript frontend

---

## 📚 Concepts Demonstrated

- Game trees and adversarial search
- Recursion and backtracking
- Time/space complexity trade-offs (Minimax vs Alpha-Beta Pruning)
- Zero-sum game theory

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙌 Acknowledgements

Built as part of an AI/ML learning task on implementing classic search algorithms in game-playing agents.
