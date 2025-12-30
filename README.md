# Chrome Dino Game Clone<img width="87" height="94" alt="DinoRun1" src="https://github.com/user-attachments/assets/a420dd44-9d33-4c3c-97df-7e38c9ca900e" />


A fully functional replica of the famous Google Chrome offline dinosaur game, built using **Python** and **Pygame**. 

## 🎮 Features
* **Infinite Runner Mechanics:** The game speed increases as your score goes up.
* **Animations:** Smooth sprite animations for running, ducking, and jumping.
* **Obstacles:** Random generation of Small Cacti, Large Cacti, and Flying Birds.
* **Score System:** Tracks current score and increases difficulty every 100 points.
* **Game States:** Includes a Start Menu with jump animation and a Game Over screen with restart functionality.

## 📸 Screenshot

<img width="1092" height="623" alt="Screenshot 2025-12-31 at 12 37 29 AM" src="https://github.com/user-attachments/assets/2fe63c23-30d4-41a8-836d-77d3c3d91620" />
*Classic Gameplay*

## 🛠️ Installation & Setup

1.  **Clone the repository**
    ```bash
    git clone https://github.com/Keshav-c0de/T-Rex-Chrome-Dino-Game.git
    cd T-Rex-Chrome-Dino-Game
    ```

2.  **Install Dependencies**
    You need Python installed. Then install Pygame:
    ```bash
    pip install pygame
    ```

3.  **Run the Game**
    ```bash
    python dinogame.py
    ```

## 🕹️ Controls

| Key | Action |
| :--- | :--- |
| **UP Arrow** / **Space** | Jump / Start Game |
| **DOWN Arrow** | Duck (to avoid birds) |
| **Any Key** | Restart Game after Death |

## 📂 Project Structure

```text
dino-game/
├── assets/          # Contains all images (Dino, Cactus, Bird, etc.)
├── dinogame.py      # Main game logic
└── README.md        # Project documentation
