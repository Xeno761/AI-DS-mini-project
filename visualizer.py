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
        self.is_hovered = False

    def draw(self, screen):
        color = tuple(min(c + 40, 255) for c in self.color) if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (100, 100, 100) if self.is_hovered else (50, 50, 50), 
                        self.rect, 2)
        font = pygame.font.Font(None, 18)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def update_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)

class MazeVisualizer:
    def __init__(self, maze, cell_size=1, maze_size="MEDIUM"):
        self.maze = maze
        self.cell_size = cell_size
        self.rows, self.cols = maze.shape
        self.maze_size = maze_size

        pygame.init()
        self.maze_width = self.cols * cell_size
        self.maze_height = self.rows * cell_size

        self.window_width = 800
        self.window_height = 700

        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(f"Maze Solver - DFS vs BFS ({maze_size})")
        self.clock = pygame.time.Clock()
        self.maze_x = (self.window_width - self.maze_width) // 2
        self.maze_y = 15

        button_width = (self.window_width - 50) // 2
        button_height = 40
        button_spacing_x = 10
        button_spacing_y = 8
        start_x = 20
        start_y = self.maze_y + self.maze_height + 20

        self.new_maze_button = Button(start_x, start_y, button_width, button_height, 
                                     "NEW MAZE", (76, 175, 80), (255, 255, 255))
        self.dfs_button = Button(start_x + button_width + button_spacing_x, start_y, 
                                button_width, button_height, 
                                "RUN DFS", (100, 150, 200), (255, 255, 255))
        self.bfs_button = Button(start_x, start_y + button_height + button_spacing_y, 
                                button_width, button_height, 
                                "RUN BFS", (150, 100, 200), (255, 255, 255))
        self.compare_button = Button(start_x + button_width + button_spacing_x, 
                                    start_y + button_height + button_spacing_y, 
                                    button_width, button_height, 
                                    "COMPARE", (255, 152, 0), (255, 255, 255))
        self.exit_button = Button(start_x, start_y + 2 * (button_height + button_spacing_y), 
                                 2 * button_width + button_spacing_x, button_height, 
                                 "EXIT", (244, 67, 54), (255, 255, 255))
        self.stats_y = start_y + 3 * (button_height + button_spacing_y) + 10
        self.start = None
        self.end = None
        self.get_random_start_end()

    def get_random_start_end(self):
        paths = []
        for y in range(self.rows):
            for x in range(self.cols):
                if self.maze[y, x] == 0:
                    paths.append((x, y))
        if len(paths) > 2:
            random.shuffle(paths)
            self.start = paths[0]
            self.end = paths[-1]
        else:
            self.start = (1, 1)
            self.end = (self.cols - 2, self.rows - 2)

    def draw_maze(self, highlight_explored=None, highlight_path=None, color_type=None):
        self.screen.fill((248, 248, 248))
        pygame.draw.rect(self.screen, (200, 200, 200),
                        (self.maze_x - 5, self.maze_y - 5, 
                         self.maze_width + 10, self.maze_height + 10), 2)
        maze_surface = pygame.Surface((self.maze_width, self.maze_height))
        maze_surface.fill(CellType.PATH)
        for y in range(self.rows):
            for x in range(self.cols):
                if self.maze[y, x] == 1:
                    pygame.draw.rect(maze_surface, CellType.WALL,
                                   (x * self.cell_size, y * self.cell_size,
                                    self.cell_size, self.cell_size))
        if highlight_explored:
            explore_color = CellType.EXPLORED_DFS if color_type == "DFS" else CellType.EXPLORED_BFS
            for ex, ey in highlight_explored:
                pygame.draw.rect(maze_surface, explore_color,
                               (ex * self.cell_size, ey * self.cell_size,
                                self.cell_size, self.cell_size))
        if highlight_path:
            for px, py in highlight_path:
                pygame.draw.rect(maze_surface, CellType.FINAL_PATH,
                               (px * self.cell_size, py * self.cell_size,
                                self.cell_size, self.cell_size))
        pygame.draw.rect(maze_surface, CellType.START,
                       (self.start[0] * self.cell_size, self.start[1] * self.cell_size,
                        self.cell_size, self.cell_size))
        pygame.draw.rect(maze_surface, CellType.END,
                       (self.end[0] * self.cell_size, self.end[1] * self.cell_size,
                        self.cell_size, self.cell_size))
        self.screen.blit(maze_surface, (self.maze_x, self.maze_y))

    def draw_ui_panel(self, stats=None):
        self.new_maze_button.draw(self.screen)
        self.dfs_button.draw(self.screen)
        self.bfs_button.draw(self.screen)
        self.compare_button.draw(self.screen)
        self.exit_button.draw(self.screen)
        if stats:
            font_small = pygame.font.Font(None, 16)
            y = self.stats_y
            for stat in stats:
                stat_text = font_small.render(stat, True, (80, 80, 80))
                text_x = (self.window_width - stat_text.get_width()) // 2
                self.screen.blit(stat_text, (text_x, y))
                y += 18

    def animate_search(self, start, end, explored, final_path, algorithm_name, color_type):
        self.draw_maze()
        self.draw_ui_panel()
        pygame.display.flip()
        pygame.time.wait(1000)
        # PHASE 1: Animate exploration (interruptible by NEW MAZE)
        for i, (ex, ey) in enumerate(explored):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False, None
                if event.type == pygame.MOUSEMOTION:
                    self.new_maze_button.update_hover(event.pos)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.new_maze_button.is_clicked(event.pos):
                        return "NEW_MAZE", None
            self.draw_maze(highlight_explored=explored[:i+1], color_type=color_type)
            progress_pct = ((i + 1) / len(explored)) * 100
            self.draw_ui_panel([
                f"{algorithm_name} - EXPLORING",
                f"Cell {i+1}/{len(explored)} ({progress_pct:.1f}%)",
                f"Strategy: {'Go DEEP (Stack)' if color_type == 'DFS' else 'Go BROAD (Queue)'}"
            ])
            pygame.display.flip()
            self.clock.tick(15)

        self.draw_maze(highlight_explored=explored, color_type=color_type)
        self.draw_ui_panel([
            f"{algorithm_name} - EXPLORATION COMPLETE",
            f"✓ Total cells explored: {len(explored)}",
            f"Now finding path from start to end..."
        ])
        pygame.display.flip()
        pygame.time.wait(1000)
        # PHASE 2: Animate path
        for i, (px, py) in enumerate(final_path):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False, None
                if event.type == pygame.MOUSEMOTION:
                    self.new_maze_button.update_hover(event.pos)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.new_maze_button.is_clicked(event.pos):
                        return "NEW_MAZE", None
            self.draw_maze(highlight_explored=explored, 
                          highlight_path=final_path[:i+1], 
                          color_type=color_type)
            progress_pct = ((i + 1) / len(final_path)) * 100
            self.draw_ui_panel([
                f"{algorithm_name} - BUILDING PATH",
                f"Step {i+1}/{len(final_path)} ({progress_pct:.1f}%)",
                f"Path so far: {len(final_path[:i+1])} steps traced"
            ])
            pygame.display.flip()
            self.clock.tick(15)

        self.draw_maze(highlight_explored=explored, 
                      highlight_path=final_path, 
                      color_type=color_type)
        self.draw_ui_panel([
            f"✓ {algorithm_name} - COMPLETE!",
            f"Explored: {len(explored)} cells | Path: {len(final_path)} steps",
            f"Route: Start {self.start} → End {self.end}"
        ])
        pygame.display.flip()
        pygame.time.wait(1500)
        return True, (len(explored), len(final_path))

    def show_comparison_screen(self, dfs_stats, bfs_stats):
        dfs_explored, dfs_path = dfs_stats
        bfs_explored, bfs_path = bfs_stats
        waiting = True
        while waiting:
            self.screen.fill((248, 248, 248))
            font_title = pygame.font.Font(None, 36)
            font_header = pygame.font.Font(None, 22)
            font_data = pygame.font.Font(None, 18)
            title = font_title.render("Algorithm Comparison", True, (33, 150, 243))
            title_rect = title.get_rect(center=(self.window_width // 2, 15))
            self.screen.blit(title, title_rect)
            box_width = (self.window_width - 80) // 2
            pygame.draw.rect(self.screen, CellType.EXPLORED_DFS, (30, 60, box_width, 130))
            pygame.draw.rect(self.screen, (50, 100, 200), (30, 60, box_width, 130), 3)
            dfs_title = font_header.render("DFS", True, (255, 255, 255))
            self.screen.blit(dfs_title, (50, 70))
            dfs_data = [
                f"Cells: {dfs_explored}",
                f"Path: {dfs_path} steps",
                "Type: DEPTH-FIRST"
            ]
            y = 100
            for data in dfs_data:
                text = font_data.render(data, True, (255, 255, 255))
                self.screen.blit(text, (50, y))
                y += 25
            bfs_x = 30 + box_width + 20
            pygame.draw.rect(self.screen, CellType.EXPLORED_BFS, (bfs_x, 60, box_width, 130))
            pygame.draw.rect(self.screen, (200, 100, 50), (bfs_x, 60, box_width, 130), 3)
            bfs_title = font_header.render("BFS", True, (255, 255, 255))
            self.screen.blit(bfs_title, (bfs_x + 20, 70))
            bfs_data = [
                f"Cells: {bfs_explored}",
                f"Path: {bfs_path} steps",
                "Type: BREADTH-FIRST"
            ]
            y = 100
            for data in bfs_data:
                text = font_data.render(data, True, (255, 255, 255))
                self.screen.blit(text, (bfs_x + 20, y))
                y += 25
            y = 210
            pygame.draw.line(self.screen, (200, 200, 200), (20, y), (self.window_width - 20, y), 2)
            analysis = font_header.render("Key Insights", True, (76, 175, 80))
            self.screen.blit(analysis, (20, y + 10))
            insights = []
            if dfs_explored > bfs_explored:
                diff = dfs_explored - bfs_explored
                pct = 100 * diff / dfs_explored
                insights.append(f"► BFS: {diff} fewer cells ({pct:.1f}%)")
            elif bfs_explored > dfs_explored:
                diff = bfs_explored - dfs_explored
                pct = 100 * diff / bfs_explored
                insights.append(f"► DFS: {diff} fewer cells ({pct:.1f}%)")
            else:
                insights.append("► Same cells explored")
            if dfs_path < bfs_path:
                insights.append(f"► DFS shorter: {dfs_path} vs {bfs_path}")
            elif bfs_path < dfs_path:
                insights.append(f"► BFS SHORTER: {bfs_path} vs {dfs_path} (BFS OPTIMAL!)")
            else:
                insights.append(f"► Same path: {dfs_path} steps")
            insights.extend([
                "► DFS uses Stack (LIFO)",
                "► BFS uses Queue (FIFO)",
                "► BFS GUARANTEES shortest path"
            ])
            y += 40
            for insight in insights:
                text = font_data.render(insight, True, (60, 60, 60))
                self.screen.blit(text, (20, y))
                y += 22
            close_button = Button(self.window_width - 130, self.window_height - 50, 110, 40, 
                                 "CLOSE", (244, 67, 54), (255, 255, 255))
            close_button.draw(self.screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEMOTION:
                    close_button.update_hover(event.pos)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if close_button.is_clicked(event.pos):
                        waiting = False
                    if self.new_maze_button.is_clicked(event.pos):
                        return "NEW_MAZE"
            self.clock.tick(30)
        return True

    def run_interactive(self, solver):
        running = True
        dfs_last_result = None
        bfs_last_result = None
        while running:
            self.draw_maze()
            self.draw_ui_panel([
                f"Start: {self.start} | End: {self.end}",
                f"{self.maze_size} ({self.cols}×{self.rows})"
            ])
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEMOTION:
                    self.new_maze_button.update_hover(event.pos)
                    self.dfs_button.update_hover(event.pos)
                    self.bfs_button.update_hover(event.pos)
                    self.compare_button.update_hover(event.pos)
                    self.exit_button.update_hover(event.pos)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.new_maze_button.is_clicked(event.pos):
                        return "NEW_MAZE"
                    elif self.dfs_button.is_clicked(event.pos):
                        dfs_path, dfs_explored = solver.dfs(self.start, self.end)
                        result, stats = self.animate_search(self.start, self.end, dfs_explored, 
                                                            dfs_path, "DFS", "DFS")
                        if result == "NEW_MAZE":
                            return "NEW_MAZE"
                        if not result:
                            return False
                        dfs_last_result = stats
                    elif self.bfs_button.is_clicked(event.pos):
                        bfs_path, bfs_explored = solver.bfs(self.start, self.end)
                        result, stats = self.animate_search(self.start, self.end, bfs_explored, 
                                                            bfs_path, "BFS", "BFS")
                        if result == "NEW_MAZE":
                            return "NEW_MAZE"
                        if not result:
                            return False
                        bfs_last_result = stats
                    elif self.compare_button.is_clicked(event.pos):
                        if dfs_last_result and bfs_last_result:
                            result = self.show_comparison_screen(dfs_last_result, bfs_last_result)
                            if result == "NEW_MAZE":
                                return "NEW_MAZE"
                            if not result:
                                return False
                    elif self.exit_button.is_clicked(event.pos):
                        return False
            self.clock.tick(30)

    def quit(self):
        pygame.quit()
