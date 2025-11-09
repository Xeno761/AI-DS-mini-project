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
        self.visited.clear()
        self.path.clear()
        self.explored.clear()
        
        stack = [start]
        self.visited.add(start)
        parent = {start: None}
        
        directions = [(0,1),(1,0),(0,-1),(-1,0)]
        
        while stack:
            x, y = stack.pop()
            self.explored.append((x, y))
            
            if (x, y) == end:
                current = end
                while current is not None:
                    self.path.append(current)
                    current = parent[current]
                self.path.reverse()
                return self.path, self.explored
            
            dirs = directions.copy()
            random.shuffle(dirs)
            
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if self.is_valid(nx, ny):
                    self.visited.add((nx, ny))
                    parent[(nx, ny)] = (x, y)
                    stack.append((nx, ny))
        
        return [], self.explored
    
    def bfs(self, start, end):
        """Breadth-First Search using Queue"""
        self.visited.clear()
        self.path.clear()
        self.explored.clear()
        
        queue = deque([start])
        self.visited.add(start)
        parent = {start: None}
        
        directions = [(0,1),(1,0),(0,-1),(-1,0)]
        
        while queue:
            x, y = queue.popleft()
            self.explored.append((x, y))
            
            if (x, y) == end:
                current = end
                while current is not None:
                    self.path.append(current)
                    current = parent[current]
                self.path.reverse()
                return self.path, self.explored
            
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if self.is_valid(nx, ny):
                    self.visited.add((nx, ny))
                    parent[(nx, ny)] = (x, y)
                    queue.append((nx, ny))
        
        return [], self.explored
