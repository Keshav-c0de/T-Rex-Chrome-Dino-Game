# 🦖 Chrome Dino Game Clone

A fully functional replica of the famous Google Chrome offline dinosaur game, built using **Python** and **Pygame**. 

## 🎮 Features
* **Infinite Runner Mechanics:** The game speed increases as your score goes up.
* **Animations:** Smooth sprite animations for running, ducking, and jumping.
* **Obstacles:** Random generation of Small Cacti, Large Cacti, and Flying Birds.
* **Score System:** Tracks current score and increases difficulty every 100 points.
* **Game States:** Includes a Start Menu with jump animation and a Game Over screen with restart functionality.

## 📸 Screenshots

![Game Play](assets/DinoRun1.png)
*Classic Gameplay*

## 🛠️ Installation & Setup

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/Keshav-c0de/T-Rex-Chrome-Dino-Game.git](https://github.com/Keshav-c0de/T-Rex-Chrome-Dino-Game.git)
    cd dino-game
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
