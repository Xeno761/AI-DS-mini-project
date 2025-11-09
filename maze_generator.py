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
        visited = set([(start_x, start_y)])
        
        while stack:
            x, y = stack[-1]
            directions = [(1,0),(0,1),(-1,0),(0,-1)]
            random.shuffle(directions)
            
            found = False
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height and (nx, ny) not in visited:
                    maze[y * 2 + 1 + dy, x * 2 + 1 + dx] = 0
                    maze[ny * 2 + 1, nx * 2 + 1] = 0
                    visited.add((nx, ny))
                    stack.append((nx, ny))
                    found = True
                    break
            if not found:
                stack.pop()
        return maze

    def generate_multi_path_maze(self):
        """
        Start with a perfect maze, then randomly knock out walls to create loops
        so multiple paths exist between start/end, but overall structure/density is preserved.
        """
        maze = self.generate_recursive_backtracking()
        h, w = maze.shape
        attempts = max(10, (h * w) // 15)  # More attempts for bigger mazes
        
        for _ in range(attempts):
            x = random.randrange(1, w - 1, 2)
            y = random.randrange(1, h - 1, 2)
            # Try knocking down a wall adjacent to two paths
            directions = [(1,0), (-1,0), (0,1), (0,-1)]
            random.shuffle(directions)
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                fx, fy = x + 2*dx, y + 2*dy
                if 0 < nx < w-1 and 0 < ny < h-1 and 0 < fx < w-1 and 0 < fy < h-1:
                    # Only add loop if both end cells are path and the wall is closed:
                    if maze[ny, nx] == 1 and maze[fy, fx] == 0 and maze[y, x] == 0:
                        maze[ny, nx] = 0
                        break  # don't over-collapse this spot

        return maze

    def get_maze(self, maze_type=1):
        if maze_type == 2:
            return self.generate_multi_path_maze()
        else:
            return self.generate_recursive_backtracking()
