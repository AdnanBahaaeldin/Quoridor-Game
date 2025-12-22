# 🎮 Quoridor Game – Python Implementation

## 📌 Game Description: Quoridor
This project is a complete implementation of the **Quoridor** abstract strategy board game for **two players**, developed in Python. The game follows the official Quoridor rules and features a graphical user interface, full move validation, wall placement constraints, and an artificial intelligence opponent with multiple difficulty levels.

Players take turns either moving their pawn or placing a wall to block their opponent, with the goal of being the first to reach the opposite side of the board. The game supports both **Human vs. Human** and **Human vs. Computer** gameplay modes.

## 📌 Game Description: Quoridor
### **Game Rules**
1. Game Board: The game is played on a 9×9 square board. 
2. Players: 2 players can play. 
3. Game Pieces:  
    * Each player has a pawn that begins at the center of their respective base line 
    * Each player has 10 walls  
4. Objective: Be the first player to move your pawn to any square on the opposite side of the board. 
5. Movement:  
    * On each turn, a player must either move their pawn or place a wall 
    * Pawns move one square orthogonally (not diagonally) 
    * Players cannot move through walls or opponent pawns 
    * If a player's pawn is adjacent to an opponent's pawn, the player can jump over the opponent's pawn (if there's no wall blocking) 
    * If a jump is blocked by a wall, the player can move diagonally around the opponent's pawn 
6. Wall Placement:  
    * Walls are two squares long and are placed on the edges between squares 
    * Walls cannot overlap or cross other walls 
    * Walls cannot be placed to completely block a player's path to the goal (there must always be a valid path to the goal for each player) 
    * Once placed, walls cannot be moved
---

## 🖼️ Screenshots & Controls
The first page shows 2 options: either to start a new game or load a previously saved game.

<img width="1003" height="779" alt="Screenshot 2025-12-22 221807" src="https://github.com/user-attachments/assets/2b777c70-7137-4805-bc14-abbd11790a72" />

If we choose New game the second page shows 2 options: either to play against AI or a human.

<img width="997" height="779" alt="Screenshot 2025-12-22 221824" src="https://github.com/user-attachments/assets/cf84c706-3aaa-4b85-917a-9c9a05279bae" />

This page shows a game started against a human shwoing controls for valid moves, how to put walls, the number of walls available for each player, and how to save the game.

<img width="3156" height="2475" alt="Picture1" src="https://github.com/user-attachments/assets/54fe0dad-1a09-4f8c-bce3-cb1a5fce1793" />

This page 3 difficulty level if you choose to play against AI on the second page.

<img width="998" height="777" alt="Screenshot 2025-12-22 221907" src="https://github.com/user-attachments/assets/b35e6b74-5f0d-4aa0-bbb7-4a454c36ad92" />

This page shows controls for choosing the direction of walls placed on the board in a game against AI.

<img width="3174" height="2475" alt="Picture2" src="https://github.com/user-attachments/assets/bd03bc33-7426-4c88-aa85-03062aab9da6" />

This page winnig message that appears whenever a player reaches his goal row.

<img width="3172" height="2475" alt="Picture3" src="https://github.com/user-attachments/assets/658a3094-f1c0-4409-9fb2-9aae31acbe54" />



<!-- Example placeholders -->
<!-- ![Main Menu](screenshots/menu.png) -->
<!-- ![Gameplay](screenshots/gameplay.png) -->
<!-- ![Wall Placement](screenshots/walls.png) -->

---

## ⚙️ Installation and Running Instructions

### **Prerequisites**
- Python 3.8 or higher
- `pip` package manager

### **Setup Steps**
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/quoridor-game.git
2. Navigate to the project directory:
   ```bash   
   cd quoridor-game
3. Install dependencies:
   ```bash
   pip install pygame
4. Run the Game:
   ```bash
   python main.py

🤖 Game Modes

Human vs. Human (local multiplayer)
Human vs. Computer (AI opponent)

📚 Technologies Used

- Python
- Pygame
- BFS Pathfinding
- Minimax with Alpha-Beta Pruning

## 📁 Project Structure

```text
quoridor-game/
│
├── main.py
├── board.py
├── player.py
├── AIPlayer.py
├── game_state.py
├── widgets.py
├── pathfinding.py
│
├── save_game.json
│
├── redo-arrow-symbol.png
├── undo-circular-arrow.png
├── image.png
├── bookmark.png
│
├── requirements.txt
│
└── README.md
```

## 🎥 Demo Video


https://github.com/user-attachments/assets/6a8aeee1-efd5-40dd-93b2-2f6b9aeca436

