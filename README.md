# 🦖 Chrome Dino game:

A faithful recreation of the classic Chrome Dinosaur game built using **Python** and **Pygame**. This project goes beyond the original with advanced features like a mathematically calculated day/night cycle, parallax scrolling, and sophisticated collision management.

## 📸 Screenshots

[Day Mode]<img width="1094" height="627" alt="Screenshot 2026-01-16 at 4 37 25 PM" src="https://github.com/user-attachments/assets/f204a808-5735-419b-b742-65e6e52f6b05" /> | [Night Mode]<img width="1092" height="622" alt="Screenshot 2026-01-16 at 4 37 52 PM" src="https://github.com/user-attachments/assets/3e4ec585-167d-4a74-8298-389c2a230f45" />
--- | ---
## ✨ Key Features

* **Infinite Runner Mechanics:** Smooth acceleration, jumping, and ducking physics.
* **Dynamic Day/Night Cycle:**
    * Features a **Sun and Moon** that rise and set along a **Sine Wave** trajectory.
    * Realistic **Parallax Scrolling** (Celestial bodies move slower than the ground).
    * **Automatic Night Mode:** The game world colors invert mathematically using `BLEND_SUB` filters when the moon rises.
* **Smart Menu System:**
    * **Death Cam:** The Game Over screen captures a screenshot of the exact moment of impact.
    * **Interactive UI:** Toggle Day/Night mode manually from the menu, with the celestial body persisting its position seamlessly into the game loop.
* **High Score System:** Persists player high scores using local file I/O.
* **Obstacles:** Randomly generated Small Cacti, Large Cacti, and flying Birds.

## 🛠️ Technical Highlights

This isn't just a clone; it implements several interesting programming concepts:

* **Sine Wave Trajectory:** The Sun and Moon follow a calculated curve using `math.sin()`, varying their height based on their progress across the screen.
* **Subtractive Rendering:** Instead of loading separate "Dark Mode" textures, the game uses `pygame.BLEND_SUB` to mathematically invert the pixel colors of the rendering surface in real-time.
* **State Management:** The game preserves the coordinates of the celestial bodies between the Game Loop and the Menu, creating a continuous visual experience.

## 🚀 How to Run

### Prerequisites
You need Python installed on your machine.

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/Keshav-c0de/T-Rex-Chrome-Dino-Game.git](https://github.com/Keshav-c0de/T-Rex-Chrome-Dino-Game.git)
    cd T-Rex-Chrome-Dino-Game
    ```

2.  **Install Pygame**
    ```bash
    pip install pygame
    ```

3.  **Run the Game**
    ```bash
    python dinogame.py
    ```

## 🎮 Controls

* **Space / Up Arrow:** Jump
* **Down Arrow:** Duck
* **Mouse Click:** Toggle Day/Night icon in the Menu

## 📂 Project Structure

* `main.py`: Contains the Game Loop, Menu Logic, and Class definitions.
* `assets/`: Folder containing sprites (Dino, Cactus, Bird, Cloud).
* `high_score.txt`: Automatically generated file to store the best score.
* `sound/`: Folder containing sound-effects (jump, die, score).

---
*Created with Python and Pygame.*
