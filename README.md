# AI-DS-mini-project: Interactive Maze Solver

This project implements and visualizes different maze-solving algorithms, specifically Depth-First Search (DFS) and Breadth-First Search (BFS). It provides an interactive experience allowing users to choose between different maze types and observe the algorithm's performance in real-time.

## Key Features & Benefits

*   **Interactive Maze Generation:** Generates both perfect mazes (with a single unique path) and multi-path mazes.
*   **Algorithm Visualization:** Visually demonstrates the DFS and BFS algorithms as they explore the maze.
*   **Clear Comparison:** Highlights the differences in exploration strategies and pathfinding between DFS and BFS.
*   **User-Friendly Interface:** Simple command-line interface for selecting maze type and initiating the solver.
*   **Customizable Visuals:** Uses Pygame for a configurable visual representation of the maze and solving process.

## Prerequisites & Dependencies

Before running this project, ensure you have the following installed:

*   **Python 3.x:** The project is written in Python 3.
*   **NumPy:** For maze generation and manipulation.  Install using: `pip install numpy`
*   **Pygame:** For visualization. Install using: `pip install pygame`

## Installation & Setup Instructions

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd AI-DS-mini-project
    ```
    Replace `<repository_url>` with the actual URL of this GitHub repository.

2.  **Install dependencies:**
    ```bash
    pip install numpy pygame
    ```

## Usage Examples

1.  **Run the `main.py` script:**
    ```bash
    python main.py
    ```

2.  **Follow the on-screen instructions:**
    *   The script will prompt you to select a maze type: `Perfect Maze (1)` or `Multi-Path Maze (2)`.  Enter `1` or `2` (or press Enter for the default `1`).
    *   A Pygame window will open, displaying the maze and visualizing the solving algorithm.  The visualization speed is controllable via delays built into the algorithms.
    *   The visualization shows explored cells and the final path.

## Project Structure

```
AI-DS-mini-project/
├── algorithms.py     # Contains the maze solving algorithms (DFS, BFS).
├── main.py           # Main script to run the interactive maze solver.
├── maze_generator.py # Generates the maze using recursive backtracking.
├── visualizer.py     # Handles the Pygame visualization of the maze and algorithms.
└── README.md         # Project documentation.
```

## Important Files and Code Snippets

### `algorithms.py`

```python
from collections import deque
import random

class MazeSolver:
    def __init__(self, maze):
        self.maze = maze
        self.rows, self.cols = maze.shape
        self.visited = set()
        self.path = []
        self.explored = []
    
    def is_valid(self, x, y):
        return (0 <= x < self.cols and 0 <= y < self.rows and 
                self.maze[y, x] == 0 and (x, y) not in self.visited)
    
    def dfs(self, start, end):
        """Depth-First Search using Stack"""
```

### `main.py`

```python
from maze_generator import MazeGenerator
from algorithms import MazeSolver
from visualizer import MazeVisualizer

def main():
    print("="*70)
    print(" "*15 + "INTERACTIVE MAZE SOLVER - DFS vs BFS")
    print("="*70)
    print("\nSelect maze type:")
    print("  1. Perfect Maze (one unique path)")
    print("  2. Multi-Path Maze (multiple routes, BFS finds shortest)")

    choice = input("Enter choice [1 or 2, default 1]: ").strip() or "1"
    maze_type = int(choice) if choice in ["1", "2"] else 1
```

### `maze_generator.py`

```python
import numpy as np
import random

class MazeGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def generate_recursive_backtracking(self):
        """Generate perfect maze with recursive backtracking (single shortest path)"""
        maze = np.ones((self.height * 2 + 1, self.width * 2 + 1), dtype=int)
        start_x, start_y = 0, 0
        maze[start_y * 2 + 1, start_x * 2 + 1] = 0
        stack = [(start_x, start_y)]
```

### `visualizer.py`

```python
import pygame
import random

class CellType:
    WALL = (20, 20, 20)
    PATH = (255, 255, 255)
    EXPLORED_DFS = (100, 150, 255)
    EXPLORED_BFS = (255, 180, 100)
    FINAL_PATH = (34, 177, 76)
    START = (66, 133, 244)
    END = (219, 68, 55)

class Button:
    def __init__(self, x, y, width, height, text, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
```

## Configuration Options

The maze dimensions (width and height) can be configured by modifying the `MazeGenerator` instantiation parameters in `main.py`. Also, the visualization speed can be controlled by adjusting delay parameters inside the algorithm's loop inside `algorithms.py`.


## License Information

This project has no specified license. All rights are reserved.

## Acknowledgments

*   The implementation of the maze generation algorithm is based on the recursive backtracking algorithm.
*   The visualization is powered by the Pygame library.
